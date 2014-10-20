"""
-------------------------------------------------------
contains
holds a function contains
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-17
-------------------------------------------------------
"""
import itertools
import networkx as nx
import graph.helper as helper
def induced_subgraph(G, H):
    '''
    induced_subgraph
    a function that checks if G has an induced subgraph of H
    Parameters:
        G: the graph to check (networkx)
        H: the induced subgraph (networkx)
    Returns:
        induced: the induced subgraph (networkx)
    Method:
        just create every permutation of the G graph with as many vertices
        as H and use networkx to check if isomorphic
    Note:
         not solved in polynomial time (only use for small cases)
    '''
    n = len(G)
    k = len(H)
    if n < k:
        return None
    permutations = create_permutations(n, k)
    induced = None
    for subset in permutations:
        subgraph = G.subgraph(subset)
        if nx.faster_could_be_isomorphic(subgraph, H):
            if nx.is_isomorphic(subgraph, H):
                induced = subgraph
                break # only want to find one
    return induced
        
def create_permutations(n, k):
    '''
    create_permutations
    a function which returns a list of all possible permutations n choose k
    Parameters:
        n: the total number of items
        k: the number of items to choose
    Returns:
        iterator: to the list of permutations
    '''
    number_list = []
    for x in range(0,n):
        number_list.append(x)
    return itertools.combinations(number_list, k)

def k_vertex(g, subgraphs):
    '''
    k_vertex
    a function that finds all the k_vertex for k=0 to n (# of g vertices)
    Parameters:
        g: the graph to finds the k vertex for (networkx)
        subgraphs: the list of subgraphs g is to be free of (list of networkx)
    Returns:
        k_vertexes: python dictionary 
        eg. [{has_k_vertex: Boolean, combination: [[node,node],[node,node]]}]
    '''
    nodes = g.nodes()
    node = len(g.nodes())
    k_vertexes = []
    # check for zero vertex
    g.add_node(node)
    zero_vertex = True
    for sub in subgraphs:
        induced = induced_subgraph(g, sub) 
        if induced is not None:
            zero_vertex = False
            break;
    if zero_vertex:
        k_vertexes.append({'has_k_vertex':True, 'combinations':[]})
    else:
        k_vertexes.append({'has_k_vertex':False, 'combinations':[]})
    # check the rest now
    g.remove_node(node) # remove added node
    for k in range(1, node + 1):
        k_vertexes.append({'has_k_vertex': False, 'combinations':[]})
        for combo in itertools.combinations(nodes, k):
            g.add_node(node) # add node
            #add the edges
            for vertex in combo:
                g.add_edge(node, vertex)
            does_contain = False # assume it does not contain all the subgraphs
            for sub in subgraphs:
                induced = induced_subgraph(g, sub)
                if induced is not None:
                    # does contain a forbidden subgraph
                    does_contain = True
            if not does_contain:
                # did not contain any forbidden subgraph
                k_vertexes[k]['has_k_vertex'] = True
                k_vertexes[k]['combinations'].append(combo)
            g.remove_node(node) # remove added node and its edges 
    return k_vertexes

import unittest
from graph.helper import make_cycle, make_claw, make_co_claw
from graph.helper import make_diamond, make_co_diamond
from pprint import PrettyPrinter
class tester(unittest.TestCase):
    def setUp(self):
        self.pp = PrettyPrinter(indent = 4)

    def tearDown(self):
        pass

    def testInducedSubgraph(self):
        h = helper.make_claw()
        g = helper.make_wheel(7)
        induced = induced_subgraph(g, h)
        expected = [0, 2, 4, 6] 
        self.assertEqual(induced.nodes(), expected,
                         "Contains: Failed to find a claw in W7")

    def testC7CoClawClawFree(self):
        g = make_cycle(7)
        subgraphs = [make_claw(), make_co_claw()]
        k_vertexes = k_vertex(g, subgraphs)
        for index, k in enumerate(k_vertexes):
            if index > 0:
                self.assertEqual(k['has_k_vertex'], False,
                                 '''
                                 K Vertex says (claw,co-claw)-free Graph 
                                 has a %s-vertex'''  % index)
            else:
                self.assertEqual(k['has_k_vertex'], True,
                                 '''
                                 K Vertex says (claw,co-claw)-free Graph 
                                 has no a %s-vertex'''  % index)

    def testC5DiamondCoDiamondFree(self):
        g = make_cycle(5)
        subgraphs = [make_diamond(), make_co_diamond()]
        k_vertexes = k_vertex(g, subgraphs)
        expect = [False, False, True, True, False, False]
        for index, k in enumerate(k_vertexes):
            self.assertEqual(k['has_k_vertex'], expect[index],
                             '''K Vertex says (diamond,co-diamond)- free Graph
                             %d - vertex:%r but should be %r''' 
                             %(index, k['has_k_vertex'], expect[index]))
        set_2_vertex = [(0, 1), (0, 4), (1, 2), (2, 3), (3, 4)]
        for check in set_2_vertex:
            self.assertEqual(check in k_vertexes[2]['combinations'], True,
                            '''
                            K vertex missing 2 Vertex set (%d, %d)
                            on (diamond, co-diamond)-free Grpah
                            ''' %(check[0],check[1]))
        set_3_vertex = [(0, 1, 3),
                        (0, 2, 3),
                        (0, 2, 4),
                        (1, 2, 4),
                        (1, 3, 4)]
        for check in set_3_vertex:
            self.assertEqual(check in k_vertexes[3]['combinations'], True,
                            '''
                            K vertex missing 3 Vertex set (%d, %d, %d)
                            on (diamond, co-diamond)-free Grpah
                            ''' %(check[0],check[1], check[2]))
