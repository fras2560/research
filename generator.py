"""
-------------------------------------------------------
generator

a function to generate all the graphs starting with G
to up to N vertices not containing any H as a induced subgraph
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-10-19
-------------------------------------------------------
"""
from graph.container import induced_subgraph, k_vertex
import logging
import graph

class Generator():
    def __init__(self, G, n, forbidden, logger=None):
        self.G = G
        self.n = n
        self.forbidden = forbidden
        if logger is None:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(message)s')
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    def total_graphs(self):
        '''
        a method to determine the total number of graphs
        Parameters:
            None
        Returns:
            total_graphs: the number of graphs (long)
        '''
        total_graphs = 0
        l_nodes = len(self.G.nodes())
        for i in range(1, self.n + 1):
            max_edges = int(l_nodes * i + ((i)*(i-1)) /2)
            total_graphs += 2**max_edges
        return total_graphs

    def iterate(self):
        '''
        a generator for all the graphs starting with G adding
        up to N vertices not containing any H as a induced subgraph
        Parameters:
        Returns:
            yields: a graph h (networx)
        '''
        self.logger.info("Generating graphs up to %d" % self.n)
        index = len(self.G.nodes()) - 1
        add_nodes = 0
        l_nodes = len(self.G.nodes())
        g = self.G.copy()
        while index  < (self.n + l_nodes - 1):
            # add a node
            print("----------------")
            print("Index: %d of %d" % (index, self.n + l_nodes - 1))
            print("----------------")
            self.logger.info("Index: %d" % index)
            index += 1
            add_nodes += 1
            g.add_node(index)
            max_edges = int(l_nodes * add_nodes + ((add_nodes)*(add_nodes-1)) /2)
            self.logger.debug("Max Edges %d" % max_edges)
            for x in range(0, 2**max_edges):
                bitstring = self.to_bitstring(x, max_edges)
                h = g.copy()
                # add the edges
                for i, bit in enumerate(bitstring):
                    self.logger.debug(i)
                    if bit == "1":
                        target, source = self.determine(i, l_nodes, add_nodes)
                        self.logger.debug("Target: %d " % target)
                        self.logger.debug("Source: %d" % source)
                        h.add_edge(target, source)
                allowed = True
                for not_allowed in self.forbidden:
                    if induced_subgraph(h, not_allowed) is not None:
                        allowed = False
                        break
                if allowed:
                    self.logger.info("Graph was not forbidden")
                    yield h

    def to_bitstring(self, number, pad=None):
        '''
        a method that takes a number and generates the bitstring
        Parameters:
            number: the positive whole number (int)
            pad: the length of the bitstring needed (int)
        Returns:
            bitstring: a string of bits 1 or 0 (string)
        '''
        power = self.largest_power(number)
        bitstring = ["0"] * (power+1)
        index = -1
        power = 2**power
        while number != 0:
            index += 1
            if number >= power:
                number -= power
                bitstring[index] = "1"
            power /= 2
        self.logger.debug("Generated bitstring:")
        self.logger.debug(bitstring)
        bitstring = "".join(bitstring)
        if pad is not None:
            while len(bitstring) < pad:
                bitstring = "0" + bitstring
        return bitstring

    def largest_power(self, number):
        '''
        a method that finds the largest power of two
        Parameters:
            number: positive whole number (int)
        Returns:
            power: the largest power (int)
        '''
        index = 0
        power = 0
        while 2**index <= number:
            power = index
            index += 1
        return power

    def determine(self, index, nodes, add_nodes):
        '''
        a method that determines what the source and target nodes of the edge are
        Parameters:
            index: the index of the edge to determine (int)
            nodes: the number of nodes (int)
            add_nodes: the number of nodes add (int)
        Returns
            (target, source): the target and source index (int)
        '''
        self.logger.debug("Determine")
        target = 1
        some = add_nodes - 1
        jump = nodes + some
        while index >= jump:
            index -=  jump
            target += 1
            some = add_nodes - target
            jump = nodes + some
        target += nodes - 1
        self.logger.debug("Index: %d" % index)
        if index >= nodes:
            index -= nodes
            source = index + target + 1
        elif index < nodes:
            source = index
        self.logger.debug("Target Node: %d" % target)
        self.logger.debug("Source: %d" % source)
        return(target, source)

