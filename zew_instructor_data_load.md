Created on May 31st 2023 in anticipation of a workshop with shared Redis database instances...

This file contains useful 'zewtopia workshop' data loading efforts possible through LUA or simple redis commands

By copy-pasting the commands into RedisInsight V2 Workbench and executing the Play button - the data will be loaded into the connected Redis Database

This is intended to make it easy for the lab exercises to be done by participants where having a suitable dataset for each exercise will speed their progress

Using this method is optional, and it's execution should normally be recommended by your instructor to avoid redundancy of effort and possible confusion
(Some of the commands are only intended to be executed one time - while others can be done by each participant using a separate prefix and/or routing value)

* The following is the data population command to be copy-pasted and executed before the search sections:

``` 
EVAL "do redis.call('SADD',KEYS[1],'Lion') redis.call('SADD',KEYS[1],'Tiger') redis.call('SADD',KEYS[1],'Elephant') redis.call('SADD',KEYS[1],'Giant Panda') redis.call('SADD',KEYS[1],'Gorilla') redis.call('SADD',KEYS[1],'Giraffe') redis.call('SADD',KEYS[1],'Polar Bear') redis.call('SADD',KEYS[1],'Hippo') redis.call('SADD',KEYS[1],'Cheeta') redis.call('SADD',KEYS[1],'Zebra') redis.call('SADD',KEYS[1],'Meerkat') redis.call('SADD',KEYS[1],'Penguin') redis.call('SADD',KEYS[1],'Kangaroo') redis.call('SADD',KEYS[1],'Flamingo') redis.call('SADD',KEYS[1],'Koala') redis.call('SADD',KEYS[1],'Chimpanzee') redis.call('SADD',KEYS[1],'Llama') redis.call('SADD',KEYS[1],'Green Anaconda') redis.call('SADD',KEYS[1],'Hyena') redis.call('SADD',KEYS[1],'Bonobo') redis.call('SADD',KEYS[1],'Alligator') redis.call('SADD',KEYS[1],'Orangutan') end" 1 zew:{batch1}:species
EVAL "do redis.call('SADD',KEYS[1],'chronic gastroenteritis') redis.call('SADD',KEYS[1],'acute gastroenteritis') redis.call('SADD',KEYS[1],'enteric parasites') redis.call('SADD',KEYS[1],'bite wound') redis.call('SADD',KEYS[1],'gore wound') redis.call('SADD',KEYS[1],'various lacerations') redis.call('SADD',KEYS[1],'bacterial abscess') redis.call('SADD',KEYS[1],'dystocia') redis.call('SADD',KEYS[1],'ingestion of foreign body') redis.call('SADD',KEYS[1],'osteoarthritis') redis.call('SADD',KEYS[1],'bacterial pneumonia') redis.call('SADD',KEYS[1],'tooth rot') redis.call('SADD',KEYS[1],'oral trauma') redis.call('SADD',KEYS[1],'digestive ulcer') redis.call('SADD',KEYS[1],'diabetis insipidus') end" 1 zew:{batch1}:disorders
EVAL "do redis.call('SADD',KEYS[1],'Giggly') redis.call('SADD',KEYS[1],'Charmer') redis.call('SADD',KEYS[1],'Hungry') redis.call('SADD',KEYS[1],'Biter') redis.call('SADD',KEYS[1],'Noisy') redis.call('SADD',KEYS[1],'Chess') redis.call('SADD',KEYS[1],'Fluffy') redis.call('SADD',KEYS[1],'Logan') redis.call('SADD',KEYS[1],'Lover') redis.call('SADD',KEYS[1],'September') redis.call('SADD',KEYS[1],'Scrappy') redis.call('SADD',KEYS[1],'Juicy') redis.call('SADD',KEYS[1],'Lock') redis.call('SADD',KEYS[1],'Pat') redis.call('SADD',KEYS[1],'Roman') redis.call('SADD',KEYS[1],'Bobby') redis.call('SADD',KEYS[1],'Archer') redis.call('SADD',KEYS[1],'Hunter') redis.call('SADD',KEYS[1],'Cutsie') redis.call('SADD',KEYS[1],'Nasty') redis.call('SADD',KEYS[1],'Young') redis.call('SADD',KEYS[1],'Old') redis.call('SADD',KEYS[1],'Bashful') redis.call('SADD',KEYS[1],'Sweet') redis.call('SADD',KEYS[1],'Charity') redis.call('SADD',KEYS[1],'Rescue') redis.call('SADD',KEYS[1],'Glutten') redis.call('SADD',KEYS[1],'Brown') redis.call('SADD',KEYS[1],'Sam') redis.call('SADD',KEYS[1],'Red') redis.call('SADD',KEYS[1],'Blue') redis.call('SADD',KEYS[1],'Brooklyn') redis.call('SADD',KEYS[1],'California') redis.call('SADD',KEYS[1],'Paris') redis.call('SADD',KEYS[1],'Barrel') redis.call('SADD',KEYS[1],'Angel') redis.call('SADD',KEYS[1],'Devil') redis.call('SADD',KEYS[1],'Sleepy') redis.call('SADD',KEYS[1],'Sneezy') redis.call('SADD',KEYS[1],'Doc') end" 1 zew:{batch1}:names
EVAL "for index = 1,3000 do local nums = '123456789' local alphs = redis.call('SRANDMEMBER', KEYS[4])..'aBcDeFgHiJkLmNoPqRsTuVwXyZ' local days = math.random(1,800) redis.call('HSET', KEYS[1] .. index,'species','' ..  redis.call('SRANDMEMBER', KEYS[2]),'name',redis.call('SRANDMEMBER', KEYS[4]) .. ' ' .. redis.call('SRANDMEMBER', KEYS[4]) ..' '.. index ,'gender', index %3 == 0 and 'male' or 'female' ,'known_disorders',index %3 == 0 and 'none reported' or redis.call('SRANDMEMBER', KEYS[3]),'days_in_zoo', days,'current_gps_location', '117.14'..math.random(800,1000).. ',32.73'.. math.random(0,900), 'dob',(redis.call('time')[1]-(days*(86400*math.random(1,8)))),'docid',index ..''.. math.random(1,800)..index .. string.sub(alphs,math.random(3,7),math.random(8,12)) .. math.random(1,800) .. '-41'.. math.random(1,800)..index .. string.sub(nums,math.random(1,4),math.random(5,9)) ..'-b749-'.. math.random(1,800)..index .. string.sub(alphs,math.random(4,9),math.random(10,14))) end" 4 zew:{batch1}:animal: zew:{batch1}:species zew:{batch1}:disorders zew:{batch1}:names
HSET zew:tenure:new days_in_zoo_start 0 days_in_zoo_end 20 description 'Newly arrived animals have a tendency towards extreme behaviors and high-energy output' tenure_class 'NEW'
HSET zew:tenure:settled days_in_zoo_start 21 days_in_zoo_end 300 description 'Settled animals form social bonds with others and begin adapting to the zoo environment' tenure_class 'SETTLED'
HSET zew:tenure:enduring days_in_zoo_start 301 days_in_zoo_end 30000 description 'Enduring animals show signs of weariness and psychological distress, often accompanied by persistent physical health issues' tenure_class 'ENDURING'
```
* this is a sample search index for our animal population using ot11 prefix:
``` 
FT.CREATE ot11_idx_zew PREFIX 1 "zew:" SCHEMA name TEXT PHONETIC dm:en species TAG dob NUMERIC SORTABLE gender TAG known_disorders TEXT PHONETIC dm:en days_in_zoo NUMERIC SORTABLE current_gps_location GEO SORTABLE
```
* creation of an index alias:
``` 
FT.ALIASADD ot11_a ot11_idx_zew
```
* a sample query using the alias: 
``` 
FT.SEARCH ot11_a "@name:(%Glue%) @days_in_zoo:[100 800] @current_gps_location:[117.14803,32.73259, 500 m] -@gender:{male}" LIMIT 0 1
```
* this is a second index designed to enable searching for tenure categories based on a supplied value: 
``` 
FT.CREATE ot11_idx2 PREFIX 1 "zew:tenure" SCHEMA days_in_zoo_start NUMERIC days_in_zoo_end NUMERIC
```
* a sample query to look for the tenure that corresponds to days in zoo equal to 18:
``` 
FT.SEARCH ot11_idx2 "@days_in_zoo_start:[-inf 18] @days_in_zoo_end:[18 +inf]" return 2 tenure_class description
```
* adding the injury SYNONYM to the first index created:
``` 
FT.SYNUPDATE ot11_idx_zew synonym1 "bruise" "injury" "wound" "scrape" "scratch" "lacerations" "trauma"
```

