"""
-------------------------------------------------------
We conjecture that (C4,C5,4K1)-free graphs which contain
no induced C7 and a base C6 always contain a strong stable
set. We also conjecture that this stable set always contains
a vertex from W, or T, or both. We finally conclude that
if we remove successive stable sets from such graphs, then
it is the case that either W or all T sets are empty or it is
the case that W joins every T.
-------------------------------------------------------
Author:  Tom LaMantia
Email:   tom.lamantia@mail.utoronto.ca
Version: 2015-08-11
-------------------------------------------------------
"""
import sys
sys.path.append("..")
from graph.helper import make_cycle
from copy import deepcopy
from networkx.algorithms.clique import find_cliques

#Program constants
BASE_CYCLE_LENGTH = 6

#Program global variables
X_SETS = None
T_SETS = None
W_SET = None

def FindLargestCliques(G):
    
    """
    -------------------------------------------------------
    This function finds the largest clique in a NetworkX graph.
    -------------------------------------------------------
    Preconditions:
        G - a NetworkX graph.
    
    Postconditions: 
        returns: result - a list of lists, where each list entry
        contains a list of vertices which comprise the largest clique(s)
        in G.
    -------------------------------------------------------
    """
    
    maximalCliques = list(find_cliques(G))
    largestSoFar = len(maximalCliques[0])
    
    for thisClique in maximalCliques:
        if len(thisClique) > largestSoFar:
            largestSoFar = len(thisClique)
            
    result = list()
    
    for thisClique in maximalCliques:
        if len(thisClique) == largestSoFar:
            result.append(thisClique)
            
    return result

"""
-------------------------------------------------------
This function takes a NetworkX graph G and returns a strong
stable set belonging to G, if such a stable set exists, and
returns None otherwise.
-------------------------------------------------------
"""
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

def AddOptionalEdges(G, edgesToAdd):
    
    """
    -------------------------------------------------------
    This function adds optional edges to a graph.
    -------------------------------------------------------
    Preconditions:
        G- a NetworkX graph.
        edgesToAdd - a list of edge tuples
    Postconditions:
        returns:
        G - a NetworkX graph which is a copy of the input graph
            with the optional edges added.
        
    -------------------------------------------------------
    """
    
    for thisNewEdge in edgesToAdd:
        G.add_edge(thisNewEdge[0], thisNewEdge[1])
    
    return deepcopy(G)

def Construct(xVertexCardanility, tVertexCardinality, wCardinality):
    """
    -------------------------------------------------------
    This function constructs a (C4,C5,4K1)-free graph with no C7.
    -------------------------------------------------------
    Preconditions:
        xVertexCardinality - a Python list, where the ith value of the list contains the
            cardinality of the set of 3-vertices for the base C6.
        tVertexCardinality - a Python list, where the ith value of the list contains the
            cardinality of the set of 2-vertices for the base C6.
        wCardinality - a python integer, which is the cardinality of the set of 6 vertices for the
            base C6
    Postconditions:
        returns:
        G - a (C4,C5,4K1)-free  NetworkX graph with no C7
        
    -------------------------------------------------------
    """
    #Initialize global variables
    global X_SETS
    global T_SETS
    global W_SET
    
    X_SETS = [[] for i in range(0,BASE_CYCLE_LENGTH)]
    T_SETS = [[] for i in range(0,3)]
    W_SET = []

    #Initialize
    G = make_cycle(BASE_CYCLE_LENGTH)
    
    #Add the x vertices
    currentIndex = 0
    for thisXVertexSize in xVertexCardanility:
        for j in range(0, thisXVertexSize):
            vertexToAdd = G.number_of_nodes()
            G.add_node(vertexToAdd)
            X_SETS[currentIndex].append(vertexToAdd)
            #Add the edges for each X
            G.add_edge((currentIndex + 0) % BASE_CYCLE_LENGTH, vertexToAdd)
            G.add_edge((currentIndex + 1) % BASE_CYCLE_LENGTH, vertexToAdd)
            G.add_edge((currentIndex + 2) % BASE_CYCLE_LENGTH, vertexToAdd)
        currentIndex += 1
        
    #Add the t vertices
    currentIndex = 0
    k = 0
    for thisTVertexSize in tVertexCardinality:
        for j in range(0, thisTVertexSize):
            vertexToAdd = G.number_of_nodes()
            G.add_node(vertexToAdd)
            T_SETS[k].append(vertexToAdd)
            #Add the edges for each X
            G.add_edge((currentIndex) % BASE_CYCLE_LENGTH, vertexToAdd)
            G.add_edge((currentIndex + 1) % BASE_CYCLE_LENGTH, vertexToAdd)
        k += 1
        currentIndex += 2
            
    #Add the w vertices
    for j in range(0, wCardinality):
        vertexToAdd = G.number_of_nodes()
        G.add_node(vertexToAdd)
        W_SET.append(vertexToAdd)
        #Add the edges for each W
        G.add_edge((currentIndex + 0) % BASE_CYCLE_LENGTH, vertexToAdd)
        G.add_edge((currentIndex + 1) % BASE_CYCLE_LENGTH, vertexToAdd)
        G.add_edge((currentIndex + 2) % BASE_CYCLE_LENGTH, vertexToAdd)
        G.add_edge((currentIndex + 3) % BASE_CYCLE_LENGTH, vertexToAdd)
        G.add_edge((currentIndex + 4) % BASE_CYCLE_LENGTH, vertexToAdd)
        G.add_edge((currentIndex + 5) % BASE_CYCLE_LENGTH, vertexToAdd)
        
    #W joins every X
    for w in W_SET:
        for thisXSet in X_SETS:
            for x in thisXSet:
                G.add_edge(x,w)
    
    #Every X is a clique
    for thisXSet in X_SETS:
        for v in thisXSet:
            for u in thisXSet:
                if u != v:
                    G.add_edge(u,v)
                    
    #Every T is a clique
    for thisTset in T_SETS:
        for v in thisTset:
            for u in thisTset:
                if u != v:
                    G.add_edge(u,v)
    
    #If Ti is non-empty:
    currentIndex = 0
    for thisTSet in T_SETS:
        #Then Ti joins Xi, Xi+5
        for thisTVertex in thisTSet:
            for thisXVertex in X_SETS[(currentIndex) % BASE_CYCLE_LENGTH]:
                G.add_edge(thisTVertex, thisXVertex)
            for thisXVertex in X_SETS[(currentIndex + 5) % BASE_CYCLE_LENGTH]:
                G.add_edge(thisTVertex, thisXVertex)
        
            #Then Xi joins Xi+5
            for thisX1Vertex in X_SETS[(currentIndex) % 6]:
                for thisX2Vertex in X_SETS[(currentIndex + 5) % BASE_CYCLE_LENGTH]:
                    G.add_edge(thisX1Vertex, thisX2Vertex)
        currentIndex += 2
    
    return G

G = Construct([1,2,1,2,2,1], [2,1,2], 2)
print(X_SETS)
print(T_SETS)
print(W_SET)
print(G.neighbors(18))
print(FindLargestCliques(G))




