#!/usr/bin/env python

import psutil
idx = 0

# =====================================================================================
# Calculate number of CPUs
cpunum = psutil.cpu_count()
print("${alignc}${color2}CORES: %d" % cpunum)

# =====================================================================================
# create template strings for Left and Right CPU bars
#
LEFT_TEMPLATE = """${color2}#IDX#:\
${if_match ${cpu cpu#IDX#} < 50} ${color1}\
${else}${if_match ${cpu cpu#IDX#} < 80} ${color6}${else} ${color8}${endif}${endif}\
${cpubar cpu#IDX# 10,} ${color1}${cpu cpu#IDX#}%  """

RIGHT_TEMPLATE = """${alignr}${cpu cpu#IDX#}% ${if_match ${cpu cpu#IDX#} < 50}${color1}\
${else}${if_match ${cpu cpu#IDX#} < 80}${color6}${else}${color8}${endif}${endif}\
${cpubar cpu#IDX# 10,}${color2} :#IDX#"""

# =====================================================================================
# generate outputs for left and right CPUs bar
#
while idx < cpunum:
	idx += 1
	if (idx <= cpunum):
		print(LEFT_TEMPLATE.replace("#IDX#","{:02}".format(idx)), end="")

	idx += 1
	if (idx <= cpunum):
		print(RIGHT_TEMPLATE.replace("#IDX#","{:02}".format(idx)))
	else:
		print("")

import json
import subprocess as sp 

cmd = "sensors -u"
sensorinfo = sp.check_output(cmd, shell=True).decode()

# for line in sensorinfo.split("\n"):
# 	print("# " + line)

import re
coretempdata = re.findall("""Core\s(\d+).+?input:\s(\d+).+?crit:\s(\d+).+?alarm""",sensorinfo,flags=re.M | re.I | re.S)

print("")
for core in coretempdata:
	tempcolor = "${color1}"
	if int(core[1]) > (.70 * int(core[2])):
		tempcolor = "${color6}"
	if int(core[1]) > (.90 * int(core[2])):
		tempcolor = "${color8}"

	cpumsg = "${color1}" +"CPU {0:>2} TEMP: ".format(*core)
	cpumsg = cpumsg + tempcolor  + "{1:>3}".format(*core) 
	cpumsg = cpumsg + "/{2:>3} C".format(*core)
	print(cpumsg)