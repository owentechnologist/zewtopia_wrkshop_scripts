### The Zoo website is being overloaded with requests. We need to throttle the interactions using a rate-limiting strategy.
#### We aren't sure which strategy to employ, so we will test some alternatives - recording the activity that gets through using Redis timeseries.  (this will allow us to visualize the outcome of each rate-limiting strategy)

## Strategy #1 Uniform Rate Limiter
### The rule here is no 1 caller is allowed to use a resource more than 1 / defined time-span in milliseconds
### Example:  bob can buy tickets to the tiger feeding only once every 10 seconds
### Implementation: Create a binary String as a gate in Redis for each resource/endpoint we want to protect for each unique caller.
### Establish a TTL for the key equal to the time frame we want to track
### We will use this naming convention, so we remember what is supposed to happen:
``` 
rl:<path>:<caller-id>
example:
rl:zewtopia.com/tigerfeeding:bob
```
### Every time a request is made we check the TTL on the gate to see if it is > 0 
### If it is greater than zero we do not allow another request
### Else - we set the TTL to the time-frame-in-seconds
### When a client seeks to access the resource associated with the gate, we check for TTL > 0 and if so, deny the request.
#### Let's look at how that behavior looks over time by firing many requests against a gated resource and logging the ones that get through as events in a TimeSeries key.
### We have our clients call this LUA script to manage the gating logic:
``` 
SCRIPT LOAD "if redis.call('ttl', KEYS[1]) > 0 then return 0 else redis.call('set',KEYS[1],ARGV[1],'PX',ARGV[1]) return redis.call('exists',KEYS[1]) end"
```
#### Loading the Lua script results in a SHA value being returned that acts as a reference to that same script.
#### We would then call such a script like this:
``` 
EVALSHA c1abd52961929c86bc593c66bc304e9ba5b5990e 1 rl:zewtopia.com/tigerfeeding:bob 10000
```
#### If we get back a 0 it means we should not continue with our request to the gated resource.
``` 
127.0.0.1:6379> time
1) "1668631508"
2) "791244"
127.0.0.1:6379> EVALSHA c1abd52961929c86bc593c66bc304e9ba5b5990e 1 rl:zewtopia.com/tigerfeeding:bob 10000
(integer) 1
127.0.0.1:6379> time
1) "1668631515"
2) "574130"
127.0.0.1:6379> EVALSHA c1abd52961929c86bc593c66bc304e9ba5b5990e 1 rl:zewtopia.com/tigerfeeding:bob:10 10000
(integer) 0
127.0.0.1:6379> time
1) "1668631525"
2) "94945"
127.0.0.1:6379> EVALSHA c1abd52961929c86bc593c66bc304e9ba5b5990e 1 rl:zewtopia.com/tigerfeeding:bob:10 10000
(integer) 1
```
### * Upside:  Each caller is gated in an even manner according to the time frame supplied  
### * Downside: If instead callers wanted to burn through a bag of credits where some could be used in a burst - this will not accommodate that behavior
### * Downside: If there are hundreds of millions of callers and thousands of gated resources the number of keys will grow to be very large
### * Downside: The resource itself is not protected if a gang of callers all happen to pass their gates at the same moment

## Strategy #2 Resource Credits-based 'Bursty' (Sliding Window) Rate Limiter

### The concept here is the resource allows for X requests by anyone within a certain timeframe.
### Once those credits run out, everyone waits until the next timeframe begins.

### Example:  The tiger feeding resource allows 100 tickets to be purchased every 10 seconds - whoever gets them first wins

### Implementation:  Create a SortedSet that tracks all requests for the gated resource
### For each submitted request, an entry is added to the SortedSet using the timestamp as measured by Redis for both the score and value 
### When each request comes in, use REMRANGEBYSCORE to remove any records of requests older than:
```
( [the current time] minus [the allotted time window] )
``` 

### Then:
### Count the number of requests that remain in that SortedSet and if it is higher than the defined limit ... reject the request (return 0)

### We will use this naming convention so we remember what is supposed to happen:
``` 
z:<path>:<timeframe-in-milliseconds>
example:
z:zewtopia.com/tigerfeeding:10000
```
### We have our clients call this LUA script to manage the gating logic:
``` 
SCRIPT LOAD "local oneMeansOK = 1 local glimit = 0+ARGV[2] local t=redis.call('TIME') redis.call('SET','time{'..KEYS[1]..'}',''..t[1]..t[2]) local fullTime = redis.call('GET','time{'..KEYS[1]..'}') local delta = (fullTime - ARGV[1]) redis.call('ZREMRANGEBYSCORE',KEYS[1],'0',delta) local rcount = (redis.call('ZCARD',KEYS[1])) if (rcount == glimit) then oneMeansOK = 0 elseif (rcount < glimit) then redis.call('ZADD',KEYS[1],fullTime,t[1]..':'..t[2]) end return oneMeansOK"
```
#### Loading the Lua script results in a SHA value being returned that acts as a reference to that same script.
#### We would then call such a script with args like this:
<ol>
<li>The number of keys passed in during this invocation</li>
<li>The keyname that will be used to create the SortedSet that tracks the number of resource uses</li>
<li>The time-window measured in microseconds (10000000 == 10 seconds) </li>
<li>The allowed number of invocations for the time-window</li>
</ol>

<img src="https://github.com/owentechnologist/LUA_rateLimiting/blob/main/ratelimiting.png" width="800"/>

``` 
127.0.0.1:6379> EVALSHA cbff0c5457b4bb3ad718d5f8f147ed70bd6a1d37 1 z:zewtopia.com/tigerfeeding 10000000 3
(integer) 1
127.0.0.1:6379> time
1) "1668807303"
2) "988345"
127.0.0.1:6379> EVALSHA cbff0c5457b4bb3ad718d5f8f147ed70bd6a1d37 1 z:zewtopia.com/tigerfeeding 10000000 3
(integer) 1
127.0.0.1:6379> time
1) "1668807306"
2) "468427"
127.0.0.1:6379> EVALSHA cbff0c5457b4bb3ad718d5f8f147ed70bd6a1d37 1 z:zewtopia.com/tigerfeeding 10000000 3
(integer) 1
127.0.0.1:6379> time
1) "1668807308"
2) "411043"
127.0.0.1:6379> EVALSHA cbff0c5457b4bb3ad718d5f8f147ed70bd6a1d37 1 z:zewtopia.com/tigerfeeding 10000000 3
(integer) 0
```

### When we get a 1 as a response - we can use the protected resource
### A 0 response tells us to wait 

### * Upside:  sometimes it is useful to allow bursts of activity up to a limit within a timeframe
### * Upside: One SortedSet key is needed to protect a single resource and can be reused across many distinct clients
### * Downside: One client might take up all the available credits for a timeframe
### * Downside: Fastest client wins

## An expanded solution where both the individual clients and the protected resource are given limits can be seen here: 
[https://github.com/owentechnologist/LUA_rateLimiting](https://github.com/owentechnologist/LUA_rateLimiting)


