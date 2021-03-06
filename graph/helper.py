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

def make_co_cricket():
    '''
    make_co_cricket
    assembles a co-cricket
    Parameters:
        None
    Returns:
        g: the co-cricket (Graph)
    '''
    g = make_diamond()
    g.add_node(4)
    return g

def make_kite():
    '''
    make_kite
    assembles a kite (co-chair)
    Parameters:
        None
    Returns:
        kite: the kite (Graph)
    '''
    kite = make_diamond()
    kite.add_node(4)
    kite.add_edge(2, 4)
    return kite

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

def make_co_cycle(n):
    '''
    a function the creates an complement of a cycle of size n
    Parameters:
        n: the size of the anti cycle
    Returns:
        co_cycle: a networkx graph (networkx)
    '''
    return nx.complement(make_cycle(n))

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

def make_diamond():
    '''
    make_diamond
    assembles a diamond
    Parameters:
        None
    Returns:
        diamond: the diamond graph (networkx)
    '''
    diamond = nx.Graph()
    for x in range(0, 4):
        # add four vertices
        diamond.add_node(x)
    diamond.add_edge(0, 1)
    diamond.add_edge(0, 2)
    diamond.add_edge(0, 3)
    diamond.add_edge(1, 2)
    diamond.add_edge(1, 3)
    return diamond

def make_co_diamond():
    '''
    make_co_diamond
    assembles a co-diamond
    Parameters:
        None
    Returns:
        co_diamond: the co-diamond graph (networkx)
    '''
    return nx.complement(make_diamond())

def make_cok4():
    '''
    make_coK4
    assembles a co-K4
    Parameters:
        None
    Returns:
        g: the co-K4 graph (networkx)
    '''
    g = nx.Graph()
    g.add_node(0)
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    return g

def text_to_networkx(lines):
    '''
    text_to_networkx
    a function that takes the lines from a text file and puts into a format for 
    networkx graph
    Parameters:
        lines: a list of lines from the text file (list)
    Returns:
        graph: a networkx graph
    '''
#     try:
    graph = nx.Graph()
    index = 0
    nodes = []
    for line in lines:
        # add all the nodes
        entries = line.split(":")
        if len(entries) == 2:
            try:
                node = int(entries[0])
            except:
                node = None
            if node is None:
                node = index
            graph.add_node(node)
            nodes.append(node)
            index += 1
    index = 0
    for line in lines:
        # add all the edges
        entries = line.split(":")
        if (len(entries) > 1):
            entries[1] = entries[1].replace(" ", "")
            edges = entries[1].split(",")
            for edge in edges:
                if edge != '':
                    graph.add_edge(nodes[index], int(edge))
        index += 1
    return graph

def networkx_to_text(G):
    '''
    a function that converts a graph G to text
    Parameters:
        G: the graph (networkx)
    Returns:
        text: the graph text (string)
    '''
    text = ""
    for node in G.nodes():
        text += str(node) + ":"
        n = []
        for neighbor in G.neighbors(node):
            n.append(str(neighbor))
        text += ",".join(n)
        text += "\n"
    return text

def make_clique(n):
    '''
    makes a clique of size n
    Parameters:
        n: the size of the clique (int)
    Returns:
        clique: the graph (networkx)
    '''
    clique = nx.Graph()
    for v in range(0, n):
        clique.add_node(v)
    end = len(clique.nodes())
    for target in clique.nodes():
        for source in range(target+1, end):
            clique.add_edge(target, source)
    return clique

def make_2K2():
    '''
    a function which assembles a 2K2
    Parameters:
        None
    Returns:
        g: 2K2 graph (network)
    '''
    return nx.complement(make_cycle(4))

def make_co_twin_c5():
    '''
    a function to assemble a co-Twin-C5
    Parameters:
        None
    Returns:
        g: the graph g (networkx)
    '''
    g = make_cycle(5)
    g.add_node(5)
    g.add_edge(5, 0)
    g.add_edge(5, 2)
    g.add_edge(5, 1)
    return g

def make_co_twin_house():
    '''
    a function to assemble a co-Twin-House
    Parameters:
        None
    Returns:
        g: the graph g (networkx)
    '''
    g = make_diamond()
    g.add_node(4)
    g.add_node(5)
    g.add_edge(2, 4)
    g.add_edge(3, 5)
    return g

def make_co_p2_p3():
    '''
    a function to assemble a co p2-p3 graph
    Parameters:
        None
    Returns:
        g: the graph g (networkx)
    '''
    g = make_diamond()
    g.add_node(4)
    g.add_edge(2, 4)
    g.add_edge(3, 4)
    return g

def make_co_A():
    '''
    a function to assemble a co-A graph
    Parameters:
        None
    Returns:
        g: the graph g (networkx)
    '''
    g = nx.Graph()
    for i in range(0, 5):
        g.add_node(i)
    g.add_edge(0, 1)
    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(1, 2)
    g.add_edge(1, 4)
    g.add_edge(1, 5)
    g.add_edge(2, 5)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    return g

def make_co_R():
    '''
    a method to assemble a co-R graph
    Parameters:
        None
    Returns:
        g: the graph g (networkx)
    '''
    g = make_diamond()
    g.add_node(4)
    g.add_node(5)
    g.add_edge(0, 4)
    g.add_edge(1, 4)
    g.add_edge(2, 4)
    g.add_edge(3, 5)
    return g

def make_bridge():
    '''
    a method to assemble a bridge graph
    Parameters:
        None
    Returns:
        g: the graph g (networkx)
    '''
    g = make_co_R()
    g.add_edge(0, 5)
    g.add_edge(1, 5)
    return g

