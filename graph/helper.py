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
        # add all the vertices
        cycle.add_node(vertex)
    for vertex in range(0,n):
        # add all the edges
        cycle.add_edge(vertex, (vertex+1) % n)
        cycle.add_edge(vertex, (vertex-1) % n)
    return cycle

def make_wheel(n):
    '''
    make_wheel
    assembles a wheel with n vertices
    Parameters:
        n: the number of vertices in the wheel (int)
    Returns:
        wheel: the wheel (networkx)
    '''
    wheel = make_cycle(n-1)
    wheel.add_node(n-1)
    for edge in range(0,n-1):
        wheel.add_edge(edge,n-1)
    return wheel

def join(G, H):
    '''
    join
    a function which (complete) joins one graph G to graph H
    Parameters:
        G: Graph with at least one vertice (Graph)
        H: Graph with at least one vertice (Graph)
    Returns:
        F: The join of G and H (Graph)
    '''
    # add all of
    F = nx.Graph()
    F.add_nodes_from(G.nodes())
    F.add_edges_from(G.edges())
    shift = G.number_of_nodes()
    # add all nodes of H
    for vertex in H.nodes():
        F.add_node(vertex)
    # add all of F edges
    for e1, e2 in H.edges():
        F.add_edge(e1 + shift, e2 + shift)
    # join the two sets of nodes
    for v1 in G.nodes():
        for v2 in H.nodes():
            F.add_edge(v1,v2+shift)
    return F

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

    def testJoin(self):
        # wheel test
        g = make_cycle(5)
        h = nx.Graph()
        h.add_node(0)
        f = join(g, h)
        expect = nx.wheel_graph(6) # expect a wheel
        self.assertEqual(expect.nodes(), f.nodes(),
                         " Join: nodes failed on wheel test")
        self.assertEqual(nx.is_isomorphic(f, expect), True,
                         " Join: edges failed on wheel test")
        # join of two trianges = K6
        g = nx.complete_graph(3)
        h = nx.complete_graph(3)
        f = join(g, h)
        expect = nx.complete_graph(6)
        self.assertEqual(expect.nodes(), f.nodes(), 
                         "Join: nodes failed for K6 test")
        self.assertEqual(nx.is_isomorphic(f, expect), True,
                         " Join: edges failed on wheel K6 test")

    def testWheel(self):
        # w5
        w = make_wheel(5)
        g = make_cycle(4)
        g.add_node(5)
        g.add_edge(0,4)
        g.add_edge(1,4)
        g.add_edge(2,4)
        g.add_edge(3,4)
        self.assertEqual(w.edges(), g.edges(), "Make wheel: Failed for W5 test")
