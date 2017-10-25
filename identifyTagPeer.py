import matplotlib
matplotlib.use("AGG")
from matplotlib import pyplot as plt
import sys

bltFile = sys.argv[1]
tag = sys.argv[2]

f = open(bltFile, "r")

numberTags = dict()
for line in f:
    line = line.split("\n")[0]
    message = line.split("#")[0]
    tags = line.split(" #")[1:]

    if tag not in tags:
        continue


    res = message.split("|")

    if res[2] == 'W':
        zTd, zDt, zS, zOrig, zAS, zPfx  = res
        
    elif res[2] == 'A':
        zTd, zDt, zS, zOrig, zAS, zPfx, sPath, zPro, zOr, z0, z1, z2, z3, z4, z5 = res
    else:
        continue

    if zOrig not in numberTags.keys():
        numberTags[zOrig] = 0
    numberTags[zOrig] += 1


x = list()
y = list()
ticks = list()

values = sorted(numberTags.items(), key=lambda x : x[1], reverse=True)
i=0
for value in values:
    x.append(i)
    i+=1
    ticks.append(value[0])
    y.append(value[1])
plt.bar(x,y)
plt.savefig("test")

for (x1, y1) in zip(ticks,y):
    print x1 + " : " + str(y1) 
