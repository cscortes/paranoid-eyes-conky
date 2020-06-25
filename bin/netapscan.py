#!/usr/bin/env python
import subprocess as sp 

# -------------------------------------------------------------------------------------------------
# Access Point Scans:
# sample data:
# :ATT 2Ghz:Infra:7:270 Mbit/s:100:▂▄▆█:WPA1 WPA2
# *:ATT 5Ghz:Infra:149:405 Mbit/s:72:▂▄▆_:WPA1 WPA2
# IN-USE,BSSID,SSID,MODE,CHAN,RATE,SIGNAL,BARS,SECURITY 

fields = "IN-USE,SSID,CHAN,RATE,SIGNAL,BSSID"
cmd = "nmcli -t -f {} device wifi list".format(fields)
accessPoints = sp.check_output(cmd, shell=True).decode()

apsinfo = accessPoints.split("\n")
apsdata = [ap.split(":",5) for ap in apsinfo if len(ap.split(":")) > 5]
# remove ap without name
aps = [ap for ap in apsdata if len(ap[1].strip()) > 1]

if len(aps) > 0:
    print("${color4}ACCESS POINT (%d)" % (len(aps),))
    title =  "${color6}" 
    title += "{0:<26} {1:<3}".format("NAME"," CH")
    title += "${alignr}" 
    title += "{0:>10} {1:>3}".format("RATE","QL")
    print(title)

    linecount = 0
    for data in aps[:10]:
        line = "${color1}"
        if "*" in data[0]:
            line = "${color0}"
        line += "{1:<26.26} {2:>3}".format(*data)
        line += "${alignr}"
        line += "{3:>10} {4:>3}".format(*data)
        print(line)

else:
    print("${color4}NO ACCESS POINTS FOUND")