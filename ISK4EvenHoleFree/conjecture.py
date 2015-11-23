"""
-------------------------------------------------------
conjecture
a program to check if G is (ISK4,Even-Hole)-free then the following holds:
1. G contains a stable set that eliminates all triangles
2. G has two vertices non-adjacent with d(v) <= 3
3. G has a clique cutset
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2015-09-16
-------------------------------------------------------
"""
# imports
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from networkx.algorithms import cycle_basis
from graph.clique_cutset import clique_cutset
import copy
from utility.file import File
from utility.generator import Generator
from graph.helper import make_cycle, make_clique, make_co_twin_c5
import logging
from os.path import join
from os import getcwd

# constants
REQUIREMENT = 4

logging.basicConfig(filename="d3_set_conjecture.log", level=logging.INFO,
                            format='%(asctime)s %(message)s')
LOGGER = logging.getLogger(__name__)

DROPS  = 10
FORBIDDEN = [make_clique(4), make_co_twin_c5(),make_cycle(4), make_cycle(6), make_cycle(8)]
MYPATH = join(getcwd(), "counter_example", "d3" )
GRAPH = make_cycle(5)

def go():
    print("Two v d(v1) <= d(v2) < 4")
    count = 0
    for g in Generator(GRAPH, DROPS, FORBIDDEN, logger=LOGGER).iterate():
        count += 1
        if not conjecture_holds(g):
            f = File(MYPATH, G=g, logger=LOGGER, base="")
            fp = f.save()
            LOGGER.info("Found the special graph")
            print("Found the special graph")
        if count % 1000 == 0:
            print("Checked {} graphs".format(count))
    print("Done")

def conjecture_holds(G):
    '''
    a function that checks if the above conjecture holds
    Parameters:
        G: the graph to check (networkx)
    Returns:
        valid: True if held, False otherwise (boolean)
    '''
    valid = False
#     if clique_cutset(G) is not None:
#         valid = True
#     if len(find_eliminating_set(G)) != 0 and not triangle_free(G):
#         valid = True
#     print(len(find_eliminating_set(G)) != 0, not triangle_free(G))
    if check_condition_holds(G):
        valid = True
    return valid

def check_condition_holds(g):
    '''
    a function that checks if there are two non-adjacent vertices with d(v)<=3
    Parameters:
        g: the graph to check (networkx)
    Returns:
        held: True if held, False otherwise (boolean)
    '''
    held = False # assume no
    vertices = []
    for i in range(0, len(g.nodes())):
        if g.degree(i) <= REQUIREMENT:
            vertices.append(i)
    if non_adjacent(vertices, g):
        held = True
    return held

def non_adjacent(vertices, g):
    '''
    a function that checks if the list of vertices has a pair who is non
    adjacent
    Parameters:
        vertices: the list of vertices (list)
        g: the graph to check (networkx)
    Returns:
        condition: True if is a pair, False otherwise (boolean)
    '''
    condition = False
    if len(vertices) >= 4:
        condition = True
    i = 0
    while i < len(vertices) and not condition:
        j = i+1
        neighbors = g.neighbors(vertices[i])
        while j < len(vertices) and not condition:
            if vertices[j] not in neighbors:
                condition = True
            j += 1
        i += 1
    return condition

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
class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testTriangle(self):
        c5 = make_cycle(5)
        c5.add_node(5)
        print(triangle_free(c5))


if __name__ == "__main__":
    go()