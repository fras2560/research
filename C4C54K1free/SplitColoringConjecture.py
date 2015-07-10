"""
-------------------------------------------------------
If a graph G is split into two subgraphs, A and B, then
chi(G) <= chi(A) + chi(B). In the case of (C4,C5,4k1)-free
graphs, we conjecture a stronger result: chi(G) = chi(A) + chi(B),
where A consists of all stable sets of size 3 in G and B is
the perfect graph comprised of all vertices in G which are
not in A. 
-------------------------------------------------------
Author:  Tom LaMantia
Email:   lama3790@mylaurier.ca
Version: 2015-09-15
-------------------------------------------------------
"""
import sys
sys.path.append("..")
from graph.helper import make_cycle
from graph.container import induced_subgraph
from graph.dcolor import Dcolor
from networkx.algorithms import maximal_independent_set
from copy import deepcopy
import logging
from utility.file import File
from os import getcwd
from os.path import join
from itertools import product
import networkx as nx
from networkx import convert_node_labels_to_integers
from networkx.algorithms import find_cliques

GRAPH_FAMILY = "SplitConjecture"
DIRECTORY = join(getcwd(), "GraphFamilies", GRAPH_FAMILY)
MY_LOGGER = logging.getLogger(__name__)

CYCLE_LENGTH = 7
CURRENT_X_SETS = [ [] for i in range(0, CYCLE_LENGTH)]
CURRENT_Y_SETS = [ [] for i in range(0, CYCLE_LENGTH)]

def ConstructBaseGraph():
    global CURRENT_X_SETS, CURRENT_Y_SETS
    
    CURRENT_X_SETS = [ [i] for i in range(0, CYCLE_LENGTH)]
    CURRENT_Y_SETS = [ [] for i in range(0, CYCLE_LENGTH)]
    
    result = make_cycle(CYCLE_LENGTH)
    
    return deepcopy(result)

def AddYSet(G, setSize, addAllOptionalXYEdges, offset):
    
    y_sets = [ [] for i in range(0,CYCLE_LENGTH)]
    
    yNodes  =  list()
    for i in range(0, setSize):
        thisVertexIndex = G.number_of_nodes()
        yNodes.append(thisVertexIndex)
        G.add_node(thisVertexIndex)
        CURRENT_Y_SETS[(offset) % 7].append(thisVertexIndex)
        
        #Because Stream1 has only 1 Y set (by definition), its
        #placement does not matter. All other placements are isomorphic
        G.add_edge((offset + 0) % 7, thisVertexIndex)
        G.add_edge((offset + 1) % 7, thisVertexIndex)
        G.add_edge((offset + 2) % 7, thisVertexIndex)
        G.add_edge((offset + 3) % 7, thisVertexIndex)
        
        #Yi forms a clique
        for thisYNode in yNodes:
            if thisYNode != thisVertexIndex:
                G.add_edge(thisYNode, thisVertexIndex)
        
        #yi joins Y_i+1
        for thisCurrentYi1 in CURRENT_Y_SETS[(offset + 1) % 7]:
            G.add_edge(thisCurrentYi1, thisVertexIndex)
        #Yi joins Y_i+6    
        for thisCurrentYi6 in CURRENT_Y_SETS[(offset + 6) % 7]:
            G.add_edge(thisCurrentYi6, thisVertexIndex)
        
        #Y1 joins Xi
        for thisCurrentXi in CURRENT_X_SETS[(1 + offset) % 7]:
            G.add_edge(thisVertexIndex, thisCurrentXi)
            
        #Yi joins X_i+1    
        for thisCurrentXi2 in CURRENT_X_SETS[(2 + offset) % 7]:
            G.add_edge(thisVertexIndex, thisCurrentXi2)
            
        #We must avoid 4k1
        for thisCurrentXi6 in CURRENT_X_SETS[(0 + offset) % 7]:
            G.add_edge(thisVertexIndex, thisCurrentXi6)
            
        #The user may request optional edges, that is: Yi joins Xi+2
        if addAllOptionalXYEdges == True:
            for thisCurrentXi2 in CURRENT_X_SETS[(3 + offset) % 7]:
                G.add_edge(thisVertexIndex, thisCurrentXi2)
                
    return deepcopy(G)

