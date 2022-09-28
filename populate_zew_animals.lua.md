### The Following LUA SCRIPTS INITIALIZE 3000 fake zoo (Zewtopia) animals  ####
### THEY SHOULD BE RUN IN the ORDER they appear below TO KEEP THINGS PREDICTABLE ###

* create the species and store them in a SET: 
```
EVAL "do redis.call('SADD',KEYS[1],'Lion') redis.call('SADD',KEYS[1],'Tiger') redis.call('SADD',KEYS[1],'Elephant') redis.call('SADD',KEYS[1],'Giant Panda') redis.call('SADD',KEYS[1],'Gorilla') redis.call('SADD',KEYS[1],'Giraffe') redis.call('SADD',KEYS[1],'Polar Bear') redis.call('SADD',KEYS[1],'Hippo') redis.call('SADD',KEYS[1],'Cheeta') redis.call('SADD',KEYS[1],'Zebra') redis.call('SADD',KEYS[1],'Meerkat') redis.call('SADD',KEYS[1],'Penguin') redis.call('SADD',KEYS[1],'Kangaroo') redis.call('SADD',KEYS[1],'Flamingo') redis.call('SADD',KEYS[1],'Koala') redis.call('SADD',KEYS[1],'Chimpanzee') redis.call('SADD',KEYS[1],'Llama') redis.call('SADD',KEYS[1],'Green Anaconda') redis.call('SADD',KEYS[1],'Hyena') redis.call('SADD',KEYS[1],'Bonobo') redis.call('SADD',KEYS[1],'Alligator') redis.call('SADD',KEYS[1],'Orangutan') end" 1 zew:{batch1}:species
```
* create some disorders and store them in a SET:
```
EVAL "do redis.call('SADD',KEYS[1],'chronic gastroenteritis') redis.call('SADD',KEYS[1],'acute gastroenteritis') redis.call('SADD',KEYS[1],'enteric parasites') redis.call('SADD',KEYS[1],'bite wound') redis.call('SADD',KEYS[1],'gore wound') redis.call('SADD',KEYS[1],'various lacerations') redis.call('SADD',KEYS[1],'bacterial abscess') redis.call('SADD',KEYS[1],'dystocia') redis.call('SADD',KEYS[1],'ingestion of foreign body') redis.call('SADD',KEYS[1],'osteoarthritis') redis.call('SADD',KEYS[1],'bacterial pneumonia') redis.call('SADD',KEYS[1],'tooth rot') redis.call('SADD',KEYS[1],'oral trauma') redis.call('SADD',KEYS[1],'digestive ulcer') redis.call('SADD',KEYS[1],'diabetis insipidus') end" 1 zew:{batch1}:disorders
```
* create some names and store them in a SET:
```
EVAL "do redis.call('SADD',KEYS[1],'Giggly') redis.call('SADD',KEYS[1],'Charmer') redis.call('SADD',KEYS[1],'Hungry') redis.call('SADD',KEYS[1],'Biter') redis.call('SADD',KEYS[1],'Noisy') redis.call('SADD',KEYS[1],'Chess') redis.call('SADD',KEYS[1],'Fluffy') redis.call('SADD',KEYS[1],'Logan') redis.call('SADD',KEYS[1],'Lover') redis.call('SADD',KEYS[1],'September') redis.call('SADD',KEYS[1],'Scrappy') redis.call('SADD',KEYS[1],'Juicy') redis.call('SADD',KEYS[1],'Lock') redis.call('SADD',KEYS[1],'Pat') redis.call('SADD',KEYS[1],'Roman') redis.call('SADD',KEYS[1],'Bobby') redis.call('SADD',KEYS[1],'Archer') redis.call('SADD',KEYS[1],'Hunter') redis.call('SADD',KEYS[1],'Cutsie') redis.call('SADD',KEYS[1],'Nasty') redis.call('SADD',KEYS[1],'Young') redis.call('SADD',KEYS[1],'Old') redis.call('SADD',KEYS[1],'Bashful') redis.call('SADD',KEYS[1],'Sweet') redis.call('SADD',KEYS[1],'Charity') redis.call('SADD',KEYS[1],'Rescue') redis.call('SADD',KEYS[1],'Glutten') redis.call('SADD',KEYS[1],'Brown') redis.call('SADD',KEYS[1],'Sam') redis.call('SADD',KEYS[1],'Red') redis.call('SADD',KEYS[1],'Blue') redis.call('SADD',KEYS[1],'Brooklyn') redis.call('SADD',KEYS[1],'California') redis.call('SADD',KEYS[1],'Paris') redis.call('SADD',KEYS[1],'Barrel') redis.call('SADD',KEYS[1],'Angel') redis.call('SADD',KEYS[1],'Devil') redis.call('SADD',KEYS[1],'Sleepy') redis.call('SADD',KEYS[1],'Sneezy') redis.call('SADD',KEYS[1],'Doc') end" 1 zew:{batch1}:names
```

