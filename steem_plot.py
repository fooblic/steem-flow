#!/usr/bin/python3
'''
Get data from Pandas dataframe and aggregate together slot's records
Plot STEEM flow graphics 
'''
import yaml
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from numpy import arange

steem_per_mvests = 425. # from https://steemd.com/
print("steem_per_mvests: ", steem_per_mvests)

import pprint
pp = pprint.PrettyPrinter(indent=4)

# set font
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["font.size"] = 16

my_config = yaml.load(open("steemapi.yml"))
df = pd.read_pickle(my_config["pickle_file"])
#print(df, df.columns.values)

col = len(df.index)
print(col, " slots")

def get_sbd(Series):
    ''' remove "SBD" string'''
    val, sbd = Series.split()
    return float(val)

convert_steem_dmin = df["convert_sbd_dmin"]/df["feed_base"].map(get_sbd)
withdraw_steem_dmin = df["withdraw_dmin"] * steem_per_mvests

total = {"to_ex_steem_dmin": df["to_ex_steem_dmin"].sum()/col,
         "to_ex_sbd_dmin":   df["to_ex_sbd_dmin"].sum()/col,
         #"to_ex_steem": df["to_ex_steem"].sum()/col,
         #"to_ex_sbd":   df["to_ex_sbd"].sum()/col,
         
         "from_ex_steem_dmin": df["from_ex_steem_dmin"].sum()/col,
         "from_ex_sbd_dmin":   df["from_ex_sbd_dmin"].sum()/col,
         #"from_ex_steem": df["from_ex_steem"].sum()/col,
         #"from_ex_sb": df["from_ex_sb"].sum()/col,

         #"steem_ex_flow": df["steem_ex_flow"].sum()/col,
         #"sbd_ex_flow": df["sbd_ex_flow"].sum()/col,
         
         "to_null_sbd_dmin":  df["to_null_sbd_dmin"].sum()/col,
         "convert_sbd_dmin":  df["convert_sbd_dmin"].sum()/col,
         "convert_spm_dmin:": convert_steem_dmin.sum()/col,
         
         "vesting_dmin":      df["vesting_dmin"].sum()/col,
         "withdraw_dmin":     df["withdraw_dmin"].sum()/col,
         "withdraw_spm_dmin": withdraw_steem_dmin.sum()/col
}
pp.pprint(total)

rate = {"rate_steem": total["to_ex_steem_dmin"] / total["from_ex_steem_dmin"],
        "rate_sbd":   total["to_ex_sbd_dmin"] / total["from_ex_sbd_dmin"],
        "rate_powering": total["withdraw_spm_dmin"] / total["vesting_dmin"]
}
pp.pprint(rate)

xtics = arange(col)

#### 1 STEEM - exchange
plt.figure(1)
plt.bar(xtics-0.2, df["to_ex_steem_dmin"],
            width=0.4,
            color="blue",
            label="to exchanges")
plt.bar(xtics+0.2, df["from_ex_steem_dmin"],
            width=0.4,
            color="lightblue",
            label="from exchanges")
plt.legend(loc = "upper left")
plt.xticks(xtics, df["dys_ts"], rotation = 90)
plt.title("STEEM flow rate")
plt.xlabel("Date")
plt.ylabel("STEEM per minute")
plt.autoscale(tight=True)
plt.subplots_adjust(bottom = 0.32)
plt.savefig("steem_ex.png")

#### 2 SBD - exchange
plt.figure(2)
plt.bar(xtics-0.2, df["to_ex_sbd_dmin"],
            width=0.4,
            color="blue",
            label="to exchanges")
plt.bar(xtics+0.2, df["from_ex_sbd_dmin"],
            width=0.4,
            color="lightblue",
            label="from exchanges")
plt.legend(loc = "best")
plt.xticks(xtics, df["dys_ts"], rotation = 90)
plt.title("SBD flow rate")
plt.xlabel("Date")
plt.ylabel("SBD per minute")
plt.autoscale(tight=True)
plt.subplots_adjust(bottom = 0.32)
plt.savefig("sbd_ex.png")

#### 3 Ratio
def ratio(Series):
    if Series < 1:
        Series = (-1) / Series
    return Series

plt.figure(3)
plt.bar(xtics-0.2, df["steem_ex_flow"].map(ratio),
            width=0.4,
            color="blue",
            label="STEEM to/from exchanges ratio")
plt.bar(xtics+0.2, df["sbd_ex_flow"].map(ratio),
            width=0.4,
            color="lightblue",
            label="SBD to/from exchanges ratio")
#plt.plot([-0.2,len(df.index)], [1,1], "r--")
#plt.plot([-0.2,len(df.index)], [-1,-1], "r--")
plt.legend(loc = "best")
plt.xticks(xtics, df["dys_ts"], rotation = 90)
plt.title("To/From exchanges flow ratio")
plt.xlabel("Date")
plt.ylabel("Ratio")
plt.autoscale(tight=True)
plt.subplots_adjust(bottom = 0.32)
plt.savefig("flow_ratio.png")


#### 4 Convert
plt.figure(4)
plt.bar(xtics-0.2, df["convert_sbd_dmin"],
            width=0.4,
            color="blue",
            label="Convert")
plt.bar(xtics+0.2, df["to_null_sbd_dmin"],
            width=0.4,
            color="lightblue",
            label="To null")
plt.legend(loc = "best")
plt.xticks(xtics, df["dys_ts"], rotation = 90)
plt.title("SBD convert")
plt.xlabel("Date")
plt.ylabel("SBD per minute")
plt.autoscale(tight=True)
plt.subplots_adjust(bottom = 0.32)
plt.savefig("convert_sbd.png")


#### 5 Vesting
plt.figure(5)
plt.bar(xtics-0.2, df["vesting_dmin"],
            width=0.4,
            color="blue",
            label="power up")
plt.bar(xtics+0.2, withdraw_steem_dmin,
            width=0.4,
            color="lightblue",
            label="power down")
plt.legend(loc = "best")
plt.xticks(xtics, df["dys_ts"], rotation = 90)
plt.title("STEEM vesting/withdraw")
plt.xlabel("Date")
plt.ylabel("STEEM per minute")
plt.autoscale(tight=True)
plt.subplots_adjust(bottom = 0.32)
plt.savefig("steem_power.png")

#plt.show()
