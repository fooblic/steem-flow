#!/usr/bin/python3
'''
Get data from Pandas dataframe and aggregate together slot's records
Plot STEEM flow graphics daily/weekly/monthly
'''
import os
import datetime
import time
import pprint

import yaml
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from numpy import arange

pp = pprint.PrettyPrinter(indent=4)

# set font
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["font.size"] = 16

my_config = yaml.load(open("steemapi.yml"))
df = pd.read_pickle(my_config["pickle_file"])

TODAY = time.strftime("%y%m%d")
#img_path = my_config["img_path"] # to save plots
img_path = "img" + TODAY + "/"

steem_per_mvests = my_config["steem_per_mvests"] # from https://steemd.com/
print("steem_per_mvests: ", steem_per_mvests)

col = len(df.index)
print(col, " slots")

def get_sbd(Series):
    ''' remove "SBD" string'''
    val, sbd = Series.split()
    return float(val)

convert_steem_dmin = df["convert_sbd_dmin"]/df["feed_base"].map(get_sbd)
withdraw_steem_dmin = df["withdraw_dmin"] * steem_per_mvests

def get_week(Series):
    '''Get a week number of a year'''
    return datetime.datetime.strptime(Series, "%Y-%m-%dT%H:%M:%S").isocalendar()[1]

def get_month(Series):
    '''Get a month number of a year'''
    return datetime.datetime.strptime(Series, "%Y-%m-%dT%H:%M:%S").month

df["week"] = df["dys_ts"].map(get_week)
df["month"] = df["dys_ts"].map(get_month)
print(df, df.columns.values)

index_list = ["to_ex_steem_dmin",
           "to_ex_sbd_dmin",
           "from_ex_steem_dmin",
           "from_ex_sbd_dmin",
           "to_null_sbd_dmin",
           "convert_sbd_dmin",
           "convert_spm_dmin",
           "vesting_dmin",
           "withdraw_dmin",
           "withdraw_spm_dmin"]

monthes = set(df["month"])
monthly = pd.DataFrame(index = index_list, columns = list(monthes))
    
weeks = set(df["week"])
weekly = pd.DataFrame(index = index_list, columns = list(weeks))

def aggregate_data(col_name, set_in, df_out):

    for numb in set_in:
        df_agg = df[df[col_name] == numb]
        col_days = len(df_agg.index)

        agg_convert_steem_dmin  = df_agg["convert_sbd_dmin"]/df_agg["feed_base"].map(get_sbd)
        agg_withdraw_steem_dmin = df_agg["withdraw_dmin"] * steem_per_mvests

        df_out[numb] = pd.Series({"to_ex_steem_dmin":   df_agg["to_ex_steem_dmin"].sum()/col_days,
                      "to_ex_sbd_dmin":     df_agg["to_ex_sbd_dmin"].sum()/col_days,

                      "from_ex_steem_dmin": df_agg["from_ex_steem_dmin"].sum()/col_days,
                      "from_ex_sbd_dmin":   df_agg["from_ex_sbd_dmin"].sum()/col_days,

                      "to_null_sbd_dmin":   df_agg["to_null_sbd_dmin"].sum()/col_days,
                      "convert_sbd_dmin":   df_agg["convert_sbd_dmin"].sum()/col_days,
                      "convert_spm_dmin":   agg_convert_steem_dmin.sum()/col_days,

                      "vesting_dmin":       df_agg["vesting_dmin"].sum()/col_days,
                      "withdraw_dmin":      df_agg["withdraw_dmin"].sum()/col_days,
                      "withdraw_spm_dmin":  agg_withdraw_steem_dmin.sum()/col_days
        })
    return df_out

weekly_df = aggregate_data("week", weeks, weekly).T
monthly_df = aggregate_data("month", monthes, monthly).T
monthly_df.sort_index(inplace=True)

print(weekly_df)
print(monthly_df)

total = {"to_ex_steem_dmin":   df["to_ex_steem_dmin"].sum()/col,
         "to_ex_sbd_dmin":     df["to_ex_sbd_dmin"].sum()/col,
         
         "from_ex_steem_dmin": df["from_ex_steem_dmin"].sum()/col,
         "from_ex_sbd_dmin":   df["from_ex_sbd_dmin"].sum()/col,
 
         "to_null_sbd_dmin":   df["to_null_sbd_dmin"].sum()/col,
         "convert_sbd_dmin":   df["convert_sbd_dmin"].sum()/col,
         "convert_spm_dmin":   convert_steem_dmin.sum()/col,
         
         "vesting_dmin":       df["vesting_dmin"].sum()/col,
         "withdraw_dmin":      df["withdraw_dmin"].sum()/col,
         "withdraw_spm_dmin":  withdraw_steem_dmin.sum()/col
}
pp.pprint(total)

