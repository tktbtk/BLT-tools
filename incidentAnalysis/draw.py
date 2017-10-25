import matplotlib
matplotlib.use("AGG")
from matplotlib import pyplot as plt
import numpy as np
import argparse
import pickle
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from matplotlib import gridspec
from datetime import datetime as dt
from datetime import timedelta as td

def mad(arr):
    arr = np.ma.array(arr).compressed() # should be faster to not use masked arrays.
    med = np.median(arr)
    return np.median(np.abs(arr - med))

def __roleFormatter(x, pos):
    if x == 0:
        return "duplicate announce"
    elif x == 1:
        return "path switching"
    elif x == 2:
        return "attribute change"
    elif x == 3:
        return "new prefix"
    elif x == 4:
        return "community change"
    elif x == 5:
        return "remove prefix"


parser = argparse.ArgumentParser()
parser.add_argument("pickle_file")
parser.add_argument("outfile")
parser.add_argument("-t", "--tags", help = "if you want to draw only several tags. ex) duplicate_announce,new_prefix")
parser.add_argument("-l", "--log", help = "if you want to draw as log scale.", action = "store_true")
args = parser.parse_args()

# get date
date = args.pickle_file.split("/")[-1][:8]

# pickle load
pkl = args.pickle_file
with open(pkl, "rb") as f:
    data = pickle.load(f)   ## data[tagName][time] = [value]


alert_flags = dict()
sorted_data = dict()
for tag in data.items():
    sorted_data[tag[0]] = np.array(sorted(tag[1].items(), key=lambda x: x[0]))[:,1]
    alert_flags[tag[0]] = 0

info = dict()
for sdata in sorted_data.items():
    # info = {tag_name : [mean, std, threshold]
    info[sdata[0]] = list()
    info[sdata[0]].append(np.median(sdata[1]))
    info[sdata[0]].append(mad(sdata[1]))
    info[sdata[0]].append(info[sdata[0]][0] + info[sdata[0]][1] * 5 * 1.4826)
    print sdata[0] + ": " + str(info[sdata[0]])

print ""
# figure format
fig = plt.figure()
gs = gridspec.GridSpec(3,1, height_ratios=[1,3,1])

# plot
movingValue = 30
ones = np.ones(movingValue)/movingValue
maximumY = 0
maximumY2 = 0
scatter = False
startTime = dt.strptime(date + "0000", "%Y%m%d%H%M")
endTime = dt.strptime(date + "2359", "%Y%m%d%H%M")

tag_array = list()
for tag in data.items():
    timeStamp = startTime
    x = list()
    y = list()
    for item in sorted(tag[1].items(), key=lambda x: x[0]):
        x.append(timeStamp)
        if timeStamp != item[0]:
            y.append(0)
        else:
            y.append(item[1])
        timeStamp += td(minutes=1)
    y = np.convolve(y, ones, "same").tolist()
    tag_array.append(y)
tag_np_array = np.array(tag_array)
total_messages = np.sum(tag_np_array, axis=0)
ax1 = fig.add_subplot(gs[0])
ax1.set_xticklabels([])
ax1.set_ylabel("the number of tag")
ax1.plot(x, total_messages)

ax2 = fig.add_subplot(gs[1])
ax2.set_xticklabels([])
ax2.set_ylabel("the number of tag")
tagColors = ['blue', 'turquoise', 'g','greenyellow', 'y', 'gold', 'coral', 'r', 'mediumvioletred', 'purple','indigo', 'rosybrown', 'cadetblue','k']

ax3 = fig.add_subplot(gs[2])
daysFmt = mdates.DateFormatter("%H")
ax3.xaxis.set_major_formatter(daysFmt)
ax3.set_xlabel("hour")
timeStamp = startTime
for (tag,C) in zip(data.items(), tagColors):
    if tag[0] == "prepending_add":
        continue
    if tag[0] == "prepending_remove":
        continue
    if tag[0] == "prepending_change":
        continue
    x = list()
    y = list()
    alert = list()
    while timeStamp < tag[1].keys()[0]:
        x.append(timeStamp)
        y.append(0)
        timeStamp += td(minutes=1)
    for item in sorted(tag[1].items(), key=lambda x: x[0]):
        y.append(item[1])
        x.append(item[0])
        timeStamp += td(minutes=1)

    if len(x) == 0 and len(y) == 0:
        continue
    if len(y) >= movingValue:
        y2 = np.convolve(y, ones, "same").tolist()
    if max(y) > maximumY:
        maximumY = max(y)
    if max(y2) > maximumY2:
        maximumY2 = max(y2)
    for (ts, value) in zip(x, y2):
        if alert_flags[tag[0]] == 0:
            if value > info[tag[0]][2]:
                print "alert! " + str(ts) + " " + tag[0] + " value: " + str(value) + " thr:" + str(info[tag[0]][2])
                alert.append(ts)
                alert_flags[tag[0]] = 1
        else:
            if value <= info[tag[0]][2]:
                print "fixed! " + str(ts) + " " + tag[0]
                alert_flags[tag[0]] = 0
            else:
                alert.append(ts)
    
    if scatter == True:
        ax2.scatter(x,y, s=20, c=C, marker='+', label=tag[0])
        ax2.plot(x,y2,c=C, alpha=0.3 ,linewidth=1)
    else:
        ax2.plot(x,y2,c=C, linewidth=1, label = tag[0])
    # log
    lgnd = ax2.legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0)
    if args.log == True:
        ax2.set_yscale("log")

    if len(alert) >= 1:
        if tag[0] == "duplicate_announce":
            y = [0] * len(alert)
        elif tag[0] == "path_switching":
            y = [1] * len(alert)
        elif tag[0] == "attribute_change":
            y = [2] * len(alert)
        elif tag[0] == "new_prefix":
            y = [3] * len(alert)
        elif tag[0] == "community_change":
            y = [4] * len(alert)
        elif tag[0] == "remove_prefix":
            y = [5] * len(alert)
        else:
            continue
        print len(alert)
        print len(y)
        ax3.plot(alert, y, "+" , c="r")
        
ax3.set_xlim(startTime, endTime)
ax3.yaxis.set_major_formatter(ticker.FuncFormatter(__roleFormatter))
if args.log == True:
    ax2.set_ylim(1, (maximumY*20/10))
else:
    ax2.set_ylim(0, (maximumY2*11/10))

plt.savefig(args.outfile, bbox_extra_artists=(lgnd,), bbox_inches='tight')
