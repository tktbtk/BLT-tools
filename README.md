# BLT-tools
These tools are made as applications of BLT (https://github.com/romain-fontugne/BLT)
which can classify messages based on the proposed method and attach the labels to BGP messages.
You can detect routing anomalies easily using these tools.

## Example
In this section, we describe how to use BLT-tools using two examples.

### 1. Monitoring Internet-wide events
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

+ Then you can draw the figure running below command.
```bash:
python anomaly_detector.py ~/test/20170825_GoogleLeak/20170825_GoogleLeak.pkl
```
<img src="https://user-images.githubusercontent.com/20659074/34763516-d9584fca-f62e-11e7-83cd-66f1b32ad37a.jpg" width="480">

### 2. Monitoring local routing changes
Second example is an outage in Syria that coincide with national examination in that country on June 1st 2017.
Because this event is much smaller than that of Google or other big BGP event,
we should focus-on the country or other unit of network.
So, we prepared two grep tools.
One can grep for the prefixes in the country,
the other can grep for the AS.
In this example, we grep for the prefixes in Syria.


+ Run BLT to get messages with labels. (You can check the detail of BLT here https://github.com/romain-fontugne/BLT)
```bash:
python bltReader.py -v 4 -s 20170601  -f 20170601 -c route-views.linx -o ~/test/20170601_SyriaOutage/20170601_SyriaOutage.blt
```
+ Grep for Syria using the grep_country.py.
```bash:
python grep_country.py ~/test/20170601_SyriaOutage/20170601_SyriaOutage.blt SY > ~/test/20170601_SyriaOutage/20170601_SyriaOutage_SY.blt
```

+ Run convert_blt_to_pickle.py to get pickle file.
```bash:
python convert_blt_to_pickle.py ~/test/20170601_SyriaOutage/20170601_SyriaOutage_SY.blt
```

+ Then you can draw the figure running below command.
```bash:
python anomaly_detector.py ~/test/20170601_SyriaOutage/20170601_SyriaOutage_SY.pkl
```
<img src="https://user-images.githubusercontent.com/20659074/34763505-cfcd5338-f62e-11e7-829e-f9e402b103b4.jpg" width="480">
