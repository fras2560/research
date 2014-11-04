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
from helper import make_cycle, make_wheel, join, make_claw, make_co_claw

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
        g = DalGraph(make_wheel(6))
        c = g.k_color()
        self.assertEqual(4, c, "KColor: W6 case")
        c5 = make_cycle(5)
        c5_2 = make_cycle(5)
        c = join(c5,c5_2)
        g = DalGraph(c)
        c = g.k_color()
        self.assertEqual(c, 6, "KColor: C5 joined with a C5")

    def testUnionNeighbors(self):
        g = DalGraph(make_claw())
        result = g.union_neighbors([0])
        expect = [1, 2, 3]
        self.assertEqual(result, expect)
        g._g.add_node(4)
        g._g.add_edge(3, 4)
        result =g.union_neighbors([4, 2])
        expect = [3, 0]
        self.assertEqual(result, expect)

    def testFindCoClaw(self):
        g = DalGraph(make_co_claw())
        # add some noise
        g._g.add_node(4)
        g._g.add_node(5)
        g._g.add_node(6)
        g._g.add_node(7)
        g._g.add_edge(3, 4)
        g._g.add_edge(2,5)
        g._g.add_edge(1, 6)
        g._g.add_edge(3, 7)
        result = g.find_co_claw()
        expect = [2, 3, 1, 0]
        self.assertEqual(result, expect)
        # no triangle
        g = DalGraph(make_claw())
        # add some noise
        g._g.add_node(4)
        g._g.add_node(5)
        g._g.add_node(6)
        g._g.add_node(7)
        g._g.add_edge(0, 4)
        g._g.add_edge(0, 5)
        g._g.add_edge(0, 6)
        g._g.add_edge(0, 7)
        result = g.find_co_claw()
        expect = None
        self.assertEqual(result, expect)
        g = DalGraph(make_wheel(6))
        result = g.find_co_claw()
        self.assertEqual(result, expect)

    def testFindClaw(self):
        g = DalGraph(make_claw())
        # add some noise
        g._g.add_node(6)
        g._g.add_node(7)
        g._g.add_edge(1, 6)
        g._g.add_edge(3, 7)
        result = g.find_claw()
        expect = [1, 3, 2, 0]
        self.assertEqual(result, expect)
        # no triangle
        g = DalGraph(make_co_claw())
        result = g.find_claw()
        expect = None
        self.assertEqual(result, expect)
        g = DalGraph(make_wheel(6))
        result = g.find_claw()
        self.assertEqual(result, expect)

    def testCritical(self):
        # is_critical graphs
        g = nx.Graph()
        g.add_node(0)
        g = join(g, g)
        g = join(g, g)
        d = DalGraph(g)
        result = d.is_critical()
        self.assertEqual(result, True)
        g = make_wheel(6)
        d = DalGraph(g)
        result = d.is_critical()
        self.assertEqual(result, True)
        d = DalGraph(make_cycle(5))
        result = d.is_critical()
        self.assertEqual(result, True)
        # test non is_critical
        d = DalGraph(make_claw())
        result = d.is_critical()
        self.assertEqual(result, False)
        d = DalGraph(make_co_claw())
        result = d.is_critical()
        self.assertEqual(result, False)

class testK4CoDiamond(unittest.TestCase):
    def setUp(self):
        self.dal = DalGraph(make_cycle(5))

    def tearDown(self):
        pass

    def testDelete2(self):
        k = {'i,i+1,i+2': 1, 'i,i+1,i+4': 1}
        result = self.dal.delete_2(k)
        self.assertEqual(k, result)
        k = {'i,i+4': 1, 'i,i+1': 2, 'i+1,i+2': 1}
        result = self.dal.delete_2(k)
        expect = {}
        self.assertNotEqual(k, result)
        self.assertEqual(expect, result)

    def testCoverC5(self):
        covered = self.dal.cover_c5("i,i+1,i+2", "i+2,i+3,i+4")
        self.assertEqual(covered, True)
        covered = self.dal.cover_c5("i,i+1,i+2", "i+1,i+2,i+3")
        self.assertEqual(covered, False)

    def testCritical(self):
        critical = self.dal.k4_codiamond_critical()
        self.assertEqual(critical, True)
        self.dal = DalGraph(make_cycle(4))
        critical = self.dal.k4_codiamond_critical()
        self.assertEqual(critical, False)
        self.dal = DalGraph(make_cycle(5))
        self.dal._g.add_node(5)
        self.dal._g.add_edge(0, 5)
        self.dal._g.add_edge(1, 5)
        self.dal._g.add_edge(2, 5)
        self.dal._g.add_node(6)
        self.dal._g.add_edge(2, 6)
        self.dal._g.add_edge(3, 6)
        self.dal._g.add_edge(4, 6)
        critical = self.dal.k4_codiamond_critical()
        self.assertEqual(critical, True)
        self.dal = DalGraph(make_cycle(5))
        self.dal._g.add_node(5)
        self.dal._g.add_edge(0, 5)
        self.dal._g.add_edge(1, 5)
        self.dal._g.add_edge(2, 5)
        self.dal._g.add_node(6)
        self.dal._g.add_edge(1, 6)
        self.dal._g.add_edge(2, 6)
        self.dal._g.add_edge(3, 6)
        critical = self.dal.k4_codiamond_critical()
        self.assertEqual(critical, False)

