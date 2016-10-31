'''
Some common functions for steem_flow2
'''
def get_redis(db, list_name):
    '''Get last parsed block number from redis'''
    redis_key = db.zrange(list_name, -1 , -1)[0].decode() # last item
    end = db.zscore(list_name, redis_key)
    return int(end)

def get_list(db, list_name, start, stop):
    redis_keys = db.zrangebyscore(list_name, start, stop) # list in range
    
    return redis_keys