* Create 3000 hash entries of animals using the 3 sets created above as random options
```
EVAL "for index = 1,3000 do local nums = '123456789' local alphs = redis.call('SRANDMEMBER', KEYS[4])..'aBcDeFgHiJkLmNoPqRsTuVwXyZ' local days = math.random(1,800) redis.call('HSET', KEYS[1] .. index,'species','' ..  redis.call('SRANDMEMBER', KEYS[2]),'name',redis.call('SRANDMEMBER', KEYS[4]) .. ' ' .. redis.call('SRANDMEMBER', KEYS[4]) ..' '.. index ,'gender', index %3 == 0 and 'male' or 'female' ,'known_disorders',index %3 == 0 and 'none reported' or redis.call('SRANDMEMBER', KEYS[3]),'days_in_zoo', days,'current_gps_location', '117.14'..math.random(800,1000).. ',32.73'.. math.random(0,900), 'dob',(redis.call('time')[1]-(days*(86400*math.random(1,8)))),'docid',index ..''.. math.random(1,800)..index .. string.sub(alphs,math.random(3,7),math.random(8,12)) .. math.random(1,800) .. '-41'.. math.random(1,800)..index .. string.sub(nums,math.random(1,4),math.random(5,9)) ..'-b749-'.. math.random(1,800)..index .. string.sub(alphs,math.random(4,9),math.random(10,14))) end" 4 zew:{batch1}:animal: zew:{batch1}:species zew:{batch1}:disorders zew:{batch1}:names
```

* Create a search index that will enable redis search queries:
``` 
 FT.CREATE idx_zew PREFIX 1 "zew:" SCHEMA name TEXT PHONETIC dm:en species TAG dob NUMERIC SORTABLE gender TAG known_disorders TEXT PHONETIC dm:en days_in_zoo NUMERIC SORTABLE current_gps_location GEO SORTABLE
```

* Add an alias for the search index to allow for remapping of queries to alternate indexes:
``` 
 FT.ALIASADD idxa_zew idx_zew
```

* Test a simple Search query:

``` 
FT.search idxa_zew "@name:bloo" return 1 name LIMIT 0 3
```

## YOU CAN STOP NOW ##

### DO NOT EXECUTE BELOW SCRIPT UNLESS YOU WANT TO CLEAN UP (REMOVE) THE DATA CREATED that uses the matching prefix: 
You can change the prefix used as the final argument to clean up any keys you have in your redis DB 
* (note that all targeted keys need to live in the same shard)


```
EVAL "local cursor = 0 local keyNum = 0 repeat local res = redis.call('scan',cursor,'MATCH',KEYS[1]..'*') if(res ~= nil and #res>=0) then cursor = tonumber(res[1]) local ks = res[2] if(ks ~= nil and #ks>0) then for i=1,#ks,1 do local key = tostring(ks[i]) redis.call('UNLINK',key) end keyNum = keyNum + #ks end end until( cursor <= 0 ) return keyNum" 1 zew:{batch1}:animal:*
```