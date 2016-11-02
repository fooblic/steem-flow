#!/usr/bin/python3
'''
Get data from Pandas dataframe and aggregate together slot's records
Plot STEEM flow graphics 
'''
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from numpy import arange

# set font
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["font.size"] = 16

df = pd.read_pickle("store.pkl")
print(df, df.columns.values)

xtics = arange(len(df.index))

#### 1
plt.figure(1)
plt.bar(xtics-0.2, df["to_ex_steem_dmin"],
            width=0.4,
            color="blue",
            label="spm to exchanges")
plt.bar(xtics+0.2, df["from_ex_steem_dmin"],
            width=0.4,
            color="lightblue",
            label="spm from exchanges")
plt.legend()
plt.xticks(xtics, df["dys_ts"], rotation = 90)
plt.title("STEEM flow rate")
plt.xlabel("Date")
plt.ylabel("STEEM per minute")
plt.autoscale(tight=True)
plt.subplots_adjust(bottom = 0.32)
plt.savefig("steem_ex.png")

#### 2
plt.figure(2)
plt.bar(xtics-0.2, df["to_ex_sbd_dmin"],
            width=0.4,
            color="blue",
            label="$pm to exchanges")
plt.bar(xtics+0.2, df["from_ex_sbd_dmin"],
            width=0.4,
            color="lightblue",
            label="$pm from exchanges")
plt.legend()
plt.xticks(xtics, df["dys_ts"], rotation = 90)
plt.title("SBD flow rate")
plt.xlabel("Date")
plt.ylabel("SBD per minute")
plt.autoscale(tight=True)
plt.subplots_adjust(bottom = 0.32)
plt.savefig("sbd_ex.png")

#### 3
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
plt.legend()
plt.xticks(xtics, df["dys_ts"], rotation = 90)
plt.title("To/From exchanges flow ratio")
plt.xlabel("Date")
plt.ylabel("Ratio")
plt.autoscale(tight=True)
plt.subplots_adjust(bottom = 0.32)
plt.savefig("flow_ratio.png")

plt.show()
