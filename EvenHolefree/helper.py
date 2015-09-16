'''
Created on Sep 16, 2015

@author: Dallas
'''
import sys
sys.path.append("..") # Adds higher directory to python modules path.

import networkx as nx
from graph.helper import make_cycle
from graph import DalGraph

def critical_cycle(n):
    g = make_cycle(n)
    v1 = n
    v2 = n+1
    g.add_node(v1)
    g.add_node(v2)
    for i in range(0, n // 2 + 1):
        g.add_edge(i, v1)
        g.add_edge(n-i-1, v2)
    return g

import unittest
class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testCriticalCycle(self):
        g = critical_cycle(5)
        nodes = [0, 1, 2, 3, 4, 5, 6]
        edges =  [(0, 1), (0, 4), (0, 5), (1, 2), (1, 5),
                  (2, 3), (2, 5), (2, 6), (3, 4), (3, 6), (4, 6)]
        self.assertEqual(nodes, g.nodes())
        self.assertEqual(edges, g.edges())
        self.assertEqual(DalGraph(graph=g).is_critical(),True)

        # the long test
#         g = critical_cycle(9)
#         nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#         edges =  [(0, 8), (0, 1), (0, 9), (1, 9), (1, 2), (2, 3), (2, 9),
#                   (3, 9), (3, 4), (4, 9), (4, 10), (4, 5), (5, 10), (5, 6),
#                   (6, 10), (6, 7), (7, 8), (7, 10), (8, 10)]
#         print(g.nodes())
#         print(g.edges())
#         self.assertEqual(nodes, g.nodes())
#         self.assertEqual(edges, g.edges())
#         self.assertEqual(DalGraph(graph=g).is_critical(),True)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()