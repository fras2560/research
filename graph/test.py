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