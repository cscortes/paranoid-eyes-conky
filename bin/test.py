import re

pat = re.search( "(#@)\s+(\w+)\s+=", "#@ adsf =")
comment, varname = pat.groups()

