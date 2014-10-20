"""
-------------------------------------------------------
check_critical_file
a simple program that checks all the critical files in the directory
critical
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-10-16
-------------------------------------------------------
"""
import os
from os import listdir
from os.path import isfile, join
from graph import DalGraph
from pprint import PrettyPrinter
pp = PrettyPrinter(indent = 4)
mypath = os.path.join(os.getcwd(),"critical")
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
pp.pprint(onlyfiles)
result = {}
for file in onlyfiles:
    try:
        d = DalGraph(file=os.path.join(mypath,file))
        critical = d.is_critical()
        print(file,critical)
        result[file] = critical
    except:
        result[file] = "Invalid File"
pp.pprint(result)