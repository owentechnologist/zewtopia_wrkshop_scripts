### Showing several uses of JSON - adding a search index and example queries

### ZooEvents look like this:
``` 
{
	"times": [{
		"military": "0800",
		"civilian": "8 AM"
	}, {
		"military": "1500",
		"civilian": "3 PM"
	}, {
		"military": "2200",
		"civilian": "10 PM"
	}],
	"responsible-parties": {
		"number_of_contacts": 2,
		"hosts": [{
			"phone": "715-876-5522",
			"name": "Duncan Mills",
			"email": "dmilla@zew.org"
		}, {
			"phone": "815-336-5598",
			"name": "Xiria Andrus",
			"email": "xiriaa@zew.org"
		}]
	},
	"cost": 0,
	"name": "Gorilla Feeding",
	"days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
	"location": "Gorilla House South"
}
```

### Create 2 such events:

``` 
JSON.SET zew:activities:gf $ '{"name": "Gorilla Feeding", "cost": 0.00, "times": [{"military":"0800","civilian":"8 AM"},{"military": "1500","civilian": "3 PM"}], "days": ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"],"location": "Gorilla House South", "responsible-parties": {"number_of_contacts": 1,"hosts":[{"name": "Duncan Mills","phone": "715-876-5522", "email": "dmills@zew.org"}]}}'
```

``` 
JSON.SET zew:activities:bl $ '{"name": "Bonobo Lecture", "cost": 10.00, "times": [{"military":"1100","civilian":"11 AM"}], "days": ["Mon", "Thur"], "location": "Mammalian Lecture Theater","responsible-parties": {"number_of_contacts": 1,"hosts":[{"name": "Dr. Clarissa Gumali", "phone": "715-322-5992", "email": "cgumali@zew.org"}]}}'
```

### Add a JSON-focused Search index:
``` 
FT.CREATE idx_zew_activities ON JSON PREFIX 1 zew:activities: SCHEMA $.name AS event_name TEXT PHONETIC dm:en $.cost AS cost NUMERIC $.times[*].military AS times TAG $.days.* AS days TAG $.location AS location TEXT PHONETIC dm:en $.responsible-parties.hosts[*].name AS host_name TEXT PHONETIC dm:en
```

### Query JSON data using RediSearch and the JSON path:

``` 
FT.SEARCH idx_zew_activities @times:{08*} return 3 $.name $.times $.location
```

### Query JSON data using RediSearch and the attribute aliases:
``` 
FT.SEARCH idx_zew_activities @times:{11*} return 2 event_name location
```

#### NB: <em> A more involved Jedis/Java based JSON + Search example is available here:</em>
[https://github.com/owentechnologist/jsonZewSearch](https://github.com/owentechnologist/jsonZewSearch)