rate = {"rate_steem": total["to_ex_steem_dmin"] / total["from_ex_steem_dmin"],
        "rate_sbd":   total["to_ex_sbd_dmin"] / total["from_ex_sbd_dmin"],
        "rate_powering": total["withdraw_spm_dmin"] / total["vesting_dmin"]
}
pp.pprint(rate)

xtics = arange(col)

try:
    os.mkdir(img_path)
except:
    print("Could not create %s" % (img_path))
#os.mkdir(img_path)

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
plt.legend(loc = "upper right")
plt.xticks(xtics, df["dys_ts"], rotation = 90)
plt.title("STEEM flow rate")
plt.xlabel("Date")
plt.ylabel("STEEM per minute")
plt.autoscale(tight=True)
plt.subplots_adjust(bottom = 0.32)
plt.savefig(img_path + "daily_steem_ex.png")

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
plt.savefig(img_path + "daily_sbd_ex.png")

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
plt.savefig(img_path + "daily_flow_ratio.png")

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
plt.savefig(img_path + "daily_convert_sbd.png")

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
plt.savefig(img_path + "daily_sp.png")


################## Weekly/Monthly graphs
monthes_list = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", 
                "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]

def plot_pic(pic):
    #### 1 STEEM - exchange

    plt.figure(pic["num"])
    plt.bar(pic["xtics"] - 0.2, pic["df1"],
                width=0.4,
                color="blue",
                label=pic["x_legend"])
    plt.bar(pic["xtics"] + 0.2, pic["df2"],
                width=0.4,
                color="lightblue",
                label=pic["y_legend"])
    plt.legend(loc = "best")

    if "Monthly" in pic["title"]:
        x_ticks = []
        for mon in pic["df1"].index.values:
            x_ticks.append(monthes_list[mon - 1])
        plt.xticks(pic["xtics"], x_ticks)
    else:
        plt.xticks(pic["xtics"], pic["df1"].index.values)

    plt.title(pic["title"])
    plt.xlabel(pic["x_label"])
    plt.ylabel(pic["y_label"])
    plt.autoscale(tight=True)
    plt.subplots_adjust(bottom = pic["bottom"])
    plt.savefig(img_path + pic["fname"])

# STEEM flow rate
weekr  = arange( len( list( weekly_df.index.values )))
monthr = arange( len( list( monthly_df.index.values )))

pnum = 6
pic = {}
pic["title"]    = "Weekly STEEM flow rate"
pic["num"]      = pnum
pic["xtics"]    = weekr
pic["df1"]      = weekly_df["to_ex_steem_dmin"]
pic["df2"]      = weekly_df["from_ex_steem_dmin"]
pic["x_legend"] = "to exchanges"
pic["y_legend"] = "from exchanges"
pic["x_label"]  = "Week number"
pic["y_label"]  = "STEEM per minute"
pic["bottom"]   = 0.1
pic["fname"]    = "weekly_steem_ex.png"
print(pnum, pic["title"])
plot_pic(pic)

pnum += 1
pic = {}
pic["title"]    = "Monthly STEEM flow rate"
pic["num"]      = pnum
pic["xtics"]    = monthr
pic["df1"]      = monthly_df["to_ex_steem_dmin"]
pic["df2"]      = monthly_df["from_ex_steem_dmin"]
pic["x_legend"] = "to exchanges"
pic["y_legend"] = "from exchanges"
pic["x_label"]  = "Month"
pic["y_label"]  = "STEEM per minute"
pic["bottom"]   = 0.1
pic["fname"]    = "monthly_steem_ex.png"
print(pnum, pic["title"])
plot_pic(pic)

# SBD flow rate
pnum += 1
pic = {}
pic["title"]    = "Weekly SBD flow rate"
pic["num"]      = pnum
pic["xtics"]    = weekr
pic["df1"]      = weekly_df["to_ex_sbd_dmin"]
pic["df2"]      = weekly_df["from_ex_sbd_dmin"]
pic["x_legend"] = "to exchanges"
pic["y_legend"] = "from exchanges"
pic["x_label"]  = "Week number"
pic["y_label"]  = "SBD per minute"
pic["bottom"]   = 0.1
pic["fname"]    = "weekly_sbd_ex.png"
print(pnum, pic["title"])
plot_pic(pic)

