'''
Some common functions for steem_flow2
'''
import json

def get_redis(db, list_name):
    '''Get last parsed block number from redis'''
    redis_key = db.zrange(list_name, -1 , -1)[0].decode() # last item
    end = db.zscore(list_name, redis_key)
    return int(end)

def get_list(db, list_name, start, stop):
    redis_keys = db.zrangebyscore(list_name, start, stop) # list in range
    
    return redis_keys

def get_slot_dates(db, key):
    '''Get start and stop date from redis record by given key'''
    record = json.loads(db.get(key).decode())
    start_date = record["last_block_time"]
    stop_date  = record["dys_ts"]

    return str(start_date + " - " +  stop_date)
