#!/usr/bin/python
'''Get last day stats report and send over xmpp'''
import os
import sys
import time
import datetime
import pprint
import json

import redis
import yaml

#import subprocess
import jabber_send

CFG = yaml.load(open(os.environ["STEEM_CFG"]))
LOG = CFG['log']
PRE = CFG["prefix"]
LAST = CFG["last_info"]
BLOCKS = CFG["blocks_list"]

rdb = redis.Redis(host=CFG["redis_host"], port=CFG["redis_port"])
pp = pprint.PrettyPrinter(indent=4)

# Steemslot
block_head = json.loads( rdb.get(PRE + LAST).decode() ) # from last start
redis_key = "%s%s:%s" % (PRE, block_head["start_block"], block_head["end_block"])
print redis_key
read_stats = json.loads( rdb.get(redis_key).decode() )
#pp.pprint(read_stats)

day = datetime.date.today()
ystday = day - datetime.timedelta(days=1)
#print(ystday)
#print(time.strftime("%Y-%m-%d"))
#print(read_stats["dys_ts"][0:10])

if read_stats["dys_ts"][0:10] != str(ystday):
    jabber_send.send_xmpp("No steem flow data for yesterday")
    sys.exit(0)

template = '''
--------------------------------------
time_stamp          | block
--------------------+-----------------
%(dys_ts)s | %(br)i
%(last_block_time)s | %(block_number)i
--------------------+-----------------
(%(time_diff)s, %(dmin).1f minutes passed #%(block_count)i blocks)

total transfers: %(trans_count)i including:

------------------------------------------------------
           | spm   | STEEM    | $pm  | SBD     | tx
-----------+-------+----------+------+---------+------
->exchange | %(to_ex_steem_dmin).1f | %(to_ex_steem).1f | %(to_ex_sbd_dmin).1f | %(to_ex_sbd).1f | %(trans2ex)i
<-exchange | %(from_ex_steem_dmin).1f | %(from_ex_steem).1f | %(from_ex_sbd_dmin).1f | %(from_ex_sb).1f | %(trans4ex)i
-----------+-------+----------+------+---------+------
to/from exchange ratio: %(steem_ex_flow).2f:1 STEEM, %(sbd_ex_flow).2f:1 SBD
between_users: %(trans_u)i
between_exchanges: %(trans_e)i

vesting:  %(vesting_dmin).1f spm | %(vesting).1f STEEM | %(trans_vest)i
withdraw: %(withdraw_dmin).2f MVpm | %(withdraw).1f MV | %(trans_withd)i 

--------------------------------
         | $pm | SBD    | tx
---------+-----+--------+-------
to null  | %(to_null_sbd_dmin).1f | %(to_null_sbd).1f | %(trans_null)i
convert  | %(convert_sbd_dmin).1f | %(convert_sbd).1f | %(convert)i
---------+-----+--------+-------

feed base: %(feed_count)i (%(feed_base)s), each %(feed_time)s
'''
out = str(template % read_stats)

if out:
    '''
    p = subprocess.Popen(['./xsend.py', out],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
    output, err = p.communicate()
    print output, err
    '''
    jabber_send.send_xmpp(out)

print out

