"""
-------------------------------------------------------
This program analyzes (C4,C5,4K1)-free graphs.

We are primarily interested in which graphs from this class
contains a strong stable set which meets all the maximal 
cliques of the graph in question. If no such strong stable
set exists, we wonder if the chromatic number is equal
to the ceiling of n/3.
-------------------------------------------------------
Author:  Tom LaMantia
Email:   lama3790@mylaurier.ca
Version: 2015-06-15
-------------------------------------------------------
"""
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from networkx.algorithms.clique import find_cliques
import networkx as nx
from networkx.algorithms import maximal_independent_set
from networkx.exception import NetworkXUnfeasible
from math import ceil
from utility.file import File
from os import getcwd
from os.path import join
import logging
from graph.colorable import chromatic_number, valid_coloring
from graph.container import induced_subgraph
from copy import deepcopy
from graph.helper import make_cycle, make_cok4
from itertools import product

LOG_FILE_NAME = "C7_Many_X_Enumerate.log"
GRAPH_FAMILY = "NoStrongStableSet"
DIRECTORY = join(getcwd(), "GraphFamilies", GRAPH_FAMILY)
MY_LOGGER = logging.getLogger(__name__)
FORBIDDEN_SUBGRAPHS = {make_cycle(4), make_cycle(5), make_cok4()}

STABLE_SET_SEARCH_ITERATIONS = 10
Y_VERTEX_START_INDEX = 0
X_VERTEX_START_INDEX = 0
CYCLE_LENGTH = 7

CURRENT_X_SETS = None
CURRENT_Y_SETS = None

def WriteToLogFile(strMsg):
    
    logFileHandle = open(LOG_FILE_NAME, "a+", encoding = "utf-8")
    thisLine = logFileHandle.readline().strip()
    while thisLine != "":
        thisLine =  logFileHandle.readline().strip()

    print(strMsg, file = logFileHandle)
    logFileHandle.close()
    
    return

def GIsHFree(G, H):
    
    result = True
    
    for thisForbiddenInducedSubgraph in H:
        if induced_subgraph(G, thisForbiddenInducedSubgraph):
            result = False
            break
    return result

def UpdateCurrentYSets(newYSet):
    global CURRENT_Y_SETS
    CURRENT_Y_SETS = newYSet
    return

def UpdateCurrentXSets(newXSet):
    global CURRENT_X_SETS
    CURRENT_X_SETS = newXSet
    return

def ConstructOnion(number_of_layers):
    
    resultGraph = make_cycle(CYCLE_LENGTH)
    
    x_sets = [ [] for i in range(0,CYCLE_LENGTH)]
    y_sets = [ [] for i in range(0,CYCLE_LENGTH)]
    
    #Add the nodes
    for vertexIndex in range(0, number_of_layers * CYCLE_LENGTH):
        #add the new node
        vertexToAddNum = resultGraph.number_of_nodes()
        resultGraph.add_node(vertexToAddNum)
        x_sets[vertexIndex % CYCLE_LENGTH].append(vertexToAddNum)
        #add its edges
        resultGraph.add_edge( (vertexToAddNum - 1) % CYCLE_LENGTH, vertexToAddNum )
        resultGraph.add_edge( vertexToAddNum % CYCLE_LENGTH, vertexToAddNum)
        resultGraph.add_edge( (vertexToAddNum + 1) % CYCLE_LENGTH, vertexToAddNum)

    #x_i forms a clique
    for thisXSet in x_sets:
        if(len(thisXSet) > 1):
            for thisCliqueEdge in product(thisXSet, thisXSet):
                if(thisCliqueEdge[0] != thisCliqueEdge[1]):
                    resultGraph.add_edge(thisCliqueEdge[0], thisCliqueEdge[1])
                    
    #X_i joins its neighbours
    for thisXSetIndex in range(0,CYCLE_LENGTH):
        x1 = x_sets[thisXSetIndex]
        x2 = x_sets[(thisXSetIndex+1) % CYCLE_LENGTH]
        for vertexI in x1:
            for vertexJ in x2:
                resultGraph.add_edge(vertexI,vertexJ)

    UpdateCurrentXSets(x_sets)
    UpdateCurrentYSets(y_sets)        
    return resultGraph

"""
-------------------------------------------------------
Dr. Hoang conjectured that when a (C4,C5,4K1)-free graph
has a strong stable set, the chromatic number of that graph
is equal to ceil(|V|/3)

Pre-conditions: A NetworkX graph G, presumed to be (C4,C5,4K1)-free
and also presumed to contain a strong stable set. This function
will only be called when this is the case.

Post-Conditions: Returns True if chi(G) = ceil(|V|/3), False otherwise. 
-------------------------------------------------------
"""
def HoangConjecture(G):

    V = G.nodes()
    chi = ceil(len(V)/3)
    
    if chi == chromatic_number(G):
        result = True
    else:
        result = False 
    
    return result

