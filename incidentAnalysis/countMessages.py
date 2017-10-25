from subprocess import Popen, PIPE
import argparse
import sys
from datetime import datetime
import matplotlib
matplotlib.use("AGG")
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import threading
import time
import numpy as np
# arguments
# 1 : update_file
# 2 : output_file

def draw(x, y, outputFilePath):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(x,y)
    daysFmt = mdates.DateFormatter("%H")
    ax.xaxis.set_major_formatter(daysFmt)
    
    ax.set_xlabel("hour")
    ax.set_ylabel("the number of messages")
    plt.savefig(outputFilePath)

class Count(threading.Thread):
    def __init__(self, files, awk, threadNumber):
        super(Count, self).__init__()
        self.files = files
        if awk == None:
            self.awkMode = False
        else:
            self.awkMode = True
            self.awk = awk
        self.x = list()
        self.y = list()
        self.result = list()
        self.threadNumber = threadNumber

    def run(self):
        i = -1
        for update in self.files:
            p1 = Popen(["bgpdump", "-m", "-v", "-t", "change", update], stdout=PIPE, bufsize=-1)
            for line in p1.stdout: 
                res = line.split("|")
                if res[2] == "W":
                    zTd, zDt, zS, zOrig, zAS, zPfx  = res
                    if self.awkMode == True:
                        if self.awk not in res:
                            continue
                    
                elif res[2] == "A":
                    zTd, zDt, zS, zOrig, zAS, zPfx, sPath, zPro, zOr, z0, z1, z2, z3, z4, z5 = res
                    if self.awkMode == True:
                        if self.awk not in res and self.awk not in sPath:
                            continue
                    
                else:
                    continue
                timestamp = datetime.utcfromtimestamp(float(zDt)).strftime("%Y/%m/%d %H:%M")
                timestamp = datetime.strptime(timestamp, "%Y/%m/%d %H:%M")
                if int(timestamp.hour) < startHour: 
                    continue
                if int(timestamp.hour) > finishHour:
                    break
                if timestamp not in self.x:
                    self.x.append(timestamp)
                    i+=1
                    self.y.append(0)
                    print "[thread" + str(self.threadNumber) + "] : " + str(timestamp)
                self.y[i] += 1
        self.result = [self.x,self.y]

    def getResult(self):
        return self.result


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("outputFilePath")
    parser.add_argument("updates", nargs = "*")
    parser.add_argument("-s", "--startHour")
    parser.add_argument("-f", "--finishHour")
    parser.add_argument("-a", "--awk")

    args = parser.parse_args()

    numberThread = 8
    thread = list()
    threadResult = list()
    
    if args.startHour and args.finishHour:
        startHour = int(args.startHour)
        finishHour = int(args.finishHour)
    else:
        startHour = 0
        finishHour = 24
    x = list()
    y = list()

    hourFiles = dict()
    for update in args.updates:
        updateHour = int(update.split("/")[-1].split(".")[2][0:2])
        if updateHour < startHour:
            continue
        if updateHour > finishHour:
            break
        if updateHour not in hourFiles.keys():
            hourFiles[updateHour] = list()
        hourFiles[updateHour].append(update)
    hourFilesItems = sorted(hourFiles.items(), key=lambda x: x[0]) 
    print hourFiles.keys()
    j = 0
#        for (hour, updates) in zip(sorted(hourFiles.items(), key=lambda x: x[0])):
    while len(hourFilesItems) > 0:
        for i in range(numberThread):
            print ("len(hourFilesItems) : " + str(len(hourFilesItems)))
            if len(hourFilesItems) > 0:
                thread.append(Count(hourFilesItems.pop(0)[1], args.awk, i+numberThread*j))
                thread[i+numberThread*j].start()
                print("thread" + str(i+numberThread*j) + " started")
        numberRunThread = threading.enumerate()
        print len(numberRunThread)
        mainThread = threading.currentThread()
        while True:
            tlist= threading.enumerate()
            if len(tlist) < 2: break
            for t in tlist:
                if t is mainThread: continue
            time.sleep(1)
        for i in range(len(numberRunThread)-1):
            threadResult.append(thread[i+numberThread*j].getResult())
        j += 1
    print ("len(threadResult) : " + str(len(threadResult))) 
    

    for data in threadResult:
        x.extend(data[0])
        y.extend(data[1])

        ones = np.ones(10)/10
        y = np.convolve(y, ones, "same").tolist()

    draw(x,y,args.outputFilePath)    
