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
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from graph.helper import make_cycle, make_cok4
from os import getcwd
from os.path import join
from utility.file import File
from itertools import combinations_with_replacement, permutations
from graph.container import induced_subgraph
import logging

FAMILY = "(C4,C6,4K1)-free"
DIRECTORY = join(getcwd(), 'GraphFamilies', FAMILY)
YIVALUE = 1
ZIVALUE = 2
BASE = make_cycle(7)
FORBIDDEN = [make_cycle(4), make_cycle(6), make_cok4()]
BOTH = 3
logging.basicConfig(filename=FAMILY + "Enumerate.log", level=logging.INFO, format='%(asctime)s %(message)s')
LOGGER = logging.getLogger(__name__)

def add_vertices(G, permutation):
    ypositions = [0, 0, 0, 0, 0, 0, 0]
    zpositions = [0, 0, 0, 0, 0, 0, 0]
    vertex = 7
    for i, value  in enumerate(permutation):
        if value == YIVALUE or value == BOTH:
            #add the new Y vertex and its edges
            G.add_node(vertex)
            G.add_edge(vertex, i)
            G.add_edge(vertex, (i+1) % 7)
            G.add_edge(vertex, (i+4) % 7)
            #Give this Y vertex a unique identifier and draw edges between new vertices if needed
            for x in range(i, -1, -1):
                if ypositions[x] > 0 and vertex - x != 2 :
                    G.add_edge(vertex, ypositions[x])
                    
                if zpositions[x] > 0:
                    G.add_edge(vertex, zpositions[x])
            ypositions[i] = vertex
            vertex += 1
        if value == ZIVALUE or value == BOTH:
            #add the new Z vertex and its edges
            G.add_node(vertex)
            G.add_edge(vertex, i)
            G.add_edge(vertex, (i+1) % 7)
            G.add_edge(vertex, (i+2) % 7)
            G.add_edge(vertex, (i+3) % 7)
            G.add_edge(vertex, (i+4) % 7)
            #Give this Y vertex a unique identifier and draw edges between new vertices if needed
            for x in range(i, -1, -1):
                if ypositions[x] > 0:
                    G.add_edge(vertex, ypositions[x])
                if zpositions[x] > 0:
                    G.add_edge(vertex, zpositions[x])
            zpositions[i] = vertex
            vertex += 1
    return

def count(combo):
    verticesAdded = 0
    for x in combo:
        if x == YIVALUE or x ==  ZIVALUE:
            verticesAdded += 1
        if x == BOTH:
            verticesAdded += 1 #we already counted one vertex, now we need to count the other too.
    return verticesAdded

def process():
    index = 0
    #Generate an array corresponding to the k-vertices we want to add to c7
    for add in combinations_with_replacement(range(4), 7):
        print(add)
        #We can have at most 3 Z's and 2 Y's, making 5 possible vertices we can add
        if count(add) > 5:
            break
        for thisPermutation in permutations(add):
            #copy initial graph (c7) and add vertices
            #self.g = BASE.copy()
            g = make_cycle(7)
            add_vertices(g, thisPermutation)
            check = True
            #we want our graph to remain {4k1,c4,c6}-free
            for H in FORBIDDEN:
                if induced_subgraph(g, H):
                    check  = False
                    break
            if check:
                #log it
                f = File(DIRECTORY, G=g, logger=LOGGER, base="C5-")
                fp = f.save()
                if fp is not None:
                    index += 1
                    print("Created Graph: %d" % index)

process()