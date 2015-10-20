"""
-------------------------------------------------------
classify
a function that classifies non G - H wrt to H
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-10
-------------------------------------------------------
"""

def classification(hole, graph):
    '''
        a function that classifies non G - H wrt to H
        Parameters:
            hole: a list of vertices that form a hole
            graph: a networkx graph
        Returns:
            groups: {x:{0:[], ...}, y:{0:[],...}, r:[], w:[], spoke=[]}
    '''
    x = {}
    y = {}
    for node in hole:
        x[node] = []
        y[node] = []
    r = []
    w = []
    spokes = []
    for node in graph.nodes():
        if node not in hole:
            count = 0 
            bros = []
            for neighbor in graph.neighbors(node):
                if neighbor in hole:
                    count += 1
                    bros.append(neighbor)
            if count == len(hole):
                w.append(node)
            elif count == 1:
                x[bros[0]].append(node)
            elif count == 0:
                r.append(node)
            elif count == 2:
                if bros[0] < bros[1]:
                    y[bros[0]].append(node)
                else:
                    y[bros[1]].append(node)
            else:
                spokes.append(node)
    return {'x': x,
            'y': y,
            'w': w,
            'r': r,
            'spokes': spokes}

import unittest
from graph.helper import make_cycle
class Test(unittest.TestCase):

    def setUp(self):
        self.graph = make_cycle(5)
        x = 5
        y = 6
        w = 7
        self.graph.add_node(x)
        self.graph.add_node(y)
        self.graph.add_node(w)
        
        self.graph.add_edge(1, x)
        self.graph.add_edge(2, y)
        self.graph.add_edge(3, y)
        for i in range(0, 4):
            self.graph.add_edge(i, w)

    def tearDown(self):
        pass

    def testName(self):
        result = classification(make_cycle(5), self.graph)
        print(result)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()