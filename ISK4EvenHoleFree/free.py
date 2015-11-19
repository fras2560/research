"""
-------------------------------------------------------
free
holds a object that finds if a graph
is a subdivisions of K4 (ISK4)
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-10
-------------------------------------------------------
"""
import logging
import networkx as nx
from graph.container import induced_subgraph
from graph.helper import make_clique

POSITION = {0:(0, 1),
            1:(0, 2),
            2:(0,3),
            3:(1, 2),
            4:(1,3),
            5:(2, 3)}

class ISK4Free():
    def __init__(self,g,logger=None):
        if logger is None:
            logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger = logger
        self.g = g

    def free(self):
        '''
        a method to determine if the graph is ISK4-free
        Parameters:
            None
        Returns:
            sub: list of vertices that form a ISK4
                    is None if does not contain (list)
        '''
        # check if omega is greater than four
        sub = None
        if nx.graph_clique_number(self.g) > 3:
            sub = induced_subgraph(self.g, make_clique(4))
        else:
            # loop through all possible subdivisions between 4 and n
            n = len(self.g.nodes())
            i = 0
            while i < n - 3 and sub is None:
                for ball in unlabeled_balls_in_unlabeled_boxe(i,
                                                              [i]*6):
                    graph = self.create_subdivions(ball)
                    sub = induced_subgraph(self.g, graph)
                    if sub is not None:
                        break
                i += 1
        return sub


    def create_subdivions(self, config):
        '''
        a method that creates a subdivision based on the configuration given
        Parameters:
            config: a list of paths lengths between each vertex of the K4
        Returns
            graph: a network graph (networkx)
        '''
        graph = nx.Graph()
        
        for i in range(0,4):
            graph.add_node(i)
        nodes = len(graph.nodes())
        for index, path_length in enumerate(config):
            # assemble a path
            (start, end) = POSITION[index]
            path = [start]
            while len(path) <= path_length:
                graph.add_node(nodes)
                path.append(nodes)
                nodes += 1
            path.append(end)
            # connect the path
            for i in range(0, len(path) - 1):
                graph.add_edge(path[i], path[i+1])
        return graph

def unlabeled_balls_in_unlabeled_boxes(balls, box_sizes):
    '''
    @author Dr. Phillip M. Feldman
    '''
    if not isinstance(balls, int):
        raise TypeError("balls must be a non-negative integer.")
    if balls < 0:
        raise ValueError("balls must be a non-negative integer.")
    if not isinstance(box_sizes,list):
        raise ValueError("box_sizes must be a non-empty list.")
    capacity= 0
    for size in box_sizes:
        if not isinstance(size, int):
            raise TypeError("box_sizes must contain only positive integers.")
        if size < 1:
            raise ValueError("box_sizes must contain only positive integers.")
        capacity+= size
    if capacity < balls:
        raise ValueError("The total capacity of the boxes is less than the "
                         "number of balls to be distributed.")
    box_sizes= list( sorted(box_sizes)[::-1] )
    return unlabeled_balls_in_unlabeled_boxe(balls, box_sizes)

def unlabeled_balls_in_unlabeled_boxe(balls, box_sizes):
    '''
    @author Dr. Phillip M. Feldman
    '''
    if not balls:
        yield len(box_sizes) * (0,)
    elif len(box_sizes) == 1:
        if box_sizes[0] >= balls:
            yield (balls,)
    else:
        for balls_in_first_box in range( min(balls, box_sizes[0]), -1, -1 ):
            balls_in_other_boxes = balls - balls_in_first_box
            short = unlabeled_balls_in_unlabeled_boxe
            for distribution_other in short(balls_in_other_boxes,
                                            box_sizes[1:]):
                if distribution_other[0] <= balls_in_first_box:
                    yield (balls_in_first_box,) + distribution_other
            

from graph.helper import make_co_twin_c5, make_cycle
import unittest
class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def compare_graphs(self,g , h):
        same = False
        if (len(g.nodes()) == len(h.nodes())):
            induced = induced_subgraph(g, h)
            if induced is not None:
                same = True
        return same

    def testCreateSubdivision(self):
        # test one zero paths and 1 path$
        g = ISK4Free(make_co_twin_c5())
        result = g.create_subdivions([0,0,0,0,0,0])
        self.assertEqual(self.compare_graphs(result, make_clique(4)), True)
        result = g.create_subdivions([1,0,0,0,0,0])
        expect = make_clique(4)
        expect.remove_edge(2, 3)
        expect.add_node(4)
        expect.add_edge(2,4)
        expect.add_edge(3,4)
        self.assertEqual(self.compare_graphs(result, expect), True)

    def testFree(self):
        # simple case
        g = ISK4Free(make_clique(4))
        result = g.free()
        self.assertEqual(self.compare_graphs(result, make_clique(4)), True)
        # another simple case
        g = ISK4Free(make_co_twin_c5())
        result = g.free()
        expect = make_co_twin_c5()
        self.assertEqual(self.compare_graphs(result, expect), True)
        # difficult graph
        graph = make_cycle(5)
        graph.add_node(5)
        graph.add_edge(0, 5)
        graph.add_edge(1, 5)
        graph.add_edge(3, 5)
        g = ISK4Free(graph)
        result = g.free()
        self.assertEqual(self.compare_graphs(result, graph), True)
        # one with no ISK4
        graph = make_cycle(6)
        g = ISK4Free(graph)
        result = g.free()
        self.assertEqual(result, None)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()