* the following creates two JSON zoo events and the ot11 search index:
```
JSON.SET zew:activities:gf $ '{"name": "Gorilla Feeding", "cost": 0.00, "times": [{"military":"0800","civilian":"8 AM"},{"military": "1500","civilian": "3 PM"}], "days": ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"],"location": "Gorilla House South", "responsible_parties": {"number_of_contacts": 1,"hosts":[{"name": "Duncan Mills","phone": "715-876-5522", "email": "dmills@zew.org"}]}}'
JSON.SET zew:activities:bl $ '{"name": "Bonobo Lecture", "cost": 10.00, "times": [{"military":"1100","civilian":"11 AM"}], "days": ["Mon", "Thur"], "location": "Mammalian Lecture Theater","responsible_parties": {"number_of_contacts": 1,"hosts":[{"name": "Dr. Clarissa Gumali", "phone": "715-322-5992", "email": "cgumali@zew.org"}]}}'
FT.CREATE ot11_activities ON JSON PREFIX 1 zew: SCHEMA $.times[*].military AS military_time TAG $.times[*].civilian AS civilian_time TAG $.location AS location TEXT SORTABLE $.cost AS cost NUMERIC SORTABLE $.name AS event_name TEXT $.days[*] AS days TAG $.responsible_parties.hosts[*].phone AS contact_phone TEXT $.responsible_parties.hosts[*].email AS contact_email TAG $.responsible_parties.hosts[*].name AS contact_name TEXT $.responsible_parties.number_of_contacts AS how_many_contacts NUMERIC
```
* and here come some sample queries:
``` 
FT.SEARCH ot11_activities "@contact_email:{dmills\\@zew\\.org}"
FT.SEARCH ot11_activities "@location:House" return 1 event_name
FT.SEARCH ot11_activities @cost:[-inf,10.00] LIMIT 0 10 return 1 contact_name
```
* and one query that requires version 2.6:
```
FT.SEARCH ot11_activities @days:{Wed} LIMIT 0 10 RETURN 1 days DIALECT 3
```
* and the aggregate query examples:
``` 
FT.SEARCH ot11_activities -@military_time:{08*} return 2 name cost SORTBY cost DESC LIMIT 0 2
FT.AGGREGATE ot11_activities @cost:[10,26] GROUPBY 1 @location REDUCE COUNT 0 as num SORTBY 2 @num DESC
FT.AGGREGATE ot11_activities * GROUPBY 0 REDUCE AVG 1 @cost as AVG_COST
```
******

