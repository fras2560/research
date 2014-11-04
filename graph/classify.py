"""
-------------------------------------------------------
classify
a module to help classify the different types of k-vertex on
a cycle
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-10-16
-------------------------------------------------------
"""
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

def classify(G, cycle):
    '''
    a function to help classify the k-vertices on graph G
    Parameters:
        G: the graph to classify (networkx)
        cycle: the list of nodes which form the cycle (list)
            cycle should list nodes in order of traversal
    Returns:
        classification: a dictionary with the classifications (dict)
    '''
    k = k_vertices(G, cycle)
    classification = {}
    for node in k:
        edges = k[node]
        node_type = []
        index = 0
        for c in cycle:
            if c in edges:
                if index == 0:
                    node_type.append("i")
                else:
                    node_type.append("i+" + str(index))
            index += 1
        logger.debug(node_type)
        result = ",".join(node_type)
        if result not in classification:
            classification[result] = 0
        classification[result] += 1
    return classification

def k_vertices(G, cycle):
    '''
    a function returns a dictionary of k vertices and adjacency to cycle
    they are adjacent to
    Parameters:
        G: the graph to count (networkx)
        cycle: the list of nodes which form the cycle (list)
    Returns:
        k: the dictionary of k-vertexes and their adjacency to the cycle
            e.g. {node:adjacencylist, node2:...}
    '''
    k = {}
    for node in cycle:
        for neighbor in G.neighbors(node):
            if neighbor not in cycle:
                if neighbor not in k:
                    k[neighbor] = []
                k[neighbor].append(node)
    logger.debug(k)
    return k

import unittest
from graph.helper import make_cycle
class Test(unittest.TestCase):

    def setUp(self):
        self.g = make_cycle(5)
        self.cycle = [0, 1, 2, 3, 4]

    def tearDown(self):
        pass

    def testKVertices(self):
        # add a 1-vertex
        self.g.add_node(5)
        self.g.add_edge(0, 5)
        result = k_vertices(self.g, self.cycle)
        self.assertEqual({5:[0]}, result)
        # add a 5-vertex
        self.g.add_node(6)
        for node in range(0, 6):
            self.g.add_edge(node, 6)
        result = k_vertices(self.g, self.cycle)
        expect = {5: [0], 6: [0, 1, 2, 3, 4]}
        self.assertEqual(result, expect)

    def testClassification1V(self):
        # add to i vertex
        self.g.add_node(5)
        self.g.add_node(6)
        self.g.add_edge(0, 5)
        self.g.add_edge(0, 6)
        result = classify(self.g, self.cycle)
        expect = {'i': 2}
        self.assertEqual(result, expect)

    def testClassificationXi(self):
        # add 2Xi, Xi+1, Xi+3
        self.g.add_node(5)
        self.g.add_node(6)
        self.g.add_node(7)
        self.g.add_node(8)
        self.g.add_edge(0, 5)
        self.g.add_edge(1, 5)
        self.g.add_edge(0, 6)
        self.g.add_edge(1, 6)
        self.g.add_edge(1, 7)
        self.g.add_edge(2, 7)
        self.g.add_edge(4, 8)
        self.g.add_edge(0, 8)
        result = classify(self.g, self.cycle)
        expect = {'i,i+4': 1, 'i,i+1': 2, 'i+1,i+2': 1}
        self.assertEqual(result, expect)

    def testClassificationYi(self):
        # add Yi, Yi+1
        self.g.add_node(5)
        self.g.add_node(6)
        self.g.add_edge(4, 5)
        self.g.add_edge(0, 5)
        self.g.add_edge(1, 5)
        self.g.add_edge(0, 6)
        self.g.add_edge(1, 6)
        self.g.add_edge(2, 6)
        result = classify(self.g, self.cycle)
        expect = {'i,i+1,i+2': 1, 'i,i+1,i+4': 1}
        self.assertEqual(result, expect)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()