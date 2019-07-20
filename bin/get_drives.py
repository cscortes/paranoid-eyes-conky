#!/home/cscortes/.local/share/virtualenvs/.conky-dlbkzSpR/bin/python
import  subprocess

# ==========================================================================================
# Which types do you want to see
#
include_list = ["ext4", "vfat", "fuseblk"]

header="""${color4}HDD:"""
tmpl = """${color2}ME1${color1} ${alignr}${fs_used ME2} / ${fs_size ME2} ${fs_bar 10,100 ME2} """

out = subprocess.check_output(["cat", "/etc/mtab"] ).decode("utf-8")
lines = [line.strip() for line in out.split("\n") 
	if len(line.strip()) > 0 and line.strip()[0] != "#" and len(line.split()) > 2]

# -------------------------------------------------------------------------------------------
# print a commented line of debug data, only can see this if you run it on the command line
for line in lines:
	print("# (%s) %s" %  (line.split()[2],  line.strip()) )

splits = [line.split() for line in lines]

data = [ ( split[2], split[1] )
	for split in splits 
		if (split[2] in include_list) ]

print(header)
for ftype,mount in data:
	r1 = tmpl.replace("ME1", "(%s) %s" % (ftype,mount))
	r2 = r1.replace("ME2", mount)
	print(r2)

