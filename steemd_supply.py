from pandas import read_csv, Series
from numpy import zeros
'''
Check STEEM blockchain mining rate
'''

csvfile = "st.csv" # Source https://steemd.com
'''
head_block_number;time;virtual_supply
3741055;2016-08-02T21:00:21;119998513.14
3741103;2016-08-02T21:02:45;120000002.98
4169242;2016-08-17T19:44:12;133621732.467
4309722;2016-08-22T17:49:42;137950038.047
'''

chain = read_csv(csvfile, sep=';', header=0, parse_dates=[1])

def to_sec(Series):
    '''Convert Timedelta to seconds'''
    return Series.days * 24*60*60 + Series.seconds

items_size = chain["head_block_number"].size

chain["blocks_delta"] = Series(zeros(items_size))
chain["time_delta"]   = Series(zeros(items_size))
chain["steem_delta"]  = Series(zeros(items_size))

for item in range(items_size-1): # calculate values difference
    
    prev    = chain["head_block_number"][item]
    cur     = chain["head_block_number"][item+1]
    t_prev  = chain["time"][item]
    t_cur   = chain["time"][item+1]
    st_prev = chain["virtual_supply"][item]
    st_cur  = chain["virtual_supply"][item+1]
    
    chain["blocks_delta"][item+1] = cur - prev
    chain["time_delta"][item+1]   = t_cur - t_prev
    chain["steem_delta"][item+1]  = st_cur - st_prev

result = chain[chain["blocks_delta"] > 0] # remove zeros
result["sec_delta"]       = result["time_delta"].apply(to_sec)
result["sec_per_block"]   = result["sec_delta"] / result["blocks_delta"]
result["steem_per_block"] = result["steem_delta"] / result["blocks_delta"]
result["steem_per_sec"]   = result["steem_delta"] / result["sec_delta"]
result["steem_per_min"]   = result["steem_per_sec"] * 60

print result