* The following is the stream event creation/processing example made easy to copy/paste:
* Note that rather than use a prefix to isolate the keys - in this example a specific routing value is used 
* to create unique sets. each participant should replace {ot11} with their initials and birth-month wrapped in { } 

``` 
SADD dates{ot11} "2022-12-24" "2022-12-25" "2022-12-26" "2022-12-27" "2022-12-28" "2022-12-29" "2022-12-30" "2022-12-31"
SADD ids{ot11} 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
```
* and the stream consumer group creation:
``` 
XGROUP CREATE X:requests{ot11} managers 0 MKSTREAM
```
* and the creation of stream entries (PTO requests)
``` 
EVAL "local id = redis.call('SRANDMEMBER','ids'..KEYS[1]) local date = redis.call('SRANDMEMBER','dates'..KEYS[1]) redis.call('XADD','X:requests'..KEYS[1],'*','empid',id,'startDate',date, 'numDays',(id%5))" 1 {ot11}
```
* and the evaluation of those PTO events by manager1 :

``` 
EVAL "local maxdays = 10 local msg = 'stuck during processing' local ptoRequest = redis.call('XREADGROUP','GROUP','managers',ARGV[1],'COUNT','1','STREAMS','X:requests'..KEYS[1],'>') local eventid = ptoRequest[1][2][1][1] local empid = ptoRequest[1][2][1][2][2] local startDate = ptoRequest[1][2][1][2][4] local days = ptoRequest[1][2][1][2][6] if (( days > '0' ) and redis.call('SISMEMBER','used'..KEYS[1],empid)<1) then msg = 'PTO approved for '..days..' days' redis.call('XADD','X:results'..KEYS[1],'*','empid',empid,'startDate',startDate,'numDays',days,'manager',ARGV[1],'status','approved') redis.call('XACK','X:requests'..KEYS[1],'managers',eventid) redis.call('SADD','used'..KEYS[1],empid) end return msg" 1 {ot11} manager1
```
* and the evaluation of those PTO events by manager2 :
``` 
EVAL "local maxdays = 10 local msg = 'stuck during processing' local ptoRequest = redis.call('XREADGROUP','GROUP','managers',ARGV[1],'COUNT','1','STREAMS','X:requests'..KEYS[1],'>') local eventid = ptoRequest[1][2][1][1] local empid = ptoRequest[1][2][1][2][2] local startDate = ptoRequest[1][2][1][2][4] local days = ptoRequest[1][2][1][2][6] if (( days > '0' ) and redis.call('SISMEMBER','used'..KEYS[1],empid)<1) then msg = 'PTO approved for '..days..' days' redis.call('XADD','X:results'..KEYS[1],'*','empid',empid,'startDate',startDate,'numDays',days,'manager',ARGV[1],'status','approved') redis.call('XACK','X:requests'..KEYS[1],'managers',eventid) redis.call('SADD','used'..KEYS[1],empid) end return msg" 1 {ot11} manager2
```
* and the evaluation of those PTO events by manager3 :
``` 
EVAL "local maxdays = 10 local msg = 'stuck during processing' local ptoRequest = redis.call('XREADGROUP','GROUP','managers',ARGV[1],'COUNT','1','STREAMS','X:requests'..KEYS[1],'>') local eventid = ptoRequest[1][2][1][1] local empid = ptoRequest[1][2][1][2][2] local startDate = ptoRequest[1][2][1][2][4] local days = ptoRequest[1][2][1][2][6] if (( days > '0' ) and redis.call('SISMEMBER','used'..KEYS[1],empid)<1) then msg = 'PTO approved for '..days..' days' redis.call('XADD','X:results'..KEYS[1],'*','empid',empid,'startDate',startDate,'numDays',days,'manager',ARGV[1],'status','approved') redis.call('XACK','X:requests'..KEYS[1],'managers',eventid) redis.call('SADD','used'..KEYS[1],empid) end return msg" 1 {ot11} manager3
```

