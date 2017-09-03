#!/usr/bin/env python3
'''
Tools to maintains steemslots db

Author: https://steemit.com/@fooblic
'''
import os
import sys
import json
import pprint as pp
import redis

import yaml

from get_redis import *   # aux functions

usage = '''Error arg key
Usage: ./steemslots.py [options]
  options:
    --remove <slot>                remove slot from Redis DB 
'''

# get parameters from cli
try:
    arg_key = sys.argv[1]
except:
    print(usage)
    sys.exit(0)

if arg_key == "--remove":
    slot = sys.argv[2]  # slot name to delete
else:
    print(usage)
    sys.exit(0)

# My config
CFG = yaml.load(open(os.environ["STEEM_CFG"]))
prefix =      CFG["prefix"]
blocks_list = CFG["blocks_list"]

try:
    rdb = redis.Redis(host="localhost", port=6379)
except:
    print("Error connection to Redis DB")
    sys.exit(0)

read_stats = json.loads( rdb.get(slot).decode() )
pp.pprint(read_stats)

reply = input("Confirm to delete slot (y/n):")

if reply == "y":
    slotlist = prefix + blocks_list
    del_slot(rdb, slot, slotlist)

    print("Done.")