"""
-------------------------------------------------------
This function finds the largest clique in a NetworkX graph.

Preconditions: G, a NetworkX graph.

Postconditions: This function returns a list of lists, where each list entry
contains a list of vertices which comprise the largest clique(s)
in G.
-------------------------------------------------------
"""
def findLargestCliques(G):
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

def FindStrongStableSetWithY(G):
    result = None
    maximalCliques = findLargestCliques(G)
    V = G.nodes()

    for thisVertex in [i for i in V if i > 13]:
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

def AddXSet(G, setSize, addAllOptionalXEdges, offset):
    
    currentXAtOffset = list()
    currentXAtOffset.append( (CYCLE_LENGTH + offset) % 14 )
    
    for i in range(0, setSize):
        thisXVetexToAdd = G.number_of_nodes()
        currentXAtOffset.append(thisXVetexToAdd)
        G.add_node(thisXVetexToAdd)
        CURRENT_X_SETS[(offset) % CYCLE_LENGTH].append(thisXVetexToAdd)
        
        #X is a 3-vertex
        G.add_edge((X_VERTEX_START_INDEX + offset + 0) % CYCLE_LENGTH, thisXVetexToAdd)
        G.add_edge((X_VERTEX_START_INDEX + offset - 1) % CYCLE_LENGTH, thisXVetexToAdd)
        G.add_edge((X_VERTEX_START_INDEX + offset + 1) % CYCLE_LENGTH, thisXVetexToAdd)
        
        #Xi joins X_i+1, X_i+6
        for thisXi1Vertex in CURRENT_X_SETS[(offset + 1) % CYCLE_LENGTH]:
            G.add_edge(thisXVetexToAdd, thisXi1Vertex)
            
        for thisXi6Vertex in CURRENT_X_SETS[(offset + 6) % CYCLE_LENGTH]:
            G.add_edge(thisXVetexToAdd, thisXi6Vertex)
        
        #X is a clique
        for thisCurrentXVertex in currentXAtOffset:
            if thisCurrentXVertex != thisXVetexToAdd:
                G.add_edge(thisCurrentXVertex, thisXVetexToAdd)
        
        #Add optional X edges if needed, that is: xi joins xi+2
        if addAllOptionalXEdges  == True:
            for thisXi2Vertex in CURRENT_X_SETS[(offset + 2) % CYCLE_LENGTH]:
                G.add_edge(thisXVetexToAdd, thisXi2Vertex)
        
    return deepcopy(G)

def AddYSet(G, setSize, addAllOptionalXYEdges, offset):
    
    y_sets = [ [] for i in range(0,CYCLE_LENGTH)]
    
    yNodes  =  list()
    for i in range(0, setSize):
        thisVertexIndex = G.number_of_nodes()
        yNodes.append(thisVertexIndex)
        G.add_node(thisVertexIndex)
        CURRENT_Y_SETS[(offset) % CYCLE_LENGTH].append(thisVertexIndex)
        
        #Because Stream1 has only 1 Y set (by definition), its
        #placement does not matter. All other placements are isomorphic
        G.add_edge((Y_VERTEX_START_INDEX + offset + 0) % CYCLE_LENGTH, thisVertexIndex)
        G.add_edge((Y_VERTEX_START_INDEX + offset + 1) % CYCLE_LENGTH, thisVertexIndex)
        G.add_edge((Y_VERTEX_START_INDEX + offset + 2) % CYCLE_LENGTH, thisVertexIndex)
        G.add_edge((Y_VERTEX_START_INDEX + offset + 3) % CYCLE_LENGTH, thisVertexIndex)
        
        #Yi forms a clique
        for thisYNode in yNodes:
            if thisYNode != thisVertexIndex:
                G.add_edge(thisYNode, thisVertexIndex)
        
        #yi joins Y_i+1
        for thisCurrentYi1 in CURRENT_Y_SETS[(offset + 1) % CYCLE_LENGTH]:
            G.add_edge(thisCurrentYi1, thisVertexIndex)
        #Yi joins Y_i+6    
        for thisCurrentYi6 in CURRENT_Y_SETS[(offset + 6) % CYCLE_LENGTH]:
            G.add_edge(thisCurrentYi6, thisVertexIndex)
        
        #Y1 joins Xi
        for thisCurrentXi in CURRENT_X_SETS[(1 + offset) % CYCLE_LENGTH]:
            G.add_edge(thisVertexIndex, thisCurrentXi)
            
        #Yi joins X_i+1    
        for thisCurrentXi2 in CURRENT_X_SETS[(2 + offset) % CYCLE_LENGTH]:
            G.add_edge(thisVertexIndex, thisCurrentXi2)
            
        #We must avoid 4k1
        for thisCurrentXi6 in CURRENT_X_SETS[(0 + offset) % CYCLE_LENGTH]:
            G.add_edge(thisVertexIndex, thisCurrentXi6)
            
        #The user may request optional edges, that is: Yi joins Xi+2
        if addAllOptionalXYEdges == True:
            for thisCurrentXi2 in CURRENT_X_SETS[(3 + offset) % CYCLE_LENGTH]:
                G.add_edge(thisVertexIndex, thisCurrentXi2)
                
    return deepcopy(G)