def AddXSet(G, setSize, addAllOptionalXEdges, offset):
    
    currentXAtOffset = list()
    currentXAtOffset.append( offset % 7)
    
    for i in range(0, setSize):
        thisXVetexToAdd = G.number_of_nodes()
        currentXAtOffset.append(thisXVetexToAdd)
        G.add_node(thisXVetexToAdd)
        CURRENT_X_SETS[(offset) % 7].append(thisXVetexToAdd)
        
        #X is a 3-vertex
        G.add_edge((offset + 0) % 7, thisXVetexToAdd)
        G.add_edge((offset - 1) % 7, thisXVetexToAdd)
        G.add_edge((offset + 1) % 7, thisXVetexToAdd)
        
        #Xi joins X_i+1, X_i+6
        for thisXi1Vertex in CURRENT_X_SETS[(offset + 1) % 7]:
            G.add_edge(thisXVetexToAdd, thisXi1Vertex)
            
        for thisXi6Vertex in CURRENT_X_SETS[(offset + 6) % 7]:
            G.add_edge(thisXVetexToAdd, thisXi6Vertex)
        
        #X is a clique
        for thisCurrentXVertex in currentXAtOffset:
            if thisCurrentXVertex != thisXVetexToAdd:
                G.add_edge(thisCurrentXVertex, thisXVetexToAdd)
        
        #Add optional X edges if needed, that is: xi joins xi+2
        if addAllOptionalXEdges  == True:
            for thisXi2Vertex in CURRENT_X_SETS[(offset + 2) % 7]:
                G.add_edge(thisXVetexToAdd, thisXi2Vertex)
        
    return deepcopy(G)

# def FindGoodStableSet(G):
# 
#     result = None
#     
#     while result == None:
#             result = maximal_independent_set(G)
#             if len(result) != 3:
#                 result = None
#     return result

def findLargestCliques(G):
    maximalCliques = list(find_cliques(G))
    
    if maximalCliques != []:
        largestSoFar = len(maximalCliques[0])
        
        for thisClique in maximalCliques:
            if len(thisClique) > largestSoFar:
                largestSoFar = len(thisClique)
                
        result = list()
        
        for thisClique in maximalCliques:
            if len(thisClique) == largestSoFar:
                result.append(thisClique)
    else:
        result = None
            
    return result

def FindStrongStableSet(G):
    result = None
    maximalCliques = findLargestCliques(G)
    V = G.nodes()

    for thisVertex in V:
        #Find maximum stable sets which contain each vertex of G
         try:
            verticesToInclude = list()
            verticesToInclude.append(thisVertex)
            thisMaximalStableSet = maximal_independent_set(G, verticesToInclude)
         except NetworkXUnfeasible:
            thisMaximalStableSet = []
         #Now determine if thisMaximumStableSet is strong, that is, meets every maximal clique
         foundStrongStableSet = True
        
         for thisMaximalClique in maximalCliques:
            if set(thisMaximalStableSet).isdisjoint(set(thisMaximalClique)):
                foundStrongStableSet = False
                break
                   
         if foundStrongStableSet == True:
            result = thisMaximalStableSet
            break

    return result

def TheAlgorithm(G):
    
    dColor = Dcolor(G)
    partialColoring = list()
    
    #Compute chi(G) (using brute force)
    k = len(dColor.color())
    
    stillHasInducedC7 = True
    while stillHasInducedC7 == True:
        #Since G has an induced C7, a strong stable set of size 3 must exist. Find it.
        thisStableSet = FindStrongStableSet(G)
        partialColoring.append(list(thisStableSet))
        
        #Remove this stable set from the graph
        for thisStableVertex in thisStableSet:
            G.remove_node(thisStableVertex)
            
        #check for induced C7
        graphToTest = convert_node_labels_to_integers(G, 0, ordering='default', label_attribute = None)
        if induced_subgraph(graphToTest, make_cycle(7)) == None:
            stillHasInducedC7 = False
        graphToTest.clear()
            
    """        
    At this point, there does not exist a strong stable set of size 3, because there is no C7.
    This means that G is now a perfect graph.
    """
    dColor2 = Dcolor(deepcopy(G))
    t = len(dColor2.color())

    #Find the chromatic number of our partial graph of stable sets
    s = len(partialColoring)

    if k == (s + t):
        print("Conjecture Holds!")
        print(partialColoring)
        print(s,t)
        print(G.nodes())
        print(G.edges())
    else:
        print('Conjecture fails.')
        print(partialColoring)
        print(s,t)
        print(G.nodes())
        print(G.edges())

    return

myGraph = ConstructBaseGraph()
for i in range(0,CYCLE_LENGTH):
    myGraph = AddXSet(myGraph, 1, False, i)
myGraph = AddYSet(myGraph, 1, False, 0)
myGraph = AddYSet(myGraph, 1, False, 1)

TheAlgorithm(myGraph)

# thisStrongStableSet = FindStrongStableSet(myGraph)
# 
# while thisStrongStableSet != None:
#     print(thisStrongStableSet)
#     for thisStableVertex in thisStrongStableSet:
#         myGraph.remove_node(thisStableVertex)
#     thisStrongStableSet = FindStrongStableSet(myGraph)
# 
# print(chromatic_number(myGraph))
