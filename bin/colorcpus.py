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
