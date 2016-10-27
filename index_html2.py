#!/usr/bin/env python3
'''
HTML templates for steem_flow2.py
'''
html_head = '''<html><head>
<meta content="text/html; charset=utf-8" http-equiv="content-type">
<meta http-equiv="refresh" content="3" >
<title>STEEM transfer statistics</title></head>
<body>'''

html_end = '</body></html>'

html_block = '''
block_interval: %(block_interval)i
<br>
from_last_block: %(block_number)i timestamp: %(last_block_time)s
<br><br>
'''

html_1 = html_head + html_block + html_end

html_cur_pow = '''
parsed_block: %(br)i (#%(block_count)i) time_stamp: %(dys_ts)s (%(time_diff)s, %(dmin).1f minutes passed)
<br><br>

pow2_count: %(pow2_count)i (avg: %(pow2_block).1f blocks), each %(pow2_time)s
<br><br>
'''

html_trans = '''
total transfers: %(trans_count)i including:
<br>
to_exchange: %(trans2ex)i (%(to_ex_steem).1f STEEM @ %(to_ex_steem_dmin).1f spm, %(to_ex_sbd).1f SBD @ %(to_ex_sbd_dmin).1f $pm) 
<br>
from_exchange: %(trans4ex)i (%(from_ex_steem).1f STEEM @ %(from_ex_steem_dmin).1f spm, %(from_ex_sb).1f SBD @ %(from_ex_sbd_dmin).1f $pm) 
<br>
to/from exchange ratio: %(steem_ex_flow).2f:1 STEEM, %(sbd_ex_flow).2f:1 SBD
<br>
between_users: %(trans_u)i
<br>
between_exchanges: %(trans_e)i
<br>
to_null: %(trans_null)i (%(to_null_sbd).1f SBD) @ %(to_null_sbd_dmin).1f $pm
<br><br>

vesting: %(trans_vest)i (%(vesting).1f STEEM) @ %(vesting_dmin).1f spm
<br>
new withdraw: %(trans_withd)i (%(withdraw).1f MV) @ %(withdraw_dmin).2f MV per min
<br><br>
convert: %(convert)i (%(convert_sbd).1f SBD) @ %(convert_sbd_dmin).1f $pm
<br>
feed base: %(feed_count)i (%(feed_base)s), each %(feed_time)s
'''

html_all = html_head + html_block + html_cur_pow + html_trans + html_end

html_slots ='''<html><head>
<title>Steem flow 2</title></head>
<body>
<ul>
{% for item in items %}
  <li><a href="{{ http }}{{ item }}">{{ item }}</a></li>
{% endfor %}
</ul>
</body>
'''
