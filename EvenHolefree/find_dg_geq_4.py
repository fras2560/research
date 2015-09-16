"""
-------------------------------------------------------
find_dq_geq_4
A program to find if there exists a graph that all of its vertices
have degree 4 or more
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2015-09-15
-------------------------------------------------------
"""


import os
from os import listdir
from os.path import isfile, join
from graph import DalGraph
from pprint import PrettyPrinter
pp = PrettyPrinter(indent = 4)
from EmailHelper import send_email
def check_critical_file(mypath, logger):
    # mypath = os.path.join(os.getcwd(),"critical")
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    pp.pprint(onlyfiles)
    result = {}
    total = len(onlyfiles)
    index = 0
    print("Total Files: %d" % total)
    for file in onlyfiles:
        try:
            print("{0:.2%}".format(index / total))
            index += 1
            logger.info("Checking file %s" % file)
            d = DalGraph(file=os.path.join(mypath,file), logger=logger)
            critical = d.critical_aprox()
            logger.info("File %s is %r" %(file, critical))
            result[file] = critical
        except:
            result[file] = "Invalid File"
    pp.pprint(result)
    logger.info("Results:")
    logger.info("-----------------")
    for file, critical in result.items():
        logger.info("File %s is %r" %(file, critical))
    logger.info("-----------------")
    send_email(CRITICAL_MESSAGE, TO_ADDRESS)

import logging
if __name__ == "__main__":
    logging.basicConfig(filename="4-Critical.log", level=logging.INFO,
                            format='%(asctime)s %(message)s')
    logger = logging.getLogger(__name__)
    mypath = os.path.join(os.getcwd(),"5-Critical")
    check_critical_file(mypath, logger)

import unittest


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()