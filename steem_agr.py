#!/usr/bin/python3
'''
Get data from Redis and aggregate together slot's records 
'''
import sys
import redis
import json
import yaml
import pprint

from get_redis import * 

# config
my_config = yaml.load(open("steemapi.yml"))
log = my_config['log']
prefix = my_config["prefix"]
last_info = my_config["last_info"]
blocks_list = my_config["blocks_list"]

rdb = redis.Redis(host="localhost", port=6379)
pp = pprint.PrettyPrinter(indent=4)

# from cli
start_block = int(sys.argv[1])
end_block   = int(sys.argv[2])

slot_list = get_list(rdb, prefix + blocks_list, start_block, end_block)
#pp.pprint(slot_list)
for redis_key in slot_list:
    print(redis_key)
    read_stats = json.loads( rdb.get(redis_key).decode() )
    pp.pprint(read_stats)
