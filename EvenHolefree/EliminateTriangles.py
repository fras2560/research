'''
Created on Sep 30, 2015
@summary: Program tries to find a stable set that eliminates all triangles
@author: Dallas
'''
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from networkx.algorithms import cycle_basis, triangles
import copy
from utility.file import File
from utility.generator import Generator
from graph.helper import make_cycle, make_clique
import logging
from os.path import join
from os import getcwd

BASE_NAME = "C5"

FORBIDDEN = [make_clique(4), make_cycle(4), make_cycle(6), make_cycle(8)]

BASE = make_cycle(5)
DROPS = 2
logging.basicConfig(filename=BASE_NAME+"ss_conjecture.log", level=logging.INFO,
                            format='%(asctime)s %(message)s')
LOGGER = logging.getLogger(__name__)
DIRECTORY = join(getcwd(), "special_graphs")
def go():
    print("Started")
    for g in Generator(BASE, DROPS,FORBIDDEN, logger=LOGGER).iterate():
        if len(find_eliminating_set(g)) == 0 and not triangle_free(g):
            f = File(DIRECTORY,G=g).save()
            if f is not None:
                print("Found a counter example")
    print("Finished")
def triangle_free(G):
    '''
    a function that checks if a graph G is triangle free
    Parameters:
        G: the graph to check (networkx)
    Returns:
        condition: True triangle free, False otherwise (boolean)
    '''
    cycles = cycle_basis(G, root=0)

    condition = True
    i = 0
    while condition and i < len(cycles):
        if len(cycles[i]) ==3:
            condition = False
        i += 1 
    return condition

def qsort(arr): 
    '''
    a quicksort function
    Parameters:
        arr: the array to sort (list)
    Returns:
        : a sorted array
    '''
    if len(arr) <= 1:
        return arr
    else:
        return qsort([x for x in arr[1:] if x<arr[0]]) + [arr[0]] + qsort([x for x in arr[1:] if x>=arr[0]])
def find_eliminating_set(G):
    '''
    a function to find a stable set that eliminates all triangles
    Parameters:
        G: the graph g to check (networkx)
    Returns:
        eliminating_set: the set of vertices (list)
    '''
    cycles = cycle_basis(G)
    for v in G.nodes():
        cycles += cycle_basis(G, root=v)
    triangles = []
    for cycle in cycles:
        if len(cycle) == 3 and qsort(cycle) not in triangles:
            triangles.append(qsort(cycle))
    elimintating_set = find_eliminating_set_aux(G, triangles, [])
    return elimintating_set

def find_eliminating_set_aux(G, triangles, stable):
    '''
    a recursive function to find a stable set that eliminates all triangles
    Parameters:
        G: the graph g to check (networkx)
        triangles: the list of triangles in the graph (list)
        stable: the list of stable vertices so far (list)
    Returns:
        result: the resulting stable set , empty if no stable set exists (list)
    
    '''
    if len(triangles) == 0:
        result = stable
    else:
        t_local = copy.deepcopy(triangles)
        triangle = t_local.pop()
        a = triangle[0]
        b = triangle[1]
        c = triangle[2]
        result = []
        if len(result) == 0  and not adjacent_to_vertices(a, stable, G):
            a_stable = copy.deepcopy(stable)
            if a not in a_stable:
                a_stable.append(a)
            a_stable = find_eliminating_set_aux(G, t_local, a_stable)
            if len(a_stable) > 0:
                result = copy.deepcopy(a_stable)
        if len(result) == 0 and not adjacent_to_vertices(b, stable, G):
            b_stable = copy.deepcopy(stable)
            if b not in b_stable:
                b_stable.append(b)
            b_stable = find_eliminating_set_aux(G, t_local, b_stable)
            if len(b_stable) > 0:
                result = copy.deepcopy(b_stable)
        if len(result) ==  0 and not adjacent_to_vertices(c, stable, G):
            c_stable = copy.deepcopy(stable)
            if c not in c_stable:
                c_stable.append(c)
            c_stable = find_eliminating_set_aux(G, t_local, c_stable)
            if len(c_stable) > 0:
                result = copy.deepcopy(c_stable)
    return result

def adjacent_to_vertices(vertex, vertices, G):
    '''
    a function to check if the vertex v is adjacent to all the vertices
    Parameters:
        vertex: some vertex (int)
        vertices: the list of vertices (list)
        G: the graph (networkx)
    Returns:
        condition: True if v adjacent to all v, False otherwise
    '''
    condition = False
    i = 0
    while not condition and i < len(vertices):
        if vertex in G.neighbors(vertices[i]):
            condition = True
        i += 1
    return condition

import unittest
from graph.helper import make_co_claw, make_diamond, make_claw
class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testFindEliminatinSet(self):
        expect = find_eliminating_set(make_claw())
        self.assertEqual(expect, [])
        expect = find_eliminating_set(make_diamond())
        self.assertEqual(expect, [0])
        print()
        expect = find_eliminating_set(make_clique(4))
        self.assertEqual(expect, [])

    def TestAdjacentToVertices(self):
        expect = adjacent_to_vertices(-1, [0, 1], make_claw())
        self.assertEqual(expect, False)
        expect = adjacent_to_vertices(0, [1, 2, 3], make_claw())
        self.assertEqual(expect, True)
        expect = adjacent_to_vertices(0, [2, 3], make_cycle(5))
        self.assertEqual(expect, False)

    def testTriangleFree(self):
        G = make_cycle(4)
        self.assertEqual(triangle_free(G), True)
        G = make_claw()
        self.assertEqual(triangle_free(G), True)
        G = make_co_claw()
        self.assertEqual(triangle_free(G), False)
        G = make_diamond()
        self.assertEqual(triangle_free(G), False)

if __name__ == "__main__":
    go()