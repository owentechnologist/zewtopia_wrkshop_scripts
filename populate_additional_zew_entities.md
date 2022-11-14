## It is expected that you have already populated Redis with animal Hashes using  
[populate_zew_animals.lua.md](./populate_zew_animals.lua.md)
### The following snippets are examples of redis commands to create data in Redis
#### Note that you run the example commands inside an active redis-cli shell:

#### Adding a few buildings to our Zew:
``` 
HSET zew:building1 current_gps_location '117.14955,32.73209' role 'Primate Training Center' contact_phone '832-777-5555' contact_name 'Front Desk' species 'Gorilla Monkey Chimpanzee Bonobo'
```
```
HSET zew:building2 current_gps_location '117.14803,32.73259' role 'Marsupial Training Center' contact_phone '832-677-5555' contact_name 'Front Desk' species 'Kangaroo Opossum Wombat Koala'
```
```
HSET zew:building3 current_gps_location '117.1299,32.73311' role 'Administrative Offices' contact_phone '899-223-2155' contact_name 'Martha Seales'
```

#### Adding a few trainers to our Zew:

```
HSET zew:trainer:nadin1 days_in_zoo 1020 name 'Nadin Huyt' species 'Kangaroo' search_set_rank 1 status hired role trainer current_gps_location '117.14803,32.73259' contact_phone '722-766-2425' contact_name 'Mrs Huyt' description 'Nadin is an excellent trainer with several years experience'
```

```
HSET zew:trainer:isaac1 days_in_zoo 23 name 'Isaac Asimov' species 'Gorilla' search_set_rank 1 status pending role trainer current_gps_location '117.14955,32.73209' contact_phone '654-877-6543' contact_name 'Isaac' description 'Isaac is a new trainer who has been volunteering to get more experience.  We expect him to be hired after another 60 days experience'
```

#### Adding tenure classification data to our Zew:

```
HSET zew:tenure:bonobo:new days_in_zoo_start 0 days_in_zoo_end 20 species bonobo description 'Newly arrived Bonobos have a tendency towards extreme behaviors and high-energy output' tenure_class 'NEW'
```

```
HSET zew:tenure:bonobo:settled days_in_zoo_start 21 days_in_zoo_end 200 species bonobo description 'Settled Bonobos form social bonds with others and begin adapting to the zoo environment' tenure_class 'SETTLED'
```

```
HSET zew:tenure:bonobo:enduring days_in_zoo_start 201 days_in_zoo_end 30000 species bonobo description 'Enduring Bonobos show signs of weariness and psychological distress, often accompanied by persistent physical health issues' tenure_class 'ENDURING'
```

## Now that we have additional data types that are related to our 'Zew' let us expand our search index to include them:
``` 
FT.CREATE idx_all_zew PREFIX 1 "zew:" SCHEMA name TEXT PHONETIC dm:en NOSTEM species TAG dob NUMERIC SORTABLE gender TAG known_disorders TEXT PHONETIC dm:en NOSTEM days_in_zoo NUMERIC SORTABLE current_gps_location GEO SORTABLE status TEXT PHONETIC dm:en role TAG contact_phone TAG contact_name TEXT NOSTEM days_in_zoo_start NUMERIC days_in_zoo_end NUMERIC
```

## remember our synonyms:

```
FT.SYNUPDATE idx_all_zew "violence_symptoms" "bruise" "injury" "wound" "scrape" "scratch" "lacerations" "trauma"
```

## remap our search index alias to use this new expanded index:
(in case you don't already have an alias you could just create one now:)
``` 
FT.ALIASADD idxa_zew idx_all_zew
```
Alternatively, you can remap one previously created:
``` 
FT.ALIASUPDATE idxa_zew idx_all_zew
```

## Some example Queries:

### This query finds the animals and employed trainers working within 50 meters of a known building’s location.  (note the use of the NOT pending status allows for results from other entities that do not have that field at all)

This is a kind of geo-spatial and species join because multiple entities share a common geo-spatial range and species. 
```
FT.SEARCH idxa_zew "@species:{Kan*} @current_gps_location:[117.14803,32.73259, 50 m] -@known_disorders:('non*') -@status:(pending)" RETURN 2 role name SORTBY role DESC
```

### This query finds the animals and trainers working within 150 meters of a known building’s location and returns the matching_members_count of how many trainers, animals and buildings related to the particular species exist.

This is a kind of geo-spatial and species join because multiple entities share a common geo-spatial range and species.
``` 
FT.AGGREGATE idxa_zew "@species:{Kan*} @current_gps_location:[117.14803,32.73259, 150 m] -@status:(pending)" GROUPBY 4 @species @role @contact_phone @contact_name REDUCE COUNT 0 AS matching_members_count SORTBY 2 @matching_members_count ASC
```

### Find the tenure category for a bonobo that has 797 days_in_zoo using a range-query: 
This returns results of the Tenure class for the bonobo with the specified number of days in zoo.  If you include a matching bonobo animal name in the OR clause, that bonobo information will be confirmed (returned) as well. 
<em>(range-queries like this can be useful when sequential ids or IPAddresses or measures of time can be grouped together)</em>
```
FT.SEARCH idxa_zew "(@days_in_zoo_start:[-inf 797] @days_in_zoo_end:[ 797 +inf] @species:{Bon*}) | @name:('Chess*') " return 3 days_in_zoo description tenure_class LIMIT 0 2
```

How would you find all the injured Gorillas?