def forbidden_line_subgraphs():
    '''
    a method to assemble all 9 of the forbidden subgraphs
    of line graphs
    Parameters:
        None
    Returns:
        graphs: a list of graphs (networkx)
    '''
    graphs = []
    graphs.append(make_claw()) # claw
    graphs.append(make_wheel(6)) # W5
    graphs.append(make_bridge()) # Bridge
    graphs.append(make_co_R()) # Co-R
    graphs.append(make_co_A()) # Co-A
    graphs.append(make_co_p2_p3())
    graphs.append(make_co_twin_house())
    graphs.append(make_co_twin_c5())
    k5_e = make_clique(5)
    k5_e.remove_edge(3, 4)
    graphs.append(k5_e)
    return graphs

import unittest
import os
class tester(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testMakeClique(self):
        edges = [(0, 1), (0, 2), (1, 2)]
        nodes = [0, 1, 2]
        clique = make_clique(3)
        self.assertEqual(edges, clique.edges(), 'Make Clique: failed on edges')
        self.assertEqual(nodes, clique.nodes(), 'Make Clique: failed on nodes')
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        nodes = [0, 1, 2, 3]
        clique = make_clique(4)
        self.assertEqual(edges, clique.edges(), 'Make Clique: failed on edges')
        self.assertEqual(nodes, clique.nodes(), 'Make Clique: failed on nodes')
        
    def testMakeDiamond(self):
        g = make_diamond()
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)]
        vertices = [0, 1, 2, 3]
        self.assertEqual(edges, g.edges(), "Make Diamond: failed on edges")
        self.assertEqual(vertices, g.nodes(),
                         "Make Diamond: failed on vertices")

    def testMakeCoDiamond(self):
        g = make_co_diamond()
        edges = [(2, 3)]
        vertices = [0, 1, 2, 3]
        self.assertEqual(edges, g.edges(),
                         "Make Co-Diamond: failed on edges")
        self.assertEqual(vertices, g.nodes(),
                         "Make Co-Diamond: failed on vertices")

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

    def testTextToNetworkx(self):
        directory = os.getcwd()
        while "inducer" in directory:
            directory = os.path.dirname(directory)
        claw = make_claw()
        c7 = make_cycle(7)
        co_claw = make_co_claw()
        tests = {'test1.txt': claw, 'test2.txt': c7, 'test3.txt': co_claw}
        for f, expect in tests.items():
            filepath = os.path.join(directory, "tests", f)
            with open(filepath) as f:
                content = f.read()
                lines = content.replace("\r", "")
                lines = lines.split("\n")
                result = text_to_networkx(lines)
                self.assertEqual(expect.nodes() ,result.nodes() ,
                                 "Text to Networkx Failed Nodes: %s" % f)
                self.assertEqual(expect.edges() ,result.edges() ,
                                 "Text to Networkx Failed Nodes: %s" % f)

    def testNetworkxToText(self):
        g = make_claw()
        text = networkx_to_text(g)
        self.assertEqual("0:1,2,3\n1:0\n2:0\n3:0\n", text)
        g = make_diamond()
        text = networkx_to_text(g)
        self.assertEqual("0:1,2,3\n1:0,2,3\n2:0,1\n3:0,1\n", text)

    def testMakeCoK4(self):
        cok4 = make_cok4()
        self.assertEqual(cok4.nodes(), [0, 1, 2, 3])
        self.assertEqual(cok4.edges(), [])

    def testMake2K2(self):
        g = make_2K2()
        expect = [0, 1, 2, 3]
        self.assertEqual(g.nodes(), expect)
        expect = [(0, 2), (1, 3)]
        self.assertEqual(g.edges(), expect)

    def testMakeCoTwinC5(self):
        result = make_co_twin_c5()
        self.assertEqual(len(result.nodes()), 6)
        expect = [(0, 1), (0, 4), (0, 5), (1, 2), (1, 5),
                  (2, 3), (2, 5), (3, 4)]
        self.assertEqual(expect, result.edges())

    def testMakeCoTwinHouse(self):
        result = make_co_twin_house()
        self.assertEqual(len(result.nodes()), 6)
        expect = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 4), (3, 5)]
        self.assertEqual(expect, result.edges())

    def testMakeCoP2P3(self):
        result = make_co_p2_p3()
        self.assertEqual(len(result.nodes()), 5)
        expect = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 4), (3, 4)]
        self.assertEqual(expect, result.edges())

    def testMakeCoA(self):
        result = make_co_A()
        self.assertEqual(len(result.nodes()), 6)
        expect = [(0, 1), (0, 3), (0, 4), (1, 2), (1, 4),
                  (1, 5), (2, 5), (3, 4), (4, 5)]
        self.assertEqual(result.edges(), expect)

    def testMakeCoR(self):
        result = make_co_R()
        self.assertEqual(len(result.nodes()), 6)
        expect = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2),
                  (1, 3), (1, 4), (2, 4), (3, 5)]
        self.assertEqual(result.edges(), expect)

    def testMakeBridge(self):
        result = make_bridge()
        self.assertEqual(len(result.nodes()), 6)
        expect = [(0, 1), (0, 2), (0, 3), (0, 4),(0, 5), (1, 2),
                  (1, 3), (1, 4),(1, 5), (2, 4), (3, 5)]
        self.assertEqual(result.edges(), expect)

    def testForbiddenLineSubgraphs(self):
        result = forbidden_line_subgraphs()
        self.assertEqual(len(result), 9)
