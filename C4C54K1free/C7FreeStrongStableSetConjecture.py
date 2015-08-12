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
from networkx.exception import NetworkXUnfeasible
from networkx.algorithms import maximal_independent_set
from itertools import combinations_with_replacement
from itertools import product

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

def IsStrongStableSet(G, strongStableSet):
    
    """
    -------------------------------------------------------
    This function verifies that a set of vertices is a strong
    stable set in some NetworkX graph.
    -------------------------------------------------------
    Preconditions:
        G - a NetworkX graph.
        strongStableSet - a Python list of vertices in G
    
    Postconditions: 
        returns: True if the vertices of strongStableSet are in fact
        pairwise non-adjacent and meet every maximum clique, False otherwise.
    -------------------------------------------------------
    """
    
    #Verify that the vertices are pairwise non-adjacent
    verticesArePairwiseNonAdjacent = True
    for thisNonEdge in product(strongStableSet, strongStableSet):
        if thisNonEdge[0] != thisNonEdge[1]:
            if thisNonEdge in G.edges():
                verticesArePairwiseNonAdjacent = False
                
    #Verify that the vertices meet every maximum clique
    verticesMeetEveryMaxClique = False
    maximumCliques = FindLargestCliques(G)
    for thisStableVertex in strongStableSet:
        for thisMaximumClique in maximumCliques:
            if thisStableVertex in thisMaximumClique:
                verticesMeetEveryMaxClique = True
                
    #Compute the result
    if verticesArePairwiseNonAdjacent == True and verticesMeetEveryMaxClique == True:
        result = True
    else:
        result = False
    
    return result

def FindStrongStableSet(G):
    
    """
    -------------------------------------------------------
    This function finds a strong stable set in a NetworkX graph.
    -------------------------------------------------------
    Preconditions:
        G - a NetworkX graph.
    
    Postconditions: 
        returns: result - a strong stable set in G if one exists,
        and returns [] otherwise. 
    -------------------------------------------------------
    """
    
    result = None
    maximalCliques = FindLargestCliques(G)
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

def FindStrongStableSetFast(G):
    
    """
    -------------------------------------------------------
    This function finds a strong stable set in a NetworkX graph.
    Since it uses our conjecture, it is significantly faster than
    the brute force method provided above.
    -------------------------------------------------------
    Preconditions:
        G - a NetworkX graph.
    
    Postconditions: 
        returns: result - a strong stable set in G if one exists,
        an.
        d returns [] otherwise. 
    -------------------------------------------------------
    """
    
    if W_SET != [] and T_SETS != [[] for i in range(0,3)]:
        result = [W_SET[0]]
        
        #Find the T set which joins W
        i = 0
        foundTWhichJoinsW = False
        while i < len(T_SETS) and foundTWhichJoinsW == False:
            
            for t in T_SETS[i]:
                joinedWithW = True
                for w in W_SET:
                    if (t, w) not in G.edges() and (w, t) not in G.edges():
                        joinedWithW = False
                        break
                if joinedWithW == True:
                    foundTWhichJoinsW = True #W joins T[i]
            if foundTWhichJoinsW == False:
                i += 1
                    
        #Pick 1 vertex from the other 2 T sets which do not see W
        for k in range(0, len(T_SETS)):
            
            if k != i:
                for t in T_SETS[k]:
                    foundGoodTInThisSet = False
                    if foundGoodTInThisSet == False and (t not in result):
                        goodT = True
                        for v in result:
                            if (t,v) in G.edges() or (v,t) in G.edges():
                                goodT = False
                        if goodT == True:
                            result.append(t)
                            foundGoodTInThisSet = True
                            break
                        
    elif W_SET != [] and T_SETS == [[] for i in range(0,3)]:
        result = [W_SET[0]]
            
    elif W_SET == [] and T_SETS != [[] for i in range(0,3)]:
        result = list()
        for thisTSet in T_SETS:
            if thisTSet != []:
                result.append(thisTSet[0])
    else:
        result = FindStrongStableSet(G) #Do this manually, it would be pretty trivial in this case.
        
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
                    
    #Every W is a clique
    for u in W_SET:
        for v in W_SET:
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

def TestGraph(G):
    
    """
    -------------------------------------------------------
    This function tests if a graph has the strong stable set we expect, and that the
    stable set we believe always exists is indeed valid.
    -------------------------------------------------------
    Preconditions:
        G - a NetworkX graph.
    
    Postconditions: 
        returns: returns True if the graph has a strong stable set defined 
        by our claim and if this stable is in fact stable, false otherwise.
    -------------------------------------------------------
    """
    
    strongStableSet = FindStrongStableSetFast(G)
    
    result = IsStrongStableSet(G, strongStableSet)
    
    return result

def Process():
    
    #Generate all X combos up to cardinality 1
    allXConfigs = combinations_with_replacement(range(2), r = BASE_CYCLE_LENGTH)
    #Generate all T combos up to cardinality 1
    allTConfigs = combinations_with_replacement(range(2), r = 3)
    #Generate all W combos up to cardinality 1
    allWConfigs = range(2)
    
    #Do it
    for thisXConfig in allXConfigs:
        #Test graphs with just X sets
        baseGraph = Construct(thisXConfig, [0,0,0], 0)  
        print(TestGraph(baseGraph))
        for thisTConfig in allTConfigs:
            #Test graphs with just T sets
            baseGraph = Construct([0,0,0,0,0,0], thisTConfig, 0)
            print(TestGraph(baseGraph))
            #Test graphs with only X,T sets
            baseGraph = Construct(thisXConfig, thisTConfig, 0)
            print(TestGraph(baseGraph))
            for thisWConfig in allWConfigs:
                #Test graphs with only X,W sets
                baseGraph = Construct(thisXConfig, [0,0,0], thisWConfig)
                print(TestGraph(baseGraph))
                #Test graphs with only W,T sets
                baseGraph = Construct([0,0,0,0,0,0], thisTConfig, thisWConfig)
                print(thisTConfig)
                print(thisWConfig)
                print(TestGraph(baseGraph))
                print("999")
                #Test graphs with X,W,T sets
                baseGraph = Construct(thisXConfig, thisTConfig, thisWConfig)
                #print(TestGraph(baseGraph))
    
    return

#Process()

baseGraph = Construct([0,0,0,0,0,0], [0, 0, 1], 1)
print(X_SETS)
print(T_SETS)
print(W_SET)
print(baseGraph.neighbors(7))
print(baseGraph.edges())
print(FindStrongStableSetFast(baseGraph))