* and the evaluation/processing of any pending PTO events by a supervisor

``` 
EVAL "local msg = 'abc' local stuckRequestID = redis.call('XPENDING','X:requests'..KEYS[1],'managers','-','+','1')[1][1] local ptoRequest = redis.call('XCLAIM','X:requests'..KEYS[1],'managers',ARGV[1],'0',stuckRequestID) local eventid = ptoRequest[1][1] local empid = ptoRequest[1][2][2] local startDate = ptoRequest[1][2][4] local days = ptoRequest[1][2][6] if (days < '1') then msg = 'request denied (PTO must be > 0 days)' end if redis.call('SISMEMBER','used'..KEYS[1],empid)>0 then msg = 'request denied  employee '..empid..' already requested PTO' end redis.call('XADD','X:results'..KEYS[1],'*','empid',empid,'startDate',startDate,'numDays',days,'manager', ARGV[1], 'status', 'denied', 'reason',msg) redis.call('XACK','X:requests'..KEYS[1],'managers',eventid) return msg" 1 {ot11} supervisor
```

*****
* The following is the code used to construct several timeseries keys - suitable for running in RedisInsight Workbench:
``` 
del zew:adult:{ot11}
del zew:child:{ot11}
del zew:pettingzoo:{ot11}
del zew:bonobolecture:{ot11}
del zew:gorillafeeding:{ot11}
del zew:3dmovie:{ot11}
del zew:snakefeeding:{ot11}

TS.CREATE zew:adult:{ot11} retention 0 LABELS data tickets attraction entrance isfree false audience adult author ot11
TS.CREATE zew:child:{ot11} retention 0 LABELS data tickets attraction entrance isfree false audience child author ot11
TS.CREATE zew:pettingzoo:{ot11} retention 0 LABELS data tickets attraction pettingzoo isfree false audience all author ot11
TS.CREATE zew:bonobolecture:{ot11} retention 0 LABELS data tickets attraction bonobolecture isfree false audience adult author ot11
TS.CREATE zew:gorillafeeding:{ot11} retention 0 LABELS data tickets attraction gorillafeeding isfree true audience all author ot11
TS.CREATE zew:3dmovie:{ot11} retention 0 LABELS data tickets attraction 3dmovie isfree false audience all author ot11
TS.CREATE zew:snakefeeding:{ot11} retention 0 LABELS data tickets attraction snakefeeding isfree true audience all author ot11

EVAL "for season = 1605525600000,1625613600000,2600000000 do for index = 1,365 do local vall = math.random(0,12) redis.call('TS.ADD', 'zew:adult:'..KEYS[1], ((index*21200000)+season), (vall+(index%9)) ) end end" 1 {ot11}
EVAL "for season = 1605525600000,1625613600000,2600000000 do for index = 1,365 do local vall = math.random(0,22) redis.call('TS.ADD', 'zew:child:'..KEYS[1], ((index*21200000)+season), (vall+(index%19)) ) end end" 1 {ot11}
EVAL "for season = 1605525600000,1625613600000,2600000000 do for index = 1,365 do local vall = math.random(0,9) redis.call('TS.ADD', 'zew:pettingzoo:'..KEYS[1], ((index*21200000)+season), (vall+(index%4)) ) end end" 1 {ot11}
EVAL "for season = 1605525600000,1625613600000,2600000000 do for index = 1,365 do local vall = math.random(0,2) redis.call('TS.ADD', 'zew:bonobolecture:'..KEYS[1], ((index*21200000)+season), (vall*(index%2)) ) end end" 1 {ot11}
EVAL "for season = 1605525600000,1625613600000,2600000000 do for index = 1,365 do local vall = math.random(0,4) redis.call('TS.ADD', 'zew:3dmovie:'..KEYS[1], ((index*21200000)+season), (vall*(index%2)) ) end end" 1 {ot11}
EVAL "for season = 1605525600000,1625613600000,2600000000 do for index = 1,365 do local vall = math.random(0,30) redis.call('TS.ADD','zew:gorillafeeding:'..KEYS[1], ((index*21200000)+season), (vall+(index%7)) ) end end" 1 {ot11}
EVAL "for season = 1605525600000,1625613600000,2600000000 do for index = 1,60 do local vall = math.random(0,30) redis.call('TS.ADD', 'zew:snakefeeding:'..KEYS[1], ((index*(21200000*6))+season), (vall*(index%2)) ) end end" 1 {ot11}
```

* This is a sample timeseries query that SUMS daily samples from all the keys that share the same label: data tickets

```
TS.MRANGE - + AGGREGATION SUM 86400000 FILTER data=tickets
```
