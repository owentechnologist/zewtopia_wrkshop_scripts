## showing several uses of JSON - adding a search index and example queries
``` 
JSON.SET zew:activities:gf $ '{"name": "Gorilla Feeding", "cost": 0.00, "times": ["0800", "1500", "2200"], "days": ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"],"location": "Gorilla House South", "responsible-party": {"name": "Duncan Mills", "contact": [{"phone": "715-876-5522"}, {"email": "dmills@zew.org"}]}}'
```

``` 
JSON.SET zew:activities:bl $ '{"name": "Bonobo Lecture", "cost": 10.00, "times": ["1100"], "days": ["Mon", "Thur"], "location": "Mammalian Lecture Theater","responsible-party": {"name": "Dr. Clarissa Gumali", "contact": [{"phone": "715-322-5992"}, {"email": "cgumali@zew.org"}]}}'
```

## Add a JSON-focused Search index:
``` 
FT.CREATE idx_zew_activities ON JSON PREFIX 1 zew:activities: SCHEMA $.name AS event_name TEXT PHONETIC dm:en $.cost AS cost NUMERIC $.times.* AS  times TAG  $.days.* AS days TAG $.location AS location TEXT PHONETIC dm:en $.responsible-party.name AS host_name TEXT PHONETIC dm:en
```

## Query JSON data using RediSearch and the JSON path:

``` 
FT.SEARCH idx_zew_activities @times:{08*} return 3 $.name $.times $.location
```

## Query JSON data using RediSearch and the attribute aliases:
``` 
FT.SEARCH idx_zew_activities @times:{11*} return 2 event_name location
```