import redis
from redis.client import Pipeline

# establish connection to your Redis instance:
myredis = redis.Redis( host='192.168.1.20', port=12000, decode_responses=True)
#myredis = redis.Redis( host='allindb.centralus.redisenterprise.cache.azure.net', port=10000, password='I4NCGKKUFmd6+VraDKrAOJrIF8TuN4bSsN+P2+2M96E=')

# Establish a Search index (we will query this a bit later)
try:
    myredis.execute_command(
    'FT.CREATE','idx_zew_revenue',
    'PREFIX','1','zew:revenue:',
    'SCHEMA','visitor_purchase_item_name','TEXT',
    'visitor_purchase_item_cost','NUMERIC','SORTABLE'
    )
except redis.exceptions.ResponseError as err:
    print(f'FT.CREATE ... {err} continuing on...')

# establish python-based stream workergroup:
# this group starts procesing at the beginning of the stream
try:
    #myredis.xgroup_destroy('zew:{batch2}:revenue:stream','group1')
    myredis.xgroup_create('zew:{batch2}:revenue:stream','group1','0-0')
except:
    print('XGROUP_CREATE ... group already exists .. continuing on...')    

# Have a single worker belonging to our group process 10 stream events
# using the > character tells redis to only deliver events unprocessed by this group: 
streamsdict = {'zew:{batch2}:revenue:stream': ">"}
for x in range(10):
    try:
        response = myredis.xreadgroup('group1','processorA',streams=streamsdict,count=1,noack=False)
        eventid = response[0][1][0][0] # the id assigned to the event when it was created
        astring = response[0][1][0][1].get('visitor_purchase') # compound string (attribute of the event)
        itemcost = astring.split(":").pop(0) # by programmer choice the cost and name are stored together
        itemname = astring.split(":").pop(1) # by programmer choice the cost and name are stored together
        # create a Hash record for the processed event:
        myredis.hset('zew:revenue:txid'+eventid,mapping={'visitor_purchase_item_name':itemname,'visitor_purchase_item_cost':itemcost})
        print(myredis.hgetall('zew:revenue:txid'+eventid))
    except:
        print('There are no more items in this stream to be processed by this group')
        length = myredis.execute_command('XLEN',"zew:{batch2}:revenue:stream")
        print(f"There are {length} items in the stream")

# use redis search to query the set of indexed Hashes:
sresult = myredis.execute_command(
'FT.AGGREGATE','idx_zew_revenue',
"@visitor_purchase_item_cost:[1 80]",
"GROUPBY", "1", "@visitor_purchase_item_name", 
"reduce", "SUM", "1", "@visitor_purchase_item_cost", 
"AS", "total_earned", 
"GROUPBY", "2", "@visitor_purchase_item_name", "@total_earned",
"SORTBY","2","@total_earned","DESC",
"LIMIT", "0", "100"
)

# display results to user:
print('\n Query Results - total dollar value by item sold:')
for c in range(len(sresult)):
    print(sresult[c])