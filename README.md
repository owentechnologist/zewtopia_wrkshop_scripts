## This repository groups together various code and command examples that are designed to illuminate the  capabilities of Redis

It is expected that you will have a redis database running with the search and JSON modules loaded

It is also expected that you have access to a command shell that allows you to run Redis-cli and connect to your redis database.

## The goal is to provide an easy copy-paste solution and reference for the Redis-curious
## Examples include Lua scripts and redis-cli commands as well as some simple python code

# Welcome to Zewtopia!  <em>(a very fake zoo)</em>

### Get started by running the scripts found here:
[populate_zew_animals.lua.md](./populate_zew_animals.lua.md)

### Then you can expand to more data types and Search queries using:
[populate_additional_zew_entities.md](./populate_additional_zew_entities.md)

### You can look at some simple JSON data and searches here:
[add_json_entities_and_search.md](./add_json_entities_and_search.md)

#### NB: <em> A Jedis/Java based JSON + Search example is available here:</em>
[https://github.com/owentechnologist/jsonZewSearch](https://github.com/owentechnologist/jsonZewSearch)

### Then you can populate a Redis Stream with purchase events using:
[zew_purchases_stream_event_creator_lua.md](./zew_purchases_stream_event_creator_lua.md)

### To run the sample python code that starts up a worker to process stream events and produce searchable Hashes -  you will need to make sure you have python3 and that redis-py is installed in your environment
``` 
pip3 install redis[hiredis]
```
