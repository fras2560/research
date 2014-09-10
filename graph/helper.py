"""
-------------------------------------------------------
helper
a couple of helper functions
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-10
-------------------------------------------------------
"""
import networkx as nx
def make_claw():
    '''
    make_claw
    assembles a claw
    Parameters:
        None
    Returns:
        claw: the claw (Graph)
    '''
    claw = nx.Graph()
    for x in range(0, 4):
        # add four vertices
        claw.add_node(x)
    hub = 0 #0-vertex is the hub of claw
    for x in range(1, 4):
        claw.add_edge(hub, x)
    return claw

def make_co_claw():
    '''
    make_co_claw
    assembles a co-claw
    Parameters:
        None
    Returns:
        co_claw: the co_claw (Graph)
    '''
    return nx.complement(make_claw())

def make_cycle(n):
    '''
    make_cycle
    assembles a cycle with n vertices
    Parameters:
        n: the number of vertices in cycle (int)
    Returns:
        cycle: the cycle (Graph)
    '''
    cycle = nx.Graph()
    for vertex in range(0,n):
        #add all the vertices
        cycle.add_node(vertex)
    for vertex in range(0,n):
        #add all the edges
        cycle.add_edge(vertex, (vertex+1) % n)
        cycle.add_edge(vertex, (vertex-1) % n)
    return cycle

import unittest
class tester(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testMakeClaw(self):
        g = make_claw()
        edges = [(0, 1), (0, 2), (0, 3)]
        vertices =[0, 1, 2, 3]
        self.assertEqual(edges, g.edges(), "Make Claw: failed on edges")
        self.assertEqual(vertices, g.nodes(), "Make Claw: failed on vertices")

    def testMakeCoClaw(self):
        g = make_co_claw()
        edges = [(1, 2), (1, 3), (2, 3)]
        vertices =[0, 1, 2, 3]
        self.assertEqual(edges, g.edges(), "Make Co-Claw: failed on edges")
        self.assertEqual(vertices, g.nodes(),
                         "Make Co-Claw: failed on vertices")

    def testMakeCycle(self):
        g = make_cycle(3)
        edges = [(0,1), (0,2), (1,2)]
        vertices = [0, 1, 2]
        self.assertEqual(edges, g.edges(), "Make Cycle: failed on edges")
        self.assertEqual(vertices, g.nodes(), "Make Cycle: failed on vertices")
