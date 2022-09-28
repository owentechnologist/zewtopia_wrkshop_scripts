### The following lua / redis-cli commands are used together to create zoo visitor purchase events on a redis stream

### Step 1: Create a Set of common items that are sold at zewtopia:
#### Note that you run the next command inside an active redis-cli shell
``` 
EVAL "do redis.call('SADD',KEYS[1],'10.00:3d movie ticket') redis.call('SADD',KEYS[1],'2.00:bottle of water') redis.call('SADD',KEYS[1],'3.00:bottle of juice') redis.call('SADD',KEYS[1],'8.00:Turkey Burger') redis.call('SADD',KEYS[1],'5.00:French Fries') redis.call('SADD',KEYS[1],'6.00:Fruit Smoothie') redis.call('SADD',KEYS[1],'8.00:Vegetable Wrap') redis.call('SADD',KEYS[1],'10.00:book') redis.call('SADD',KEYS[1],'15.00:stuffed animal') redis.call('SADD',KEYS[1],'1.00:pin') redis.call('SADD',KEYS[1],'2.00:postcard') redis.call('SADD',KEYS[1],'5.00:child entrance ticket') redis.call('SADD',KEYS[1],'15.00:Adult entrance ticket') redis.call('SADD',KEYS[1],'1.50:lollipop') redis.call('SADD',KEYS[1],'12.00:jigsaw puzzle') end" 1 zew:{batch2}:common
```

### Step 2: Create a Set of rarer items that are sold at zewtopia:
#### Note that you run the next command inside an active redis-cli shell
```
EVAL "do  redis.call('SADD',KEYS[1],'8.00:Senior Entrance Ticket') redis.call('SADD',KEYS[1],'80.00:Family Annual Subscription') redis.call('SADD',KEYS[1],'16.00:Butterfly Hall Experience') redis.call('SADD',KEYS[1],'60.00:Hardcover Book') end" 1 zew:{batch2}:rare
```

### Step 3: Populate a redis stream with events that look like this:
``` 
XRANGE zew:{batch2}:revenue:stream - + COUNT 2
1) 1) "1663662326713-0"
   2) 1) "visitor_purchase"
      2) "2.00:bottle of water"
2) 1) "1663662326713-1"
   2) 1) "visitor_purchase"
      2) "5.00:child entrance ticket"

```
#### This next example shows how to populate the stream using random elements from the prior sets
### Populate the stream with bursts of 50 purchase activities every 10 seconds for 2 minutes:
#### (make certain your host and port are correct)
#### Note that you run the next command from a command-shell and that calls redis-cli so that the -i and -r switches come into effect:
#### -i is an interval measured in seconds -r says to repeat something multiple times
```
redis-cli -h 192.168.1.20 -p 12000 -i 10 -r 12 EVAL "for index = 1,50 do redis.call('XADD', KEYS[1],'*','visitor_purchase', index %3 == 0 and redis.call('SRANDMEMBER', KEYS[3]) or redis.call('SRANDMEMBER', KEYS[2])) end return 'Added 50 park visitor purchase events'" 3 zew:{batch2}:revenue:stream zew:{batch2}:common zew:{batch2}:rare
```
