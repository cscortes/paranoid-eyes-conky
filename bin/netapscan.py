#!/usr/bin/env python
import subprocess as sp 

# -------------------------------------------------------------------------------------------------
# Access Point Scans:
# sample data:
# :ATT 2Ghz:Infra:7:270 Mbit/s:100:▂▄▆█:WPA1 WPA2
# *:ATT 5Ghz:Infra:149:405 Mbit/s:72:▂▄▆_:WPA1 WPA2
#
cmd = "nmcli -t device  wifi list"
accessPoints = sp.check_output(cmd, shell=True).decode()

aps = accessPoints.split("\n")
print("${color4}ACCESS POINT (%d)" % (len(aps),))
title =  "${color6}" 
title += "{0:<26} {1:<3}".format("NAME"," CH")
title += "${alignr}" 
title += "{0:>10} {1:>3}".format("RATE","QL")
print(title)

for line in aps[:10]:
    data = line.split(":")

    if len(data) > 5:
        line = "${color1}"
        if "*" in data[0]:
            line = "${color0}"
        line += "{1:<26.26} {3:>3}".format(*data)
        line += "${alignr}"
        line += "{4:>10} {5:>3}".format(*data)
        print(line)

# else:
#     print("${color4}NO ACCESS POINTS FOUND")