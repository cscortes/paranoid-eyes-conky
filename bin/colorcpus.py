#!/home/cscortes/.local/share/virtualenvs/.conky-dlbkzSpR/bin/python

# previously, we had this code:
# ${color2}CORE1: ${colorcpu1}${cpubar cpu1 10,} ${color1}${cpu cpu1}% $alignr${cpu cpu2}% ${color1}${cpubar cpu2 10,}${color2} :CORE2
# ${color2}CORE3: ${color1}${cpubar cpu3 10,} ${color1}${cpu cpu3}% $alignr${cpu cpu4}% ${color1}${cpubar cpu4 10,}${color2} :CORE4

idx = 0
cpunum = 4

print("${color2}CORES: %d" % cpunum);
# print("${color2}CORE1: ${color8}${cpubar cpu1 10,} ${color1}${cpu cpu1}% $alignr${cpu cpu2}% ${color1}${cpubar cpu2 10,}${color2} :CORE2")

LEFT_TEMPLATE = """${color2}CORE#IDX#:\
${if_match ${cpu cpu#IDX#} < 30} ${color1}\
${else}${if_match ${cpu cpu#IDX#} < 80} ${color6}${else} ${color8}${endif}${endif}\
${cpubar cpu#IDX# 10,} ${color1}${cpu cpu#IDX#}%  """

RIGHT_TEMPLATE = """${alignr}${cpu cpu#IDX#}% ${if_match ${cpu cpu#IDX#} < 30}${color1}\
${else}${if_match ${cpu cpu#IDX#} < 80}${color6}${else}${color8}${endif}${endif}\
${cpubar cpu#IDX# 10,}${color2} :CORE#IDX#"""

while idx < cpunum:
	idx += 1
	if (idx <= cpunum):
		print(LEFT_TEMPLATE.replace("#IDX#",str(idx)), end="")

	idx += 1
	if (idx <= cpunum):
		print(RIGHT_TEMPLATE.replace("#IDX#",str(idx)))
	else:
		print("")
