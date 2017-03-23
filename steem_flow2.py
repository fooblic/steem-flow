#!/usr/bin/env python3
'''
Retrive and parse blocks from STEEM blockchain
Collect average STEEM flows intensity to Redis DB

Author: https://steemit.com/@fooblic
'''
import time
import sys
import dateutil.parser
import redis
import json

# My vars
from index_html2 import * # html templates
from flow_vars2 import *  # config, initial values
from get_redis import *   # aux functions

# get parameters from cli
try:
    arg_key = sys.argv[1]
except:
    print(usage)
    sys.exit(0)

try:
    rdb = redis.Redis(host="localhost", port=6379)
except:
    print("Error connection to Redis DB")
    sys.exit(0)

if arg_key == "--days":
    pdays = float(sys.argv[2]) # how many days to get stats
elif arg_key == "--blocks":
    start_block = int(sys.argv[2])
    end_block   = int(sys.argv[3])
elif arg_key == "--redis":
    start_block = get_redis(rdb, prefix + blocks_list) + 1
else:
    print(usage)
    sys.exit(0)

'''Python Library for Steem:
https://github.com/xeroc/python-steemlib'''
from steemapi.steemnoderpc import SteemNodeRPC
    
rpc = SteemNodeRPC(rpc_node)
config = rpc.get_config()
if log:
    pp.pprint(config)
    
block_interval = config["STEEMIT_BLOCK_INTERVAL"]
bpd = int(60 * 60 * 24 / block_interval) # blocks per day

props = rpc.get_dynamic_global_properties()
block_number = props['last_irreversible_block_num']
if arg_key == "--days":
    start_block = block_number - int(pdays * bpd)
    end_block   = block_number
elif arg_key == "--redis":
    end_block   = block_number
pp.pprint(props)

last_block_time = rpc.get_block(start_block)['timestamp']
time_last_block = dateutil.parser.parse(last_block_time)

block_head = {"block_interval": block_interval,
              "start_block": start_block,
              "last_block_time": last_block_time,
              "end_block": end_block}

rdb.set(prefix + last_info, json.dumps(block_head))


print('Start from #%s block at %s till block #%s ...' % (start_block, last_block_time, end_block) )

