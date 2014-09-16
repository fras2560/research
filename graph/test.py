"""
-------------------------------------------------------
graph
unit tests for graph classes and functions
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-10
-------------------------------------------------------
"""
import unittest
import networkx as nx
from graph import DalGraph
from helper import make_cycle
class testDalGraph(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testHoleNumber(self):
        # test C3
        c3 = make_cycle(3)
        hole = DalGraph(c3).hole_number()
        self.assertEqual(hole, 3, "Hole Number on C3")
        # test C5
        c5 = make_cycle(5)
        hole = DalGraph(c5).hole_number()
        self.assertEqual(hole, 5, "Hole Number on C5")
        # test C8
        c8 = make_cycle(8)
        hole = DalGraph(c8).hole_number()
        self.assertEqual(hole, 8, "Hole Number on C8")
        # test K4
        k4 = nx.complete_graph(4)
        hole = DalGraph(k4).hole_number()
        self.assertEqual(hole, None, "Hole Number on K4")
        # test random graph
        rando = nx.barbell_graph(10, 10)
        hole = DalGraph(rando).hole_number()
        self.assertEqual(hole, None, "Hole Number on random graph")

    def testCliqueNumber(self):
        # test K3
        k3 = nx.complete_graph(3)
        clique = DalGraph(k3).clique_number()
        self.assertEqual(clique, 3, "Clique Number on K3")
        # test K5
        k5 = nx.complete_graph(5)
        clique = DalGraph(k5).clique_number()
        self.assertEqual(clique, 5, "Clique Number on K5")
        # test K8
        k8 = nx.complete_graph(8)
        clique = DalGraph(k8).clique_number()
        self.assertEqual(clique, 8, "Clique Number on K8")
        # test C4
        c4 = make_cycle(4)
        clique = DalGraph(c4).clique_number()
        self.assertEqual(clique, None, "Clique Number on C4")
        # test random graph
        rando = nx.barbell_graph(10, 10)
        clique = DalGraph(rando).clique_number()
        self.assertEqual(clique, None, "Clique Number on random graph")

    def testCheckSmallerCycle(self):
        c3 = make_cycle(3)
        g = DalGraph(c3)
        c = g.check_smaller_cycle([], 1, 0)
        self.assertEqual(c, [0, 1], "Failed the simple C2 case")
        c3 = make_cycle(3)
        g = DalGraph(c3)
        c = g.check_smaller_cycle([0], 0, 1)
        self.assertEqual(c, [0, 1], "Failed the simple C2 case")
        c5 = make_cycle(5)
        g = DalGraph(c5)
        c = g.check_smaller_cycle([0, 1, 2], 4, 3)
        self.assertEqual(c, [0, 1, 2, 3 , 4, 0], "Failed the simple C5 Case")
        c4 = make_cycle(4)
        g = DalGraph(c4)
        c = g.check_smaller_cycle([0, 1, 2], 0 ,3)
        self.assertEqual([], c, "Failed the simple C4 case")
        c5 = make_cycle(5)
        c5.add_edge(2, 4)
        g = DalGraph(c5)
        c = g.check_smaller_cycle([0, 1, 2], 4, 3)
        self.assertEqual([], c, "Failed to find back track node in C5 Case")
        c = g.check_smaller_cycle([2], 4, 3)
        self.assertEqual([], c, "Failed to find back track node in C5 Case")

    def testCycleNodes(self):
        g = DalGraph(make_cycle(3))
        c = g.cycle_nodes()
        self.assertEqual(c, [], "Cycle Nodes Failed: found cycle less than 3")
        g = DalGraph(make_cycle(5))
        c = g.cycle_nodes()
        self.assertEqual(c, [0, 1, 2, 3, 4 ,0], 
                         "Cycle Nodes Failed: did not find C5")
        c5 = make_cycle(5)
        c5.add_edge(2,4)
        g = DalGraph(c5)
        c = g.cycle_nodes()
        self.assertEqual(c, [], "Cycle Nodes Failed: did found non-induced C5")

    def testKColor(self):
        g = DalGraph(make_cycle(3))
        c = g.k_color()
        self.assertEqual(3, c, "KColor: K3 case")
        g = DalGraph(make_cycle(4))
        c = g.k_color()
        self.assertEqual(None, c, "KColor: C4 case")
        g = DalGraph(make_cycle(4))
