#!/usr/bin/env python

import psutil
import time

# =================================================================================================
# NOTE: have to call the process_iter twice, because the first time, it returns NONE for cpu_percent
# Get all process information, that we need: name, pid, cpu_percent, memory_percent
# Sort via cpu percent, secondary key is memory percent
#
process_info = [i.info for i in psutil.process_iter(attrs=['cpu_percent']) ]
time.sleep(1)
process_info = [i.info for i in psutil.process_iter(attrs=['name','pid','cpu_percent','memory_percent']) ]
sorted_pinfo = sorted(process_info, reverse=True, key=lambda a: (a['cpu_percent'],a['memory_percent']))

# =================================================================================================
# print header information
print("${color4}    PID    CPU%   MEM%    PROCESS NAME")

# =================================================================================================
# each proc formatting, create a COLOR property, based on 0,50,80 for each process
#
TEMPLATE='''{p[COLOR]}{p[pid]:>8d} {p[cpu_percent]:>6.1f} {p[memory_percent]:>6.1f}    {p[name]}'''

for aprocess in sorted_pinfo[:6]:
	aprocess["COLOR"] = "${color1}"
	if (aprocess["cpu_percent"] >80):
		aprocess["COLOR"] = "${color8}"
	elif (aprocess["cpu_percent"] > 50):
		aprocess["COLOR"] = "${color6}"

	print(TEMPLATE.format(p=aprocess))

