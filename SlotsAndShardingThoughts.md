When using a clustered redis database and LUA scripts you can run into issues if you don't understand that each execution of a LUA script only happens against a single shard with a subset of possible slots.

I refer to the value used to route requests and identify the associated slots to a key as the routing value.

When executing a LUA script against redis it is good to provide a routing value that matches the slot assignment of the interesting keys to be processed during the execution of that script.  

This is done by ensuring that at least 1 key-value is passed to the LUA script. (which is the way LUA in Redis figures out the routing value)

The routing value is easily identified by using the curly braces to surround it.  When your intention is to process multiple keys that live in the same slots - you can just provide the routing value in its {} rathar than naming all the keys explicitly as args to the LUA script.

**********
Below, I have provided routing values and their standard mapping to a grouping of slots in various small clusters:

``` 
With 2 Partitions/Shards:
{1} == slots from 8192-16383
{2} == slots from 0-8191

So - invoke your LUA 2X like this to ensure all shards are processed:
EVALSHA <SHA_VALUE> 1 {1} <other_args_separated_by_spaces>
EVALSHA <SHA_VALUE> 1 {2} <other_args_separated_by_spaces>

With 4 Partitions/Shards:
{1} == slots from 8192-12287
{2} == slots from 4096-8191
{3} == slots from 0-4095
{4} == slots from 12288-16383

So - invoke your LUA 4X like this to ensure all shards are processed:
EVALSHA <SHA_VALUE> 1 {1} <other_args_separated_by_spaces>
EVALSHA <SHA_VALUE> 1 {2} <other_args_separated_by_spaces>
EVALSHA <SHA_VALUE> 1 {3} <other_args_separated_by_spaces>
EVALSHA <SHA_VALUE> 1 {4} <other_args_separated_by_spaces>

With 8 Partitions/Shards:
{1} == slots from 8192-10239
{2} == slots from 4096-6143
{3} == slots from 0-2047
{4} == slots from 12288-14335
{1a} == slots from 2048-4095
{1b} == slots from 14336-16383
{1c} == slots from 10240-12287
{1d} == slots from 6144-8191

So - invoke your LUA 8X like this to ensure all shards are processed:
EVALSHA <SHA_VALUE> 1 {1} <other_args_separated_by_spaces>
EVALSHA <SHA_VALUE> 1 {2} <other_args_separated_by_spaces>
EVALSHA <SHA_VALUE> 1 {3} <other_args_separated_by_spaces>
EVALSHA <SHA_VALUE> 1 {4} <other_args_separated_by_spaces>
EVALSHA <SHA_VALUE> 1 {1a} <other_args_separated_by_spaces>
EVALSHA <SHA_VALUE> 1 {1b} <other_args_separated_by_spaces>
EVALSHA <SHA_VALUE> 1 {1c} <other_args_separated_by_spaces>
EVALSHA <SHA_VALUE> 1 {1d} <other_args_separated_by_spaces>

With 3 Partitions/Shards: (using standard hashing policy)
{1} == slots from 5461-10922
{3} == slots from 0-5460
{4} == slots from 10923-16383

So - invoke your LUA 3X like this to ensure all shards are processed:
EVALSHA <SHA_VALUE> 1 {1} <other_args_separated_by_spaces>
EVALSHA <SHA_VALUE> 1 {3} <other_args_separated_by_spaces>
EVALSHA <SHA_VALUE> 1 {4} <other_args_separated_by_spaces>

With 6 Partitions/Shards: (using standard hashing policy)
{1} == 8192-10922
{2} == 5461-8191
{3} == 0-2729
{4} == 13654-16383
{1A} == 10923-13653
{1AA} == 2730-5460

So - invoke your LUA 6X like this to ensure all shards are processed:
EVALSHA <SHA_VALUE> 1 {1} <other_args_separated_by_spaces>
EVALSHA <SHA_VALUE> 1 {2} <other_args_separated_by_spaces>
EVALSHA <SHA_VALUE> 1 {3} <other_args_separated_by_spaces>
EVALSHA <SHA_VALUE> 1 {4} <other_args_separated_by_spaces>
EVALSHA <SHA_VALUE> 1 {1A} <other_args_separated_by_spaces>
EVALSHA <SHA_VALUE> 1 {1AA} <other_args_separated_by_spaces>

```
If you do not use deliberate routing values in your keys it's OK - you can use SCAN to find the ones that are local to a particular routing value: 

