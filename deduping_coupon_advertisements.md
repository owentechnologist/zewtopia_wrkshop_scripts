# CF example:
The Zewtopia Zoo survives largely due to online/apps and games that enable targeted advertising for our partners.
When a visitor launches our app or launches a new level of a game, they receive an informational text about an exhibit along with a coupon to purchase one of our partner products.
Our contract with our partners insists that we try to send one of each coupon to each visitor in a month.
We try to balance that with the need to not annoy our visitors with more than one copy of a coupon.

The way we choose to manage this is to use a CuckooFilter to keep track of the combination of coupons and visitorIDs.
If the combination exists in the monthly CuckooFilter, we know not to send that coupon to that user.

To simulate this activity we will first create two Sets from which we will draw random elements:
1) a set of userIDs
2) a set of couponIds

```
EVAL "for id = 1,1200000 do redis.call('SADD',KEYS[1],'visitor'..id) end" 1 ot11:zew:visitor:{ids}
```

```
EVAL "for id = 1,150 do redis.call('SADD',KEYS[1],'coupon'..id) end" 1 ot11:zew:coupon:{ids}
```

Next, we will condense a month's advertising activity into a few seconds using the following lua script:
```
EVAL "for index = 1,800000, 1 do local vistorid = redis.call('SRANDMEMBER',KEYS[3]) local couponid = redis.call('SRANDMEMBER',KEYS[2]) local compound_id = ('visitorid:'..vistorid..':couponid:'..couponid) local addresult = redis.call('CF.ADDNX', KEYS[1], (compound_id)) if addresult == 0 then redis.call('XADD',KEYS[4],'*','Add_duplicate_prevented_for',compound_id) end end" 4 ot11:cf:coupons:october:{ids} ot11:zew:coupon:{ids} ot11:zew:visitor:{ids} ot11:add_dupe_stream{ids}
```
** If you receive an error fix it by creating a larger cuckoo filter:
If you receive an error: Maximum expansions reached (this means you did not reserve enough space for the cuckoo filter)
Delete it:
```
del ot11:cf:coupons:october:{ids}
```
Also delete the stream key that was tracking the avoided duplicates:

``` 
del ot11:add_dupe_stream{ids}
```
Then recreate the Cuckoo filter with the following settings:
```
CF.RESERVE ot11:cf:coupons:october:{ids} 10000000 MAXITERATIONS 10 EXPANSION 1 BUCKETSIZE 2
```

Run the simulation again to populate the CF:
```
EVAL "for index = 1,800000, 1 do local vistorid = redis.call('SRANDMEMBER',KEYS[3]) local couponid = redis.call('SRANDMEMBER',KEYS[2]) local compound_id = ('visitorid:'..vistorid..':couponid:'..couponid) local addresult = redis.call('CF.ADDNX', KEYS[1], (compound_id)) if addresult == 0 then redis.call('XADD',KEYS[4],'*','Add_duplicate_prevented_for',compound_id) end end" 4 ot11:cf:coupons:october:{ids} ot11:zew:coupon:{ids} ot11:zew:visitor:{ids} ot11:add_dupe_stream{ids}
```

Finally, we can see how many (if any) users were protected from receiving duplicate notices thanks to the use of ADDNX:
```
XLEN ot11:add_dupe_stream{ids}
```
To see some examples of the deduped coupons:
```
XRANGE ot11:add_dupe_stream{ids} - + COUNT 2
```

