'''
Created on Oct 14, 2015

@author: Dallas
'''
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from graph.helper import make_cycle, make_kite, make_clique, make_wheel
from utility.file import File
from graph import DalGraph
import os
from utility.generator import Generator
from EvenHoleFree.helper import critical_cycle 
import logging
from pprint import PrettyPrinter
pp = PrettyPrinter(indent = 4)

FORBIDDEN =  [make_kite(),
              make_cycle(4),
              make_cycle(6),
              make_cycle(8),
              make_cycle(5),
              make_wheel(6)
              ]
BASE = "C5"
DIRECTORY=os.path.join(os.getcwd(), "Critical-graphs", BASE)
STARTING = make_cycle(5)
logging.basicConfig(filename=BASE+"finding_critical.log", level=logging.INFO,
                            format='%(asctime)s %(message)s')
LOGGER = logging.getLogger(__name__)
DROPS = 5

def go():
    gen = Generator(STARTING, DROPS, FORBIDDEN, logger=LOGGER)
    total = gen.total_graphs()
    i = 0
    for g in gen.iterate():
        i +=1 
        if i % 1000 == 0:
            print("Finished %d of %d" %(i, total))
        if DalGraph(g, logger=LOGGER).critical_aprox():
            f = File(DIRECTORY,G=g).save()
            if f is not None:
                print("Found a critical graph")
    print("Done checked %d" % i)
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
    go()
