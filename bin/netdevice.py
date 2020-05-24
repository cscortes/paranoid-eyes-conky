#!/usr/bin/env python
import subprocess as sp 

# -------------------------------------------------------------------------------------------------
# Find Active Connection
#
activeConnectionDevice = "NONE"

devices = sp.check_output("nmcli -t device", shell=True).decode()
for line in devices.split("\n"):
    data = tuple(line.split(":"))
    if len(data) > 3:
        if ":connected:" in line:
            activeConnectionDevice = data[0]

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
  
  