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
import logging
logging.basicConfig(filename='genator.log', level=logging.INFO, 
                    format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

def generate(G, n, forbidden):
    '''
    a function to generate all the graphs starting with G adding
    up to N vertices not containing any H as a induced subgraph
    Parameters:
        G: the starting Graph (networkx)
        n: the number of vertices to add (int)
        forbidden: a list of forbidden subgraphs (networkx)
    Returns:
        graphs: a list of graphs
    '''
    logger.info("Generating graphs up to %d" % n)
    index = len(G.nodes()) - 1
    add_nodes = 0
    l_nodes = len(G.nodes())
    graphs = []
    g = G.copy()
    while index  < n:
        # add a node
        logger.info("Index: %d" % index)
        index += 1
        add_nodes += 1
        g.add_node(index)
        max_edges = int(l_nodes * add_nodes + ((add_nodes)*(add_nodes-1)) /2)
        logger.debug("Max Edges %d" % max_edges)
        for x in range(0, 2**max_edges):
            bitstring = to_bitstring(x, max_edges)
            logger.info(bitstring)
            h = g.copy()
            # add the edges
            for i, bit in enumerate(bitstring):
                logger.debug(i)
                if bit == "1":
                    target, source = determine(i, l_nodes, add_nodes)
                    logger.debug("Target: %d " % target)
                    logger.debug("Source: %d" % source)
                    h.add_edge(target, source)
            graphs.append(h)
    return graphs

def to_bitstring(number, pad=None):
    '''
    a function that takes a number and generates the bitstring
    Parameters:
        number: the positive whole number (int)
        pad: the length of the bitstring needed (int)
    Returns:
        bitstring: a string of bits 1 or 0 (string)
    '''
    power = largest_power(number)
    bitstring = ["0"] * (power+1)
    index = -1
    power = 2**power
    while number != 0:
        index += 1
        if number >= power:
            number -= power
            bitstring[index] = "1"
        power /= 2
    logger.debug("Generated bitstring:")
    logger.debug(bitstring)
    bitstring = "".join(bitstring)
    if pad is not None:
        while len(bitstring) < pad:
            bitstring = "0" + bitstring
    return bitstring

def largest_power(number):
    '''
    a function that finds the largest power of two
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

def determine(index, nodes, add_nodes):
    '''
    a function that determines what the source and target nodes of the edge are
    Parameters:
        index: the index of the edge to determine (int)
        nodes: the number of nodes (int)
        add_nodes: the number of nodes add (int)
    Returns
        (target, source): the target and source index (int)
    '''
    logger.debug("Determine")
    target = 1
    some = add_nodes - 1
    jump = nodes + some
    while index >= jump:
        index -=  jump
        target += 1
        some = add_nodes - target
        jump = nodes + some
    target += nodes - 1
    logger.debug("Index: %d" % index)
    if index >= nodes:
        index -= nodes
        source = index + target + 1
    elif index < nodes:
        source = index
    logger.debug("Target Node: %d" % target)
    logger.debug("Source: %d" % source)
    return(target, source)

import networkx as nx
import unittest
class Tester(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testLargestPower(self):
        self.assertEqual(largest_power(3), 1)
        self.assertEqual(largest_power(4), 2)
        self.assertEqual(largest_power(7), 2)
        self.assertEqual(largest_power(8), 3)

    def testToBitstring(self):
        self.assertEqual("11", to_bitstring(3))
        self.assertEqual("0", to_bitstring(0))
        self.assertEqual("1", to_bitstring(1))
        self.assertEqual("100", to_bitstring(4))
        self.assertEqual("111", to_bitstring(7))
        self.assertEqual("0011", to_bitstring(3, 4))
        self.assertEqual("00", to_bitstring(0, 2))
        self.assertEqual("01", to_bitstring(1, 2))
        self.assertEqual("0100", to_bitstring(4, 4))
        self.assertEqual("0111", to_bitstring(7,4))

    def testDetermine(self):
        # only one add node
        self.assertEqual(determine(0, 5, 1), (5,0))
        self.assertEqual(determine(1, 5, 1), (5,1))
        self.assertEqual(determine(2, 5, 1), (5,2))
        self.assertEqual(determine(3, 5, 1), (5,3))
        self.assertEqual(determine(4, 5, 1), (5,4))
        # two add nodes
        self.assertEqual(determine(0, 5, 2), (5,0))
        self.assertEqual(determine(1, 5, 2), (5,1))
        self.assertEqual(determine(2, 5, 2), (5,2))
        self.assertEqual(determine(3, 5, 2), (5,3))
        self.assertEqual(determine(4, 5, 2), (5,4))
        self.assertEqual(determine(5, 5, 2), (5,6))
        self.assertEqual(determine(6, 5, 2), (6,0))
        self.assertEqual(determine(7, 5, 2), (6,1))
        self.assertEqual(determine(8, 5, 2), (6,2))
        self.assertEqual(determine(9, 5, 2), (6,3))
        self.assertEqual(determine(10, 5, 2), (6,4))
        # three add nodes
        self.assertEqual(determine(0, 5, 3), (5,0))
        self.assertEqual(determine(1, 5, 3), (5,1))
        self.assertEqual(determine(2, 5, 3), (5,2))
        self.assertEqual(determine(3, 5, 3), (5,3))
        self.assertEqual(determine(4, 5, 3), (5,4))
        self.assertEqual(determine(5, 5, 3), (5,6))
        self.assertEqual(determine(6, 5, 3), (5,7))
 
        self.assertEqual(determine(7, 5, 3), (6,0))
        self.assertEqual(determine(8, 5, 3), (6,1))
        self.assertEqual(determine(9, 5, 3), (6,2))
        self.assertEqual(determine(10, 5, 3), (6,3))
        self.assertEqual(determine(11, 5, 3), (6,4))
        self.assertEqual(determine(12, 5, 3), (6,7))
        
        self.assertEqual(determine(13, 5, 3), (7,0))
        self.assertEqual(determine(14, 5, 3), (7,1))
        self.assertEqual(determine(15, 5, 3), (7,2))
        self.assertEqual(determine(16, 5, 3), (7,3))
        self.assertEqual(determine(17, 5, 3), (7,4))

    def testGenerate2Nodes(self):
        G = nx.Graph()
        G.add_node(0)
        graphs = generate(G, 1, [])
        self.assertEqual(len(graphs), 2)
        self.assertEqual(graphs[0].nodes(), [0, 1])
        self.assertEqual(graphs[0].edges(), [])
        self.assertEqual(graphs[1].nodes(), [0, 1])
        self.assertEqual(graphs[1].edges(), [(0,1)])

    def testGenerate3Nodes(self):
        G = nx.Graph()
        G.add_node(0)
        graphs = generate(G, 2, [])
        self.assertEqual(len(graphs), 10)
        self.assertEqual(graphs[0].nodes(), [0, 1])
        self.assertEqual(graphs[0].edges(), [])
        self.assertEqual(graphs[1].nodes(), [0, 1])
        self.assertEqual(graphs[1].edges(), [(0,1)])
        # three vertex graphs
        self.assertEqual(graphs[2].nodes(), [0, 1, 2])
        self.assertEqual(graphs[2].edges(), [])
        self.assertEqual(graphs[3].nodes(), [0, 1, 2])
        self.assertEqual(graphs[3].edges(), [(0, 2)])
        self.assertEqual(graphs[4].nodes(), [0, 1, 2])
        self.assertEqual(graphs[4].edges(), [(1, 2)])
        self.assertEqual(graphs[5].nodes(), [0, 1, 2])
        self.assertEqual(graphs[5].edges(), [(0, 2), (1, 2)])
        self.assertEqual(graphs[6].nodes(), [0, 1, 2])
        self.assertEqual(graphs[6].edges(), [(0, 1)])
        self.assertEqual(graphs[7].nodes(), [0, 1, 2])
        self.assertEqual(graphs[7].edges(), [(0, 1), (0, 2)])
        self.assertEqual(graphs[8].nodes(), [0, 1, 2])
        self.assertEqual(graphs[8].edges(), [(0, 1), (1, 2)])
        self.assertEqual(graphs[9].nodes(), [0, 1, 2])
        self.assertEqual(graphs[9].edges(), [(0, 1), (0, 2), (1, 2)])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
