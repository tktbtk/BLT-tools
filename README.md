# BLT-tools
These tools are made as applications of BLT (https://github.com/romain-fontugne/BLT)
which can classify messages based on the proposed method and attach the labels to BGP messages.
You can detect routing anomalies easily using these tools.

## Example
In this chapter, we describe how to use BLT-tools using one example.

On August 25th 2017 around 3:22 UTC, Google (AS15169) leaks over 150k routes for small prefixes that were presumably used for their internal traffic engineering.
This kind of incident is called "Route-Leak".
You can catch this incident using our anomaly-detector.

+ Run BLT to get messages with labels. (You can check the detail of BLT here https://github.com/romain-fontugne/BLT)
```bash:
python bltReader.py -v 4 -s 20170825  -f 20170826 -c route-views.linx -o ~/test/20170825_GoogleLeak/20170825_GoogleLeak.blt
```

+ Run convert_blt_to_pickle.py to get pickle file.
```bash:
python convert_blt_to_pickle.py ~/test/20170825_GoogleLeak/20170825_GoogleLeak.blt
```

+ Then you can draw the figure run below command.
```bash:
python anomaly_detector.py ~/test/20170825_GoogleLeak/20170825_GoogleLeak.pkl
```
