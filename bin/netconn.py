#!/usr/bin/env python
import subprocess as sp 

# -------------------------------------------------------------------------------------------------
# Device Connection Mappings
# sample data:
# wlp3s0:wifi:connected:Auto Cortes 5Ghz
# p2p-dev-wlp3s0:wifi-p2p:disconnected:
# enp2s0:ethernet:unavailable:
# lo:loopback:unmanaged:
#                
print("${color4}NET CONNECTION")
devices = sp.check_output("nmcli -t device", shell=True).decode()
format_template = "{0:<16}{1:<14}{3:>16}"
print("${color6}" + format_template.format("DEVICE","TYPE","","CONNECTION"))

for line in devices.split("\n"):
    deviceConnectionMap = ""
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