class Generator2():
    def __init__(self, G, n, forbidden, logger=None):
        self.G = G
        self.n = n
        self.forbidden = forbidden
        if logger is None:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger = logger

    def iterate(self):
        for graph in self.iterate_aux(self.G):
            yield graph

    def iterate_aux(self, g):
        index = len(g.nodes())
        if index >= self.n + len(self.G.nodes()):
            # must be done
            self.logger.debug("Reach index %d" % index)
        else:
            # still need to add drop vertexes
            for k_set in k_vertex(g, self.forbidden):
                if k_set['has_k_vertex']:
                    if len(k_set['combinations']) > 0:
                        k =len(k_set['combinations'][0])
                    else:
                        h = g.copy()
                        h.add_node(index)
                        k = 0
                        yield h
                    self.logger.debug("Has k Vertex: %d" % k)
                    self.logger.debug("Combination:")
                    self.logger.debug(k_set['combinations'])
                    for combo in k_set['combinations']:
                        h = g.copy()
                        h.add_node(index)
                        for edge in combo:
                            h.add_edge(edge, index)
                        yield h # a valid graph
                        for graph in self.iterate_aux(h):
                            yield graph

import networkx as nx
import unittest
from graph.helper import make_claw, make_cycle, make_cok4

class Tester(unittest.TestCase):
    def setUp(self):
        self.gen = Generator(make_claw(), 2, [])

    def tearDown(self):
        pass

    def testLargestPower(self):
        self.assertEqual(self.gen.largest_power(3), 1)
        self.assertEqual(self.gen.largest_power(4), 2)
        self.assertEqual(self.gen.largest_power(7), 2)
        self.assertEqual(self.gen.largest_power(8), 3)

    def testToBitstring(self):
        self.assertEqual("11", self.gen.to_bitstring(3))
        self.assertEqual("0", self.gen.to_bitstring(0))
        self.assertEqual("1", self.gen.to_bitstring(1))
        self.assertEqual("100", self.gen.to_bitstring(4))
        self.assertEqual("111", self.gen.to_bitstring(7))
        self.assertEqual("0011", self.gen.to_bitstring(3, 4))
        self.assertEqual("00", self.gen.to_bitstring(0, 2))
        self.assertEqual("01", self.gen.to_bitstring(1, 2))
        self.assertEqual("0100", self.gen.to_bitstring(4, 4))
        self.assertEqual("0111", self.gen.to_bitstring(7,4))

    def testDetermine(self):
        # only one add node
        self.assertEqual(self.gen.determine(0, 5, 1), (5,0))
        self.assertEqual(self.gen.determine(1, 5, 1), (5,1))
        self.assertEqual(self.gen.determine(2, 5, 1), (5,2))
        self.assertEqual(self.gen.determine(3, 5, 1), (5,3))
        self.assertEqual(self.gen.determine(4, 5, 1), (5,4))
        # two add nodes
        self.assertEqual(self.gen.determine(0, 5, 2), (5,0))
        self.assertEqual(self.gen.determine(1, 5, 2), (5,1))
        self.assertEqual(self.gen.determine(2, 5, 2), (5,2))
        self.assertEqual(self.gen.determine(3, 5, 2), (5,3))
        self.assertEqual(self.gen.determine(4, 5, 2), (5,4))
        self.assertEqual(self.gen.determine(5, 5, 2), (5,6))
        self.assertEqual(self.gen.determine(6, 5, 2), (6,0))
        self.assertEqual(self.gen.determine(7, 5, 2), (6,1))
        self.assertEqual(self.gen.determine(8, 5, 2), (6,2))
        self.assertEqual(self.gen.determine(9, 5, 2), (6,3))
        self.assertEqual(self.gen.determine(10, 5, 2), (6,4))
        # three add nodes
        self.assertEqual(self.gen.determine(0, 5, 3), (5,0))
        self.assertEqual(self.gen.determine(1, 5, 3), (5,1))
        self.assertEqual(self.gen.determine(2, 5, 3), (5,2))
        self.assertEqual(self.gen.determine(3, 5, 3), (5,3))
        self.assertEqual(self.gen.determine(4, 5, 3), (5,4))
        self.assertEqual(self.gen.determine(5, 5, 3), (5,6))
        self.assertEqual(self.gen.determine(6, 5, 3), (5,7))
 
        self.assertEqual(self.gen.determine(7, 5, 3), (6,0))
        self.assertEqual(self.gen.determine(8, 5, 3), (6,1))
        self.assertEqual(self.gen.determine(9, 5, 3), (6,2))
        self.assertEqual(self.gen.determine(10, 5, 3), (6,3))
        self.assertEqual(self.gen.determine(11, 5, 3), (6,4))
        self.assertEqual(self.gen.determine(12, 5, 3), (6,7))
        
        self.assertEqual(self.gen.determine(13, 5, 3), (7,0))
        self.assertEqual(self.gen.determine(14, 5, 3), (7,1))
        self.assertEqual(self.gen.determine(15, 5, 3), (7,2))
        self.assertEqual(self.gen.determine(16, 5, 3), (7,3))
        self.assertEqual(self.gen.determine(17, 5, 3), (7,4))

    def testGenerate2Nodes(self):
        
        G = nx.Graph()
        G.add_node(0)
        index = 0
        expected = [{'nodes':[0, 1], 'edges':[]},
                    {'nodes':[0, 1], 'edges':[(0, 1)]}]
        self.gen = Generator(G, 1, [])
        for graph in self.gen.iterate():
            self.assertEqual(graph.nodes(), expected[index]['nodes'])
            self.assertEqual(graph.edges(), expected[index]['edges'])
            index += 1
        self.assertEqual(index, 2)

    def testGenerate3Nodes(self):
        G = nx.Graph()
        G.add_node(0)
        index = 0
        expected = [{'nodes':[0, 1], 'edges':[]},
                    {'nodes':[0, 1], 'edges':[(0, 1)]},
                    {'nodes':[0, 1, 2], 'edges':[]},
                    {'nodes':[0, 1, 2], 'edges':[(0, 2)]},
                    {'nodes':[0, 1, 2], 'edges':[(1, 2)]},
                    {'nodes':[0, 1, 2], 'edges':[(0, 2), (1, 2)]},
                    {'nodes':[0, 1, 2], 'edges':[(0, 1)]},
                    {'nodes':[0, 1, 2], 'edges':[(0, 1), (0, 2)]},
                    {'nodes':[0, 1, 2], 'edges':[(0, 1),(1, 2)]},
                    {'nodes':[0, 1, 2], 'edges':[(0, 1), (0, 2), (1, 2)]}
                    ]
        self.gen = Generator(G, 2 , [])
        for graph in self.gen.iterate():
            self.assertEqual(graph.nodes(), expected[index]['nodes'])
            self.assertEqual(graph.edges(), expected[index]['edges'])
            index += 1
        self.assertEqual(index, 10)

    def testTotalGraphs(self):
        G = nx.Graph()
        G.add_node(0)
        self.gen = Generator(G, 2, [])
        result = self.gen.total_graphs()
        self.assertEqual(10, result)
        G = make_cycle(5)
        self.gen  = Generator(G, 5, [])
        result = self.gen.total_graphs()
        self.assertEqual(34427111456, result)

class Tester2(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTwoNode(self):
        g = nx.Graph()
        g.add_node(0)
        gen = Generator2(g, 1, [])
        expected = [{'nodes':[0, 1],
                     'edges':[]},
                    {'nodes':[0, 1],
                     'edges':[(0, 1)]},
                    ]
        number = 0
        for graph in gen.iterate():
            self.assertEqual(expected[number]['nodes'], graph.nodes())
            self.assertEqual(expected[number]['edges'], graph.edges())
            number += 1
        self.assertEqual(number, 2)

    def testForbidden(self):
        claw = make_claw()
        c4 = make_cycle(4)
        cok4 = make_cok4()
        g = make_cycle(5)
        not_allowed = [claw, c4, cok4]
        gen = Generator2(g, 1, forbidden=not_allowed)
        for graph in gen.iterate():
            for h in not_allowed:
                if induced_subgraph(graph, h) is not None:
                    print(graph.edges())
                    print(h.edges())
                    self.assertEqual(True, False ,"Failed to forbid a graph")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
