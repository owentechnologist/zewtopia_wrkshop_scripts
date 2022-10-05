# Zewtopia Ticket Sales!
### <em>you will need access to a Redis-TimeSeries Database to work with the following data:</em>
## Executing the scripts below will populate several time-series keys that track ticket sales over 10 years for various attractions at the zoo

* Cleanup any old keys:
``` 
del zew:adult:{tickets}
del zew:child:{tickets}
del zew:pettingzoo:{tickets}
del zew:bonobolecture:{tickets}
del zew:gorillafeeding:{tickets}
```
* Create 5 new keys establishing labels so that they can later be analyzed and filtered and grouped:
``` 
TS.CREATE zew:adult:{tickets} retention 0 LABELS data tickets attraction zoo isfree false type adult
TS.CREATE zew:child:{tickets} retention 0 LABELS data tickets attraction zoo isfree false type child
TS.CREATE zew:pettingzoo:{tickets} retention 0 LABELS data tickets attraction pettingzoo isfree true type all
TS.CREATE zew:bonobolecture:{tickets} retention 0 LABELS data tickets attraction bonobolecture isfree false type adult
TS.CREATE zew:gorillafeeding:{tickets} retention 0 LABELS data tickets attraction gorillafeeding isfree true type all
```

* populate the keys with values for 10 years of ticket sales:

``` 
EVAL "for season = 1251784800000,1629525600000,7869600000 do for index = 0,365 do local vall = math.random(1,120) redis.call('TS.ADD', 'zew:adult:{tickets}', ((index*11200000)+season), (vall+1) ) end end" 1 {tickets} 
EVAL "for season = 1251784800000,1629525600000,7869600000 do for index = 0,365 do local vall = math.random(2,220) redis.call('TS.ADD', 'zew:child:{tickets}', ((index*11200000)+season), (vall+1) ) end end" 1 {tickets} 
EVAL "for season = 1251784800000,1629525600000,7869600000 do for index = 0,365 do local vall = math.random(1,90) redis.call('TS.ADD', 'zew:pettingzoo:{tickets}', ((index*11200000)+season), (vall+1) ) end end" 1 {tickets} 
EVAL "for season = 1251784800000,1629525600000,7869600000 do for index = 0,365 do local vall = math.random(1,20) redis.call('TS.ADD', 'zew:bonobolecture:{tickets}', ((index*11200000)+season), (vall+1) ) end end" 1 {tickets} 
EVAL "for season = 1251784800000,1629525600000,7869600000 do for index = 0,365 do local vall = math.random(30,80) redis.call('TS.ADD', 'zew:gorillafeeding:{tickets}', ((index*11200000)+season), (vall+1) ) end end" 1 {tickets} 
```

* now begin your analysis using Time-Series Queries:

``` 
TS.MRANGE - + FILTER data=tickets isfree=(false,true) GROUPBY isfree REDUCE SUM
```

* can you tell whether tickets that are free are more popular than tickets that are not free?

* How would you query the time-series to uncover which of the attractions sells the most tickets?