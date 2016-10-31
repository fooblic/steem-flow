#!/usr/bin/env python3
'''
Initial variables values for steem_flow2.py
'''
import yaml
import pprint

usage = '''Error arg keys.
Usage: ./steem_flow2.py [options]
  options:
    --days <n>               parse blocks for <n> last days 
    --blocks <start> <end>   parse blocks numbers from <start> to <end>
    --redis                  parse blocks from last one in Redis DB 
'''

exchanges = ('bittrex', 'poloniex', 'blocktrades', 'openledger',
                 'hitbtc-exchange', 'hitbtc-payout', 'changelly',
                 'shapeshiftio')

oper_list = ('vote',
            'comment',
            'delete_comment',
            'custom_json',
            'limit_order_create',
            'limit_order_cancel',
            'account_create',
            'account_update',
            'account_witness_vote')

# My config
my_config = yaml.load(open("steemapi.yml"))
log = my_config['log']
pause = my_config['pause'] # seconds

prefix = my_config["prefix"]
last_info = my_config["last_info"]
blocks_list = my_config["blocks_list"]

pp = pprint.PrettyPrinter(indent=4)

block_count = 0

pow2_count = 0
pow2_block = 0 # average blocks
pow2_time = 0 

trans_count = 0

trans2ex = 0 # to exchange
to_ex_steem = 0
to_ex_sbd = 0

trans4ex = 0 # from exchange
from_ex_steem = 0
from_ex_sbd = 0

trans_u = 0 # between users
user_steem = 0
user_sbd = 0

trans_ex = 0 # between exchanges
ex_steem = 0
ex_sbd = 0

trans_null = 0 # to null
to_null_sbd = 0

trans_vest = 0 # transfer_to_vesting (power up)
vesting = 0
trans_withd = 0 # withdraw_vesting (power down)
withdraw = 0

set_withdraw_vesting_route = 0

convert = 0
convert_steem = 0
convert_sbd = 0

feed_count = 0
feed_time = 0
feed_base = 'N/A'

