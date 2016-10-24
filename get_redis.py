import json

def get_redis(db):
    '''Get last parsed block number from redis'''
    redis_key = db.lindex("steem:chain", -1) # last item
    read_stats = json.loads( db.get(redis_key).decode() )
    end = int(read_stats["br"])
    return end
