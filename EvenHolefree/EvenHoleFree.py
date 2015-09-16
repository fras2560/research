'''
Created on Sep 10, 2015

@author: Dallas
'''
from networkx.algorithms import graph_clique_number
from networkx import complement
from graph.helper import make_cycle
from graph.container import induced_subgraph
def even_hole_free(G):
    i_set = graph_clique_number(complement(G))
    free = True
    i = 4
    while i <= i_set * 2 and free:
        g = make_cycle(i)
        if induced_subgraph(G, g):
            free = False
        i += 2
    return free

def odd_hole_free(G):
    i_set = graph_clique_number(complement(G))
    free = True
    i = 5
    while i <= i_set * 2 + 1 and free:
        g = make_cycle(i)
        if induced_subgraph(G, g):
            free = False
        i += 2
    return free

import unittest
class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testEvenHoleFree(self):
        g = make_cycle(4)
        self.assertEqual(even_hole_free(g), False)
        g = make_cycle(5)
        self.assertEqual(even_hole_free(g), True)
        g = make_cycle(10)
        self.assertEqual(even_hole_free(g), False)

    def testOddHoleFree(self):
        g = make_cycle(4)
        self.assertEqual(odd_hole_free(g), True)
        g = make_cycle(5)
        self.assertEqual(odd_hole_free(g), False)
        g = make_cycle(10)
        self.assertEqual(odd_hole_free(g), True)
        g = make_cycle(11)
        self.assertEqual(odd_hole_free(g), False)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()