``` 
> SET s:name owen
OK
> EVAL "return redis.call('SCAN','0','MATCH','s:na*','COUNT','9000000')" 1 {1}
1) "0"
2) (empty array)
> EVAL "return redis.call('SCAN','0','MATCH','s:na*','COUNT','9000000')" 1 {2}
1) "0"
2) 1) "s:name"
```

Then , just be sure to only attempt to process the keys that are found in that local shard during that particular execution.

Gather all the local keys that match the pattern of interest and be sure to only process those each time the script is run.  You need to run the script X times where X == number of Partitions (each time with a different routing value as the argument)

****** 
For example - let's say we wanted to create a second copy of all keys starting with prefix equal to some value (ARGV[2] in the following script):
``` 
local index = ARGV[1] 
local prefix = ARGV[2] 
local count = ARGV[3] 
local scanResults = redis.call('SCAN',index,'MATCH',prefix,'COUNT',count) 
if #{scanResults[2][1]} > 0 
  then local innerLoop = 1 
  while #{scanResults[2][innerLoop]} > 0 
    do redis.call('COPY',scanResults[2][innerLoop],'update:'..scanResults[2][innerLoop]..'{'..scanResults[2][innerLoop]..'}') 
    innerLoop=(innerLoop+1) 
  end 
end 
return scanResults[1]
```
We load the script to get a reusable SHA value:
``` 
SCRIPT LOAD "local index = ARGV[1] local prefix = ARGV[2] local count = ARGV[3] local scanResults = redis.call('SCAN',index,'MATCH',prefix,'COUNT',count) if #{scanResults[2][1]} > 0 then local innerLoop = 1 while #{scanResults[2][innerLoop]} > 0 do redis.call('COPY',scanResults[2][innerLoop],'update:'..scanResults[2][innerLoop]..'{'..scanResults[2][innerLoop]..'}') innerLoop=(innerLoop+1) end end return scanResults[1]"
ac849bf9367e23d9fddba59a0738ce898e9287b6
```
We can then call it as many times as we need to... to ensure all matching keys in all shards/partitions are processed:
``` 
EVALSHA ac849bf9367e23d9fddba59a0738ce898e9287b6 1 {1} 0 s:nam* 1
3
EVALSHA ac849bf9367e23d9fddba59a0738ce898e9287b6 1 {1} 3 s:nam* 1
0
```
#### Notice that when calling the script repeatedly, we first use 0 and then use the return value as the 1st argument which allows us to SCAN all keys in that shard 
(when the response from the script is a 0 - we can stop executing it against that routing value as it means there are no more possible matches in that partition)

Next: we move on to the next/remaining Shard/routing values:

``` 
EVALSHA ac849bf9367e23d9fddba59a0738ce898e9287b6 1 {4} 0 s:nam* 1
3
EVALSHA ac849bf9367e23d9fddba59a0738ce898e9287b6 1 {4} 3 s:nam* 1
0
```

So, if we started like this:
``` 
SET s:name1 Fred
OK
SET s:name2 Julius
OK
SET s:name3 Misha
OK
SET s:name4 Friedrich
OK
SET s:name5 Samantha
OK
SET s:name6 Mufasa
OK
SET s:name7 owen
OK
SET s:name8 Xi
OK
SET s:name9 Susan
OK
SET s:name10 Ameer
OK
```
After running the script as many times as needed against all shards/partitions: 
``` 
> keys *
 1) "s:name1"
 2) "s:name9"
 3) "update:s:name5{s:name5}"
 4) "s:name5"
 5) "update:s:name9{s:name9}"
 6) "update:s:name1{s:name1}"
 7) "s:name4"
 8) "s:name8"
 9) "update:s:name8{s:name8}"
10) "update:s:name4{s:name4}"
11) "update:s:name10{s:name10}"
12) "s:name10"
13) "s:name7"
14) "update:s:name3{s:name3}"
15) "update:s:name7{s:name7}"
16) "s:name3"
17) "update:s:name2{s:name2}"
18) "update:s:name6{s:name6}"
19) "s:name6"
20) "s:name2"

> get update:s:name1{s:name1}
"Fred"
```

