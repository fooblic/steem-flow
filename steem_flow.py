#!/usr/bin/env python3
import pprint
import time
import sys
import dateutil.parser
import yaml

from steemapi.steemnoderpc import SteemNodeRPC

# My vars
from index_html import *
from flow_vars import *

# My config
my_config = yaml.load(open("steemapi.yml"))
log = my_config['log']
index_file = my_config['index_file']

rpc = SteemNodeRPC('ws://node.steem.ws')
config = rpc.get_config()
block_interval = config["STEEMIT_BLOCK_INTERVAL"]

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(config)

props = rpc.get_dynamic_global_properties()
block_number = props['last_irreversible_block_num']
pp.pprint(props)

last_block_time = rpc.get_block(block_number)['timestamp']
time_last_block = dateutil.parser.parse(last_block_time)
#pp.pprint(dys)

oper_list = ('vote',
            'comment',
            'delete_comment',
            'custom_json',
            'limit_order_create',
            'limit_order_cancel',
            'account_create',
            'account_update',
            'account_witness_vote')

exchanges = ('bittrex', 'poloniex', 'blocktrades', 'openledger',
                 'hitbtc-exchange', 'hitbtc-payout', 'changelly')

br = block_number

print('Start at block %s ...' % block_number)

with open('index.html', 'w') as fl:
      fl.write(html_1 % (block_interval, block_number, last_block_time) )

while True:
    dys = rpc.get_block(br)
    time_dys = dateutil.parser.parse(dys['timestamp'])
    time_diff = time_dys - time_last_block
    dmin = time_diff.days*24*60 + time_diff.seconds/60
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
                            print('\n!!! Unknown currency !!!\n')

                    elif operation[1]["from"] in exchanges \
                        and operation[1]["to"] not in exchanges:
                        trans4ex += 1
                        amount = operation[1]['amount'].split()
                        if amount[1] == 'SBD':
                            from_ex_sbd += float(amount[0])
                        elif amount[1] == 'STEEM':
                            from_ex_steem += float(amount[0])
                        else:
                            print('\n!!! Unknown currency !!!\n')

                    elif operation[1]["from"] not in exchanges \
                        and operation[1]["to"] not in exchanges:
                        trans_u += 1

                    elif operation[1]["from"] in exchanges \
                        and operation[1]["to"] in exchanges:
                        trans_ex += 1

                    else:
                        print('\n!!!!!!!!! Unknown transfer !!!!!!!!!!\n')

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
                        print('\n!!! Unknown currency !!!\n')

                if from_ex_steem > 0:
                    steem_ex_flow = to_ex_steem / from_ex_steem
                else:
                    steem_ex_flow = 0

                if from_ex_sbd > 0:
                    sbd_ex_flow = to_ex_sbd / from_ex_sbd
                else:
                    sbd_ex_flow = 0    
                        
                out = html_all % (
                    block_interval,
                    block_number, last_block_time,
                    br, block_count, 
                    dys['timestamp'], time_diff, round(dmin, 1),
                    pow2_count, round(pow2_block, 1), pow2_time,
                    trans_count, 
                    trans2ex, round(to_ex_steem,1), round(to_ex_steem/dmin,1),
                    round(to_ex_sbd,1), round(to_ex_sbd/dmin,1),
                    trans4ex, round(from_ex_steem,1), round(from_ex_steem/dmin,1),
                    round(from_ex_sbd,1), round(from_ex_sbd/dmin,1),
                    round(steem_ex_flow,2), round(sbd_ex_flow,2),
                    trans_u, trans_ex,
                    trans_null, round(to_null_sbd,1), round(to_null_sbd/dmin,1),
                    trans_vest, round(vesting,1), round(vesting/dmin,1),
                    trans_withd, round(withdraw/1000/1000,1), round(withdraw/dmin,1),
                    convert, round(convert_sbd,1), round(convert_sbd/dmin,1),
                    feed_count, feed_base, feed_time
                )
                
                with open(index_file, 'w') as fl:
                    fl.write(out)
    br += 1
    block_count += 1
    time.sleep(block_interval)
