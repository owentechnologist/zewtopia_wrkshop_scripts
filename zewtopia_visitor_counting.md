## This example shows how to use Count Min Sketch to keep track of many items that need to be counted

### As is common with probablistic data structures - there is the potential for accuracy to be sacrificed in exchange for speed and memory conservation

### Imagine we have a need to keep track of everytime someone visits any of our exhibits in Zewtopia - we have hundreds of exhibits and we get millions of visitors a year.  
We don't really care if we are off by a few percentage points - do we?

* Define and Create the Count Min Sketch Object in Redis: (the smaller the values - the more accurate the count)

```
CMS.INITBYPROB {cms}:zew:visitor:counts 0.001 0.05
```

* We will use the Count Min Sketch to record visitors as they stop at various exhibits  like this:
```
CMS.INCRBY {cms}:zew:visitor:counts <some_entry_id> <some-val>
```

* this script will populate over a million unique happenings. It also stores two of the counts in redis strings so that we can compare them and their deterministic scores to the scores recorded by our Count Min Sketch:

```
EVAL "for index = 80,3000 do local vcount = math.random(30,80) redis.call('CMS.INCRBY','{cms}:zew:visitor:counts',ARGV[1], vcount, ARGV[2], index%vcount ) redis.call('INCRBY','{cms}'..ARGV[1],vcount) redis.call('INCRBY','{cms}'..ARGV[2],index%vcount) for inner = 1,998 do redis.call('CMS.INCRBY','{cms}:zew:visitor:counts',ARGV[1]..inner, vcount, ARGV[2]..inner, index%vcount ) end end" 1 {cms} 'zebra_pen' 'lion_pen' 
```

* Query the Count Min Sketch: (some rare results may be inflated)

```
CMS.QUERY {cms}:zew:visitor:counts 'lion_pen' 'zebra_pen' 'lion_pen22' 'zebra_pen100'
1) (integer) 159766
2) (integer) 159933
3) (integer) 79883
4) (integer) 159933
```

* Check results against the deterministic strings:

```
mget {cms}lion_pen {cms}zebra_pen
1) "79883"
2) "159933"
```

### As shown above it can be seen that 100% accuracy is not guaranteed.  You can get close to 100% if you size the data structure accordingly.
### You could try the above exercise again - this time using these setting for the Count Min Sketch object:

```
CMS.INITBYPROB {cms}:zew:visitor:counts 0.001 0.01
```

### It is worth noting the difference in memory needed as the settings change

### You can use this command to find out what each version requires:

* the original settings use this much ram:
```
memory usage {cms}:zew:visitor:counts
(integer) 80064
```

* the more accurate version with the smaller rate of error uses this much:

``` 
memory usage {cms}:zew:visitor:counts
(integer) 112064
```