It may not be obvious that in order for the copy to work we have to ensure that the copy is written to the same shard as where the execution is taking place.

It is because of this, that the script uses the original keyname as the routing value for each copy.
The script could instead use the KEYS[1] value as the routing value for each copy - it would accomplish the same outcome.

The one extra value of using the original keyname as the routing value is in the case where a future scaling event occurs and you want to redistribute your keys to more shards - using the original name as the routing value will facilitate more division - according to the variance present in the original keynames.

Note also - in the above scenario, in most cases it would be good to pass a larger value for the count so that more keys are processed in a single execution - however, LUA scripts will time out if they take too long, so you will want to test and find a happy count value that is optimal for your situation and needs. 

## Here is a second example - similar to the one above - but this one unlinks keys instead:

1. load the script into Redis so it is easily reused across clients
2. execute the script using the returned SHA value and supplying the necessary args:  
```1``` (to indicate a single routing key value is being provided)
```{1}``` (to act as the routing value for this iteration)   
```0``` (to indicate the cursorID for the embedded SCAN operation)  
```mon*``` (to indicate the prefix to be used in the scan)
```500``` (to determine how many keys to scan looking for a match)
3. Capture the returned cursorID and re-execute the script using the same routing value until it is equal to ```0```
4. Once the returned cursorID is equal to ```0``` - move on to the next routing value 
5. Repeat until all routing values have been utilized and all cursorIDs have returned ```0```

## <em>Here it is in action:</em>
(note in the example below - the use of keys command is not recommended, nor necessary and only used as a way to prove the script works!)
```
SCRIPT LOAD "local index = ARGV[1] local prefix = ARGV[2] local count = ARGV[3] local unlinked = 0 local scanResults = redis.call('SCAN',index,'MATCH',prefix,'COUNT',count) if #{scanResults[2][1]} > 0 then local innerLoop = 1 while #{scanResults[2][innerLoop]} > 0 do redis.call('UNLINK',scanResults[2][innerLoop]) innerLoop=(innerLoop+1) unlinked=(unlinked+1)end end return 'unlinked '..unlinked..' keys!  Use this # as your next scan id Arg: '..scanResults[1]"
```
in this example - result of SCRIPT LOAD Is ```"3624b7980adc18c24708839669e203a8a15cdeec"```
``` 
> keys mon*
1) "mon{1}"
2) "mon{4}"
3) "mon{2}"
4) "mon{3}"

> EVALSHA "3624b7980adc18c24708839669e203a8a15cdeec" 1 {1} 0 mon* 500
"unlinked 2 keys!  Use this # as your next scan id Arg: 83"

> keys mon*
1) "mon{2}"
2) "mon{3}"

> EVALSHA "3624b7980adc18c24708839669e203a8a15cdeec" 1 {1} 83 mon* 500
"unlinked 0 keys!  Use this # as your next scan id Arg: 0"

> keys mon*
1) "mon{2}"
2) "mon{3}"

> EVALSHA "3624b7980adc18c24708839669e203a8a15cdeec" 1 {2} 0 mon* 500
"unlinked 1 keys!  Use this # as your next scan id Arg: 595"

> keys mon*
1) "mon{2}"

> EVALSHA "3624b7980adc18c24708839669e203a8a15cdeec" 1 {2} 595 mon* 500
"unlinked 1 keys!  Use this # as your next scan id Arg: 0"

> keys mon*
(empty list or set)
```




