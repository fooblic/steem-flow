import json

def get_redis(db):
    '''Get last parsed block number from redis'''
    head = json.loads( db.get("block_head").decode() )
    end = int(head["end_block"])
    return end
