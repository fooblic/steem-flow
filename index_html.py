#!/usr/bin/env python3
'''
HTML templates for steem_flow.py
'''
html_head = '''<html><head>
<meta content="text/html; charset=utf-8" http-equiv="content-type">
<meta http-equiv="refresh" content="3" >
<title>STEEM transfer statistics</title></head>
<body>'''

html_end = '</body></html>'

html_block = '''
block_interval: %s
<br>
from_last_block: %s timestamp: %s
<br><br>
'''

html_1 = html_head + html_block + html_end

html_cur_pow = '''
current_block: %s (#%s) time_stamp: %s (%s, %s minutes passed)
<br><br>

pow2_count: %s (avg: %s blocks), each %s
<br><br>
'''

html_trans = '''
transfers: %s
<br>
to_exchange: %s (%s STEEM @ %s spm, %s SBD @ %s $pm) 
<br>
from_exchange: %s (%s STEEM @ %s spm, %s SBD @ %s $pm) 
<br>
to/from exchange ratio: %s:1 STEEM, %s:1 SBD
<br>
between_users: %s
<br>
between_exchanges: %s
<br>
to_null: %s (%s SBD) @ %s $pm
<br><br>

vesting: %s (%s STEEM) @ %s spm
<br>
new withdraw: %s (%s MV) @ %s VESTS per min
<br><br>
convert: %s (%s SBD) @ %s $pm
<br>
feed base: %s (%s), each %s
'''

html_all = html_head + html_block + html_cur_pow + html_trans + html_end
