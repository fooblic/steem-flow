
def get_redis(db):
    '''Get last parsed block number from redis'''
    redis_key = db.zrange("steem:blocks", -1 , -1)[0].decode() # last item
    end = db.zscore("steem:blocks", redis_key)
    return int(end)

