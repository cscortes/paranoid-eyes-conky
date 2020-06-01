#!/usr/bin/env python
import sys
import re

def doreplacments( vars, conf, conky ):
    data = []
    # replace all vars in config
    for line in conf:
        d = [ var for var in vars if var in line ] 
        if d:
            data.append(vars[d[0]])
        else:
            data.append(line)
    # append the rest of conky
    data += conky
    return data

def findreplacements( data ):
    replacements = {}

    for line in data:
        pat = re.search( "(#@)\s+(\w+)\s+=", line)
        if (pat):
            comment, varname = pat.groups()
            replacements[varname] = line.replace(comment,"")
    
    return replacements

def main():
    if len(sys.argv) < 4:
        Exception("Not enough arguments, need configfile and conkyfile to outconkyfile")

    configfname = sys.argv[1]
    conkyfname  = sys.argv[2]
    finalfname  = sys.argv[3]

    with open(configfname,"r") as configfo:
        configdata = configfo.readlines()

    with open(conkyfname, "r") as conkyfo:
        conkydata = conkyfo.readlines()

    replacements = findreplacements(conkydata)
    finaldata = doreplacments(replacements, configdata, conkydata)

    with open(finalfname, "w") as finalfo:
        finalfo.writelines(finaldata)

main()