def DifferentSizeXAndDifferentSizeY(xyCardinalityUpperBound):
    
    #ALWAYS ADD X'S ***BEFORE*** adding your Y's!
    t = range(1,xyCardinalityUpperBound)
    xConfigSet = set(set(product(set(t),repeat = CYCLE_LENGTH)))
    yConfigSet = set(set(product(set(t),repeat = CYCLE_LENGTH)))
    
    badYConfigurations = set()
    #Now we need to sift through our Y sets and remove illegal ones
    #No more than 3 Y's
    for thisYConfig in yConfigSet:
        numberYSets = 0
        for i in range(0,CYCLE_LENGTH):
            if thisYConfig[i] == 2:
                numberYSets += 1;
                if thisYConfig[(i + 3) % CYCLE_LENGTH] == 2 or thisYConfig[(i + 4) % CYCLE_LENGTH] == 2:
                    badYConfigurations = badYConfigurations.union({thisYConfig})
                    break 
            if numberYSets > 3:
                badYConfigurations = badYConfigurations.union(set(thisYConfig))
                break

    yConfigSet.difference_update(badYConfigurations)
            
    # now we may construct our graphs!
    for thisXConfig in xConfigSet:
        for thisYConfig in yConfigSet:
            myGraph = ConstructOnion(1)
            for i in range(0,CYCLE_LENGTH):
                if thisXConfig[i] >= 2:
                    myGraph = AddXSet(myGraph, thisXConfig[i] - 1, False, i)
            for i in range(0,CYCLE_LENGTH):
                if thisYConfig[i] >= 2:
                    myGraph = AddYSet(myGraph, thisXConfig[i] - 1, False, i)
            
            #Since the strong stable set is probabilistic, run it a few times just in case
            #it returns None when in fact a strong stable set exists!
            for i in range(0,STABLE_SET_SEARCH_ITERATIONS):        
                thisStrongStableSet = FindStrongStableSet(myGraph)
                if thisStrongStableSet != None:
                    break
        
            if not (GIsHFree(myGraph, FORBIDDEN_SUBGRAPHS)):
                print("ERROR!")
                f = File(DIRECTORY, G = myGraph, logger = MY_LOGGER, base="C5-")
                f.save()
                exit()
             
            if thisStrongStableSet == None:
                print("G does not contain a strong stable set")
                WriteToLogFile("X Config: {0}    Y Config: {1}".format(thisXConfig, thisYConfig))
                f = File(DIRECTORY + "X_and_Y", G = myGraph, logger = MY_LOGGER, base="C5-")
                f.save()
            else:
                print("G does contain a strong stable set: {0}".format(thisStrongStableSet))
                
            myGraph.clear()

    return

def DifferentSizeXSetsNoYSetsTest(xCardinalityUpperBound):

    t = range(1,xCardinalityUpperBound)
    graphConfigSet = set(set(product(set(t),repeat = CYCLE_LENGTH)))

    for thisGraphConfiguration in graphConfigSet:
        myGraph = ConstructOnion(1)
        for thisSetIndex in range(0,CYCLE_LENGTH):
            if thisGraphConfiguration[thisSetIndex] >= 2:
                myGraph = AddXSet(myGraph, thisGraphConfiguration[thisSetIndex] - 1, False, thisSetIndex)
                 
        thisStrongStableSet = FindStrongStableSet(myGraph)
        
        if not (GIsHFree(myGraph, FORBIDDEN_SUBGRAPHS)):
            print("ERROR!")
            f = File(DIRECTORY, G = myGraph, logger = MY_LOGGER, base="C5-")
            f.save()
            exit()
         
        if thisStrongStableSet == None:
            print("G does not contain a strong stable set")
            WriteToLogFile("X Config: {0}".format(thisGraphConfiguration))
            f = File(DIRECTORY + "_X_only", G = myGraph, logger = MY_LOGGER, base="C5-")
            f.save()
        else:
            print("G does contain a strong stable set: {0}".format(thisStrongStableSet))
        myGraph.clear()

    return

WriteToLogFile("Testing: C7 with only X sets")
DifferentSizeXSetsNoYSetsTest(3)
WriteToLogFile("Testing: C7 with both X and Y sets")
DifferentSizeXAndDifferentSizeY()



