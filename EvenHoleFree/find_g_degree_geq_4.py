"""
-------------------------------------------------------
find_g_degree_geq_4
a program to check if a there is exists a graph G 
such that d(v) >=4 for every v in G
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2015-09-16
-------------------------------------------------------
"""
import sys
sys.path.append("..") # Adds higher directory to python modules path.

import unittest
import os
from os import getcwd, listdir
from os.path import isfile, join
from graph.helper import make_clique, make_cycle
from graph import DalGraph
from utility.generator import Generator
import logging
from utility.file import File
logging.basicConfig(filename="find_special_graph.log", level=logging.INFO,
                            format='%(asctime)s %(message)s')
LOGGER = logging.getLogger(__name__)

REQUIREMENT = 4
DROPS  = 4
MYPATH = join(getcwd(), "special_graphs")

def check_graph(drops, graph, forbidden):
    for g in Generator(graph, drops, forbidden, logger=LOGGER).iterate():
        if special_graph(g):
            f = File(MYPATH, G=g, logger=LOGGER, base="")
            fp = f.save()
            LOGGER.info("Found the special graph")
            print("Found the special graph")

def go():
    forbidden = [make_clique(4), make_cycle(4), make_clique(6), make_cycle(8)]
    onlyfiles = [ f for f in listdir(MYPATH) if isfile(join(MYPATH,f)) ]
    for f in onlyfiles:
        print("Working on:")
        print(f)
        g = File(MYPATH,file=f).load(f)
        check_graph(DROPS, g, forbidden)
    return

def special_graph(g):
    i = 0
    valid = True
    while i < len(g.nodes()) and valid:
        if g.degree(i) < REQUIREMENT:
            valid = False
        i += 1
    return valid


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSpecialGraph(self):
        self.assertEqual(special_graph(make_cycle(4)), False)
        self.assertEqual(special_graph(make_clique(5)), True)  

if __name__ == "__main__":
    go()