for br in range(start_block, end_block + 1):
    dys = rpc.get_block(br)
    dys_ts = dys['timestamp']
    time_dys = dateutil.parser.parse(dys_ts)
    time_diff = time_dys - time_last_block
    dmin = time_diff.days*24*60 + time_diff.seconds/60
    if dmin == 0: # no div 0
        dmin = pause * 60
    txs = dys['transactions']
    
    for tx in txs:

        for operation in tx['operations']:

            if (operation[0] not in oper_list):

                if log:
                    print(br)
                    pp.pprint(tx['operations'])
                    #pp.pprint(dys)
                    #print(dys['previous'], dys['timestamp'])

                if operation[0] == 'pow2':
                    pow2_count += 1
                    pow2_block = block_count / pow2_count
                    pow2_time = time_diff / pow2_count

                if operation[0] == 'transfer':
                    trans_count += 1
                    if operation[1]["from"] not in exchanges \
                      and operation[1]["to"] == 'null':
                      trans_null += 1
                      amount = operation[1]['amount'].split()
                      to_null_sbd += float(amount[0])

                    elif operation[1]["from"] not in exchanges \
                        and operation[1]["to"] in exchanges:
                        trans2ex += 1
                        amount = operation[1]['amount'].split()
                        if amount[1] == 'SBD':
                            to_ex_sbd += float(amount[0])
                        elif amount[1] == 'STEEM':
                            to_ex_steem += float(amount[0])
                        else:
                            print('\n!!! Unknown currency\n')

                    elif operation[1]["from"] in exchanges \
                        and operation[1]["to"] not in exchanges:
                        trans4ex += 1
                        amount = operation[1]['amount'].split()
                        if amount[1] == 'SBD':
                            from_ex_sbd += float(amount[0])
                        elif amount[1] == 'STEEM':
                            from_ex_steem += float(amount[0])
                        else:
                            print('\n!!! Unknown currency\n')

                    elif operation[1]["from"] not in exchanges \
                        and operation[1]["to"] not in exchanges:
                        trans_u += 1

                    elif operation[1]["from"] in exchanges \
                        and operation[1]["to"] in exchanges:
                        trans_ex += 1

                    else:
                        print('\n!!! Unknown transfer\n')

                if operation[0] == 'transfer_to_vesting':
                    trans_vest += 1
                    vesting += float(operation[1]['amount'].split()[0])

                if operation[0] == 'withdraw_vesting':
                    trans_withd += 1
                    withdraw += float(operation[1]['vesting_shares'].split()[0])
                        
                if operation[0] == 'feed_publish':
                    feed_count += 1
                    feed_time = time_diff / feed_count
                    feed_base = operation[1]['exchange_rate']['base']
                    
                if operation[0] == 'convert':
                    convert += 1
                    amount = operation[1]['amount'].split()
                    if amount[1] == 'STEEM':
                        convert_steem += float(amount[0])
                    if amount[1] == 'SBD':
                        convert_sbd += float(amount[0])
                    else:
                        print('\n!!! Unknown currency\n')

                if from_ex_steem > 0:
                    steem_ex_flow = to_ex_steem / from_ex_steem
                else:
                    steem_ex_flow = 0

                if from_ex_sbd > 0:
                    sbd_ex_flow = to_ex_sbd / from_ex_sbd
                else:
                    sbd_ex_flow = 0    

                block_stats = {"block_interval": block_interval,
                    "block_number": start_block,
                    "last_block_time": last_block_time,
                    
                    "br": br,
                    "block_count": block_count, 
                    "dys_ts": dys_ts,
                    "time_diff": str(time_diff),
                    "dmin": dmin,
                    
                    "pow2_count": pow2_count,
                    "pow2_block": pow2_block,
                    "pow2_time": str(pow2_time),
                    
                    "trans_count": trans_count, 
                    "trans2ex": trans2ex,
                    "to_ex_steem": to_ex_steem,
                    "to_ex_steem_dmin": to_ex_steem/dmin,
                    "to_ex_sbd": to_ex_sbd,
                    "to_ex_sbd_dmin": to_ex_sbd/dmin,
                    
                    "trans4ex": trans4ex,
                    "from_ex_steem": from_ex_steem,
                    "from_ex_steem_dmin": from_ex_steem/dmin,
                    "from_ex_sb": from_ex_sbd,
                    "from_ex_sbd_dmin": from_ex_sbd/dmin,

                    "steem_ex_flow": steem_ex_flow,
                    "sbd_ex_flow": sbd_ex_flow,
                    "trans_u": trans_u,
                    "trans_e": trans_ex,

                    "trans_null": trans_null,
                    "to_null_sbd": to_null_sbd,
                    "to_null_sbd_dmin": to_null_sbd/dmin,

                    "trans_vest": trans_vest,
                    "vesting": vesting,
                    "vesting_dmin": vesting/dmin,

                    "trans_withd": trans_withd,
                    "withdraw": withdraw/1000/1000,
                    "withdraw_dmin": withdraw/1000/1000/dmin,

                    "convert": convert,
                    "convert_sbd": convert_sbd,
                    "convert_sbd_dmin": convert_sbd/dmin,

                    "feed_count": feed_count,
                    "feed_base": feed_base,
                    "feed_time": str(feed_time)
                }

                redis_key = "%s%s:%s" % (prefix, start_block, end_block)
                rdb.set(redis_key , json.dumps(block_stats))
                
    block_count += 1
    time.sleep(pause)

rdb.zadd(prefix + blocks_list, redis_key, end_block)

print('Parsed %s blocks for %s from #%s to #%s' % (block_count, str(time_diff),
                                                     start_block, end_block) )