pnum += 1
pic = {}
pic["title"]    = "Monthly SBD flow rate"
pic["num"]      = pnum
pic["xtics"]    = monthr
pic["df1"]      = monthly_df["to_ex_sbd_dmin"]
pic["df2"]      = monthly_df["from_ex_sbd_dmin"]
pic["x_legend"] = "to exchanges"
pic["y_legend"] = "from exchanges"
pic["x_label"]  = "Month"
pic["y_label"]  = "SBD per minute"
pic["bottom"]   = 0.1
pic["fname"]    = "monthly_sbd_ex.png"
print(pnum, pic["title"])
plot_pic(pic)

# To/From exchanges flow ratio
pnum += 1
pic = {}
pic["title"]    = "Weekly To/From exchanges flow ratio"
pic["num"]      = pnum
pic["xtics"]    = weekr
pic["df1"]      = (weekly_df["to_ex_steem_dmin"]/weekly_df["from_ex_steem_dmin"]).map(ratio)
pic["df2"]      = (weekly_df["to_ex_sbd_dmin"]/weekly_df["from_ex_sbd_dmin"]).map(ratio)
pic["x_legend"] = "STEEM to/from exchanges ratio"
pic["y_legend"] = "SBD to/from exchanges ratio"
pic["x_label"]  = "Week number"
pic["y_label"]  = "Ratio"
pic["bottom"]   = 0.1
pic["fname"]    = "weekly_flow_ratio.png"
print(pnum, pic["title"])
plot_pic(pic)

pnum += 1
pic = {}
pic["title"]    = "Monthly To/From exchanges flow ratio"
pic["num"]      = pnum
pic["xtics"]    = monthr
pic["df1"]      = (monthly_df["to_ex_steem_dmin"]/monthly_df["from_ex_steem_dmin"]).map(ratio)
pic["df2"]      = (monthly_df["to_ex_sbd_dmin"]/monthly_df["from_ex_sbd_dmin"]).map(ratio)
pic["x_legend"] = "STEEM to/from exchanges ratio"
pic["y_legend"] = "SBD to/from exchanges ratio"
pic["x_label"]  = "Month"
pic["y_label"]  = "Ratio"
pic["bottom"]   = 0.1
pic["fname"]    = "monthly_flow_ratio.png"
print(pnum, pic["title"])
plot_pic(pic)

# SBD convert
pnum += 1
pic = {}
pic["title"]    = "Weekly SBD convert"
pic["num"]      = pnum
pic["xtics"]    = weekr
pic["df1"]      = weekly_df["convert_sbd_dmin"]
pic["df2"]      = weekly_df["to_null_sbd_dmin"]
pic["x_legend"] = "convert"
pic["y_legend"] = "to null"
pic["x_label"]  = "Week number"
pic["y_label"]  = "SBD per minute"
pic["bottom"]   = 0.1
pic["fname"]    = "weekly_convert_sbd.png"
print(pnum, pic["title"])
plot_pic(pic)

pnum += 1
pic = {}
pic["title"]    = "Monthly SBD convert"
pic["num"]      = pnum
pic["xtics"]    = monthr
pic["df1"]      = monthly_df["convert_sbd_dmin"]
pic["df2"]      = monthly_df["to_null_sbd_dmin"]
pic["x_legend"] = "convert"
pic["y_legend"] = "to null"
pic["x_label"]  = "Month"
pic["y_label"]  = "SBD per minute"
pic["bottom"]   = 0.1
pic["fname"]    = "monthly_convert_sbd.png"
print(pnum, pic["title"])
plot_pic(pic)

# STEEM vesting/withdraw
pnum += 1
pic = {}
pic["title"]    = "Weekly STEEM vesting/withdraw"
pic["num"]      = pnum
pic["xtics"]    = weekr
pic["df1"]      = weekly_df["vesting_dmin"]
pic["df2"]      = weekly_df["withdraw_spm_dmin"]
pic["x_legend"] = "power up"
pic["y_legend"] = "power down"
pic["x_label"]  = "Week number"
pic["y_label"]  = "STEEM per minute"
pic["bottom"]   = 0.1
pic["fname"]    = "weekly_sp.png"
print(pnum, pic["title"])
plot_pic(pic)

pnum += 1
pic = {}
pic["title"]    = "Monthly STEEM vesting/withdraw"
pic["num"]      = pnum
pic["xtics"]    = monthr
pic["df1"]      = monthly_df["vesting_dmin"]
pic["df2"]      = monthly_df["withdraw_spm_dmin"]
pic["x_legend"] = "power up"
pic["y_legend"] = "power down"
pic["x_label"]  = "Month"
pic["y_label"]  = "STEEM per minute"
pic["bottom"]   = 0.1
pic["fname"]    = "monthly_sp.png"
print(pnum, pic["title"])
plot_pic(pic)

#plt.show()
