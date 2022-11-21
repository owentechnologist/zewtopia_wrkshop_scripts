When using a clustered redis database and LUA scripts you can run into issues if you don't understand that each execution of a LUA script only happens against a single shard with a subset of possible slots.

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
192.168.1.20:18386> SET s:name owen
OK
192.168.1.20:18386> EVAL "return redis.call('SCAN','0','MATCH','s:na*','COUNT','9000000')" 1 {1}
1) "0"
2) (empty array)
192.168.1.20:18386> EVAL "return redis.call('SCAN','0','MATCH','s:na*','COUNT','9000000')" 1 {2}
1) "0"
2) 1) "s:name"
```

Then , just be sure to only attempt to process the keys that are found in that local shard during that particular execution.

Gather all the local keys that match the pattern of interest and be sure to only process those each time the script is run.  You need to run the script X times where X == number of Partitions (each time with a different routing value as the argument)
