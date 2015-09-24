"""
-------------------------------------------------------
find_dq_geq_4
A program to find if there exists a graph that all of its vertices
have degree 4 or more
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2015-09-24
-------------------------------------------------------
"""
from os import getcwd
from os.path import join
import os
from graph.helper import make_clique, make_cycle
from utility.file import File
from utility.generator import Generator
import logging

REQUIREMENT  = 3
logging.basicConfig(filename="hoang_conjecture.log", level=logging.INFO,
                            format='%(asctime)s %(message)s')
LOGGER = logging.getLogger(__name__)

REQUIREMENT = 4
DROPS  = 1
FORBIDDEN = [make_clique(4), make_cycle(4), make_clique(6), make_cycle(8)]
MYPATH = join(getcwd(), "special_graphs", "Non_adjacent")
GRAPH = make_cycle(5)

def go():
    for g in Generator(GRAPH, DROPS, FORBIDDEN, logger=LOGGER).iterate():
        if not check_condition_holds(g):
            f = File(MYPATH, G=g, logger=LOGGER, base="")
            fp = f.save()
            LOGGER.info("Found the special graph")
            print("Found the special graph")

def check_condition_holds(g):
    '''
    a function that checks if there are two non-adjacent vertices with d(v)<=3
    Parameters:
        g: the graph to check (networkx)
    Returns:
        held: True if held, False otherwise (boolean)
    '''
    held = False # assume no
    vertices = []
    for i in range(0, len(g.nodes())):
        if g.degree(i) <= REQUIREMENT:
            vertices.append(i)
    if non_adjacent(vertices, g):
        held = True
    return held

def non_adjacent(vertices, g):
    '''
    a function that checks if the list of vertices has a pair who is non
    adjacent
    Parameters:
        vertices: the list of vertices (list)
        g: the graph to check (networkx)
    Returns:
        condition: True if is a pair, False otherwise (boolean)
    '''
    condition = False
    if len(vertices) >= 4:
        condition = True
    i = 0
    while i < len(vertices) and not condition:
        j = i+1
        neighbors = g.neighbors(vertices[i])
        while j < len(vertices) and not condition:
            if vertices[j] not in neighbors:
                condition = True
            j += 1
        i += 1
    return condition

import unittest
class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCheckCondition(self):
        test = check_condition_holds(make_clique(5))
        expect = False
        self.assertEqual(test, expect)
        test = check_condition_holds(make_clique(3))
        expect = False
        self.assertEqual(test, expect)
        test = check_condition_holds(make_cycle(5))
        expect = True
        self.assertEqual(test, expect)
        
        
    def testNonAdjacent(self):
        self.assertEqual(non_adjacent([1,2], make_clique(4)), False)
        self.assertEqual(non_adjacent([1,2], make_cycle(4)), False)
        self.assertEqual(non_adjacent([1,3], make_cycle(4)), True)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()
    go()