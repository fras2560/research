"""
-------------------------------------------------------
This program creates graphs by adding {3,5}-vertices to C7 while remaining
{4k1,c4,c6}-free.
-------------------------------------------------------
Author:  Dallas Fraser, Tom LaMantia
ID:      110242560
Email:   fras2560@mylaurier.ca, lama3790@mylaurier.ca
Version: 2015-05-26
-------------------------------------------------------
"""

from graph.helper import make_cycle, make_cok4
from tqdm import tqdm
from os import getcwd
from os.path import join
from file import File
from itertools import combinations_with_replacement, permutations
from graph.container import induced_subgraph
import logging

FAMILY = "Line(Co-K4)-free-C7"
DIRECTORY = join(getcwd(), 'GraphFamilies', FAMILY)
YIVALUE = 1
ZIVALUE = 2
BASE = make_cycle(7)
FORBIDDEN = [make_cycle(4), make_cycle(6), make_cok4()]
BOTH = 3
logging.basicConfig(filename=FAMILY + "Enumerate.log", level=logging.INFO,
                            format='%(asctime)s %(message)s')
LOGGER = logging.getLogger(__name__)

class Enumerate():
    def __init__(self):
        self.g = BASE

    def add_vertices(self, permutation):
        ypositions = [0, 0, 0, 0, 0, 0, 0]
        zpositions = [0, 0, 0, 0, 0, 0, 0]
        vertex = 7
        for i, value  in enumerate(permutation):
            if value == YIVALUE or value == BOTH:
                #add the new Y vertex and its edges
                self.g.add_node(vertex)
                self.g.add_edge(vertex, i)
                self.g.add_edge(vertex, (i+1) % 7)
                self.g.add_edge(vertex, (i+4) % 7)
                #Give this Y vertex a unique identifier and draw edges between new vertices if needed
                for x in range(i, -1, -1):
                    if ypositions[x] > 0 and vertex - x != 2 :
                        self.g.add_edge(vertex, ypositions[x])
                        
                    if zpositions[x] > 0:
                        self.g.add_edge(vertex, zpositions[x])
                ypositions[i] = vertex
                vertex += 1
            if value == ZIVALUE or value == BOTH:
                #add the new Z vertex and its edges
                self.g.add_node(vertex)
                self.g.add_edge(vertex, i)
                self.g.add_edge(vertex, (i+1) % 7)
                self.g.add_edge(vertex, (i+2) % 7)
                self.g.add_edge(vertex, (i+3) % 7)
                self.g.add_edge(vertex, (i+4) % 7)
                #Give this Y vertex a unique identifier and draw edges between new vertices if needed
                for x in range(i, -1, -1):
                    if ypositions[x] > 0:
                        self.g.add_edge(vertex, ypositions[x])
                    if zpositions[x] > 0:
                        self.g.add_edge(vertex, zpositions[x])
                zpositions[i] = vertex
                vertex += 1
        return

    def count(self, combo):
        verticesAdded = 0
        for x in combo:
            if x == YIVALUE or x ==  ZIVALUE:
                verticesAdded += 1
            if x == BOTH:
                verticesAdded += 1 #we already counted one vertex, now we need to count the other too.
        return verticesAdded

    def process(self):
        index = 0
        #Generate an array corresponding to the k-vertices we want to add to c7
        for add in combinations_with_replacement(range(4), 7):
            print(add)
            #We can have at most 3 Z's and 2 Y's, making 5 possible vertices we can add
            if self.count(add) > 5:
                break
            for thisPermutation in permutations(add):
                #copy initial graph (c7) and add vertices
                #self.g = BASE.copy()
                self.g = make_cycle(7)
                self.add_vertices(thisPermutation)
                check = True
                #we want our graph to remain {4k1,c4,c6}-free
                for H in FORBIDDEN:
                    if induced_subgraph(self.g, H):
                        check  = False
                        break
                if check:
                    #log it
                    
                    f = File(DIRECTORY, G=self.g, logger=LOGGER, base="C5-")
                    fp = f.save()
                    if fp is not None:
                        index += 1
                        print("Created Graph: %d" % index)

import unittest
class Tester(unittest.TestCase):
    def setUp(self):
        #called when starting test
        self.e = Enumerate()

    def tearDown(self):
        #called when done test
        pass

    def testProcess(self):
        self.e.process()

#    def testAddVertices(self):
#         # test one
#         self.e.add_vertices((0, 0, 0, 0, 0, 0, 1))
#         self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7], self.e.g.nodes())
#         expect = [(0, 1), (0, 6), (0, 7), (1, 2), (2, 3), (3, 4), (3, 7),
#                   (4, 5), (5, 6), (6, 7)]
#         self.assertEqual(expect, self.e.g.edges())
#         self.e.g = make_cycle(7)
#         #test two
#         self.e.add_vertices((2, 0, 0, 0, 0, 0, 1))
#         self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8], self.e.g.nodes())
#         expect  = [(0, 8), (0, 1), (0, 6), (0, 7), (1, 2), (1, 7),
#                    (2, 3), (2, 7), (3, 8), (3, 4), (3, 7), (4, 5),
#                    (4, 7), (5, 6), (6, 8), (7, 8)]
#         self.assertEqual(expect, self.e.g.edges())
#         self.e.g = make_cycle(7)
#         # test three
#         self.e.add_vertices((0, 0, 0, 1, 0, 0, 3))
#         self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], self.e.g.nodes())
#         expect = [(0, 8), (0, 1), (0, 9), (0, 6), (0, 7), (1, 9), (1, 2),
#                   (2, 3), (2, 9), (3, 8), (3, 9), (3, 4), (3, 7), (4, 5),
#                   (4, 7), (5, 6), (6, 8), (6, 9), (7, 8)]
#         self.assertEqual(expect, self.e.g.edges())
