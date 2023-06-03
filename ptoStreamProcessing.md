### This series of commands showcases the use of Redis Streams -- including the Claiming of Pending events that have been given to members of a worker group

#### 1. Establish two sets of data that will be used in our simple example:
* A SET of dates
* A SET of employee Ids
#### 2. Register a ‘managers’ worker group to process a RedisStream
#### 3. Create several PTO requests as events written to the RedisStream
#### 4. Have manager/workers process the events from the stream (some should fail and get stuck)
#### 5. Process the stuck events as a supervisor process that can deny requests

### Using Redis-cli execute the following:

### Write the first SET of data:

```
SADD dates{ot11} "2022-12-24" "2022-12-25" "2022-12-26" "2022-12-27" "2022-12-28" "2022-12-29" "2022-12-30" "2022-12-31"
```

### Write the second SET of data:

```
SADD ids{ot11} 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
```

### Create a worker group called ‘managers’  to process Stream events:

```
XGROUP CREATE X:requests{ot11} managers 0 MKSTREAM
```

### Execute the following script 10 or more times:

``` 
EVAL "local id = redis.call('SRANDMEMBER','ids'..KEYS[1]) local date = redis.call('SRANDMEMBER','dates'..KEYS[1]) redis.call('XADD','X:requests'..KEYS[1],'*','empid',id,'startDate',date, 'numDays',(id%5))" 1 {ot11}
```

Now would be a good time to look at the information available in Redis Insight if you have it.
* Can you see the messages/events written to the stream?
* Can you find the ‘managers’ worker Group?
* Are any messages in a ‘Pending’ state?

### Now, Let's act as workers in our 'managers' worker groyp
### Execute the following script 10 or more times:
(For some executions, change the last argument to manager2 or manager3 to show multiple workers)

``` 
EVAL "local maxdays = 10 local msg = 'stuck during processing' local ptoRequest = redis.call('XREADGROUP','GROUP','managers',ARGV[1],'COUNT','1','STREAMS','X:requests'..KEYS[1],'>') local eventid = ptoRequest[1][2][1][1] local empid = ptoRequest[1][2][1][2][2] local startDate = ptoRequest[1][2][1][2][4] local days = ptoRequest[1][2][1][2][6] if (( days > '0' ) and redis.call('SISMEMBER','used'..KEYS[1],empid)<1) then msg = 'PTO approved for '..days..' days' redis.call('XADD','X:results'..KEYS[1],'*','empid',empid,'startDate',startDate,'numDays',days,'manager',ARGV[1],'status','approved') redis.call('XACK','X:requests'..KEYS[1],'managers',eventid) redis.call('SADD','used'..KEYS[1],empid) end return msg" 1 {ot11} manager1
```
#### <em>NB: When there are no remaining messages to process you will see an error like this:</em>
``` 
@user_script:1: user_script:1: attempt to index local 'ptoRequest' (a boolean value)
```

### By now, you should have seen at least one request get stuck as the managers are not equipped to process duplicate requests nor requests for zero days off
### It is time to look for Pending messages and Claim them as a supervisor so that they can be denied!
### Execute the following script multiple times and check the information available in Redis Insight to see what the impact of all the above has been

``` 
EVAL "local msg = 'abc' local stuckRequestID = redis.call('XPENDING','X:requests'..KEYS[1],'managers','-','+','1')[1][1] local ptoRequest = redis.call('XCLAIM','X:requests'..KEYS[1],'managers',ARGV[1],'0',stuckRequestID) local eventid = ptoRequest[1][1] local empid = ptoRequest[1][2][2] local startDate = ptoRequest[1][2][4] local days = ptoRequest[1][2][6] if (days < '1') then msg = 'request denied (PTO must be > 0 days)' end if redis.call('SISMEMBER','used'..KEYS[1],empid)>0 then msg = 'request denied  employee '..empid..' already requested PTO' end redis.call('XADD','X:results'..KEYS[1],'*','empid',empid,'startDate',startDate,'numDays',days,'manager', ARGV[1], 'status', 'denied', 'reason',msg) redis.call('XACK','X:requests'..KEYS[1],'managers',eventid) return msg" 1 {ot11} supervisor
```
#### <em>NB: When there are no remaining Pending messages to process, you will see an error like this:</em>
``` 
@user_script:1: user_script:1: attempt to index field '?' (a nil value)
```





