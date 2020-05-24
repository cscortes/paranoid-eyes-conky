#!/usr/bin/env python
import subprocess as sp 

# -------------------------------------------------------------------------------------------------
# Device Connection Mappings
#
print("${color4}NET CONNECTION")
devices = sp.check_output("nmcli -t device", shell=True).decode()
format_template = "{0:<16}{1:<14}{3:>16}\n"
deviceConnectionMap = "${color6}" + format_template.format("DEVICE","TYPE","","CONNECTION")

for line in devices.split("\n"):
    data = tuple(line.split(":"))
    # make sure we have least 4 items
    if len(data) > 3:
        if ":connected:" in line:
            deviceConnectionMap += "${color0}"
            activeConnectionDevice = data[0]
        else:
            deviceConnectionMap += "${color1}"
        deviceConnectionMap += format_template.format(*data)

print(deviceConnectionMap)

# -------------------------------------------------------------------------------------------------
# Device Details 
#
print("${color4}NET DEVICE DETAIL")
cmd = "nmcli -t device show {}".format(activeConnectionDevice)
deviceInfo = sp.check_output(cmd, shell=True).decode()

d = [("${color6}PROPERTY","VALUE")]
for line in deviceInfo.split("\n"):

    # highlight special information
    if [x for x in ("IP4.ADDRESS","GENERAL.HWADDR","IP6.ADDRESS") 
        if x in line]:
        line = "${color0}" + line 
    else:
        line = "${color1}" + line 

    # display only useful information
    datum = tuple(line.split(":",1))
    if len(datum) > 1:
        if   [x for x in ("GENERAL.MTU","GENERAL.HWADDR","GENERAL.TYPE") 
        if x in datum[0]]:
            d.append(datum)
        elif [x for x in ("IP4.ADDRESS","IP4.GATEWAY","IP4.ROUTE", "IP4.DNS")
        if x in datum[0]]:
            if ("IP4.ROUTE" in datum[0]):
                firstroute = datum[1].split(",",1)[0]
                d.append((datum[0], firstroute.replace("dst =","")))
            else:
                d.append(datum)
        elif [x for x in ("IP6.ADDRESS","IP6.GATEWAY")
        if x in datum[0]]:
            d.append(datum)

for datum in d:
    mesg = "{0:<24}{1:>30}".format(datum[0].strip(),datum[1].strip())
    print(mesg)
    #print( "${color1}" + datum[0] + " ${alignr}" + datum[1] )

# -------------------------------------------------------------------------------------------------
# Access Point Scans:
# sample data:
#  :ATT 2Ghz:Infra:7:270 Mbit/s:100:▂▄▆█:WPA1 WPA2
# *:ATT 5Ghz:Infra:149:405 Mbit/s:72:▂▄▆_:WPA1 WPA2
#
cmd = "nmcli -t device  wifi list"
accessPoints = sp.check_output(cmd, shell=True).decode()

print("\n${color4}ACCESS POINT")
title =  "${color6}" 
title += "{0:<15} {1:<3}".format("NAME"," CH")
title += "${alignr}" 
title += "{0:>10} {1:>3}".format("RATE","QL")
print(title)

for line in accessPoints.split("\n"):
    data = line.split(":")

    if len(data) > 5:
        line = "${color1}"
        line += "{1:<15} {3:>3}".format(*data)
        line += "${alignr}"
        line += "{4:>10} {5:>3}".format(*data)
        print(line)

