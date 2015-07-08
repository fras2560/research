"""
-------------------------------------------------------
This program attempts to color (C4,C5,4K1)-free graphs
using a greedy algorithm, which colors this graph
class by removing stable sets.
-------------------------------------------------------
Author:  Tom LaMantia
Email:   lama3790@mylaurier.ca
Version: 2015-06-15
-------------------------------------------------------
"""
import sys
sys.path.append("..")
from copy import deepcopy
from graph.helper import make_cycle
from graph.colorable import valid_coloring
from networkx.algorithms import find_cliques, maximal_independent_set
from math import ceil

CYCLE_LENGTH = 7
CURRENT_X_SETS = [ [] for i in range(0, CYCLE_LENGTH)]
CURRENT_Y_SETS = [ [] for i in range(0, CYCLE_LENGTH)]

def ConstructBaseGraph():
    global CURRENT_X_SETS, CURRENT_Y_SETS
    
    CURRENT_X_SETS = [ [] for i in range(0, CYCLE_LENGTH)]
    CURRENT_Y_SETS = [ [] for i in range(0, CYCLE_LENGTH)]
    
    result = make_cycle(CYCLE_LENGTH)
    
    return deepcopy(result)

# """
# -------------------------------------------------------
# This function finds the largest clique in a NetworkX graph.
# 
# Preconditions: G, a NetworkX graph.
# 
# Postconditions: This function returns a list of lists, where each list entry
# contains a list of vertices which comprise the largest clique(s)
# in G.
# -------------------------------------------------------
# """
# def findLargestCliques(G):
#     maximalCliques = list(find_cliques(G))
#     
#     if maximalCliques == []:
#         result  = []
#     else:
#         largestSoFar = len(maximalCliques[0])
#         
#         for thisClique in maximalCliques:
#             if len(thisClique) > largestSoFar:
#                 largestSoFar = len(thisClique)
#                 
#         result = list()
#         
#         for thisClique in maximalCliques:
#             if len(thisClique) == largestSoFar:
#                 result.append(thisClique)
#                   
#     return result
# 
# """
# -------------------------------------------------------
# This function takes a NetworkX graph G and returns a strong
# stable set belonging to G, if such a stable set exists, and
# returns None otherwise.
# -------------------------------------------------------
# """
# def FindStrongStableSet(G):
#     result = None
#     maximalCliques = findLargestCliques(G)
#     
#     if maximalCliques !=  []:
#         V = G.nodes()
#     
#         for thisVertex in V:
#             #Find maximum stable sets which contain each vertex of G
#              try:
#                 verticesToInclude = list()
#                 verticesToInclude.append(thisVertex)
#                 thisMaximalStableSet = maximal_independent_set(G, verticesToInclude)
#              except NetworkXUnfeasible:
#                 thisMaximalStableSet = []
#              #Now determine if thisMaximumStableSet is strong, that is, meets every maximal clique
#              foundStrongStableSet = True
#             
#              for thisMaximalClique in maximalCliques:
#                 if set(thisMaximalStableSet).isdisjoint(set(thisMaximalClique)):
#                     foundStrongStableSet = False
#                     break
#                        
#              if foundStrongStableSet == True:
#                 result = thisMaximalStableSet
#                 break
# 
#     return result

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
    currentXAtOffset.append( (7 + offset) % 14 )
    
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

def FindGoodStableSet(G):

    graphToSearch = deepcopy(G)
    for i in range(0,6):
        graphToSearch.remove_node(i)

    for i in range(0,10):
        try:
            result = maximal_independent_set(graphToSearch)
        except IndexError:
            return None
        if len(result) == 3:
            break
    
    if len(result) != 3:
        result = None

    return result

def GreedyColoring(G):
    
    graphToTest = deepcopy(G)
    result = []
    
    thisStableSet = FindGoodStableSet(G)
    
    while thisStableSet != None:
        result.append(thisStableSet)
        for thisStableVertex in thisStableSet:
            graphToTest.remove_node(thisStableVertex)
         
        thisStableSet = FindGoodStableSet(graphToTest)
    
    V = len(G.nodes())
    while len(result) < ceil(V/3):
        result.append([])
        
    if graphToTest.nodes() != []:
        for thisUncoloredNode in graphToTest.nodes():
            for color in range(0,len(result)):
                canUseThisColor = True
                for thisColoredNode in result[color]:
                    x = thisColoredNode
                    y = thisUncoloredNode
                    if((x,y) in G.edges() or (y,x) in  G.edges()):
                        canUseThisColor = False
                if canUseThisColor == True:
                    result[color].append(thisUncoloredNode)
    return result

G = ConstructBaseGraph()
for i in range(0,7):
    G = AddXSet(G, 1, False, i)
G = AddYSet(G, 1, False, 0)

coloring = GreedyColoring(G)
print(valid_coloring(coloring,G))



