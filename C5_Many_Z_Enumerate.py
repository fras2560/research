"""
-------------------------------------------------------
This program generates C5 with 5 sets of Z vertices. The program assumes
that all possible Z sets are non-empty and have cardinality 1 or 2. All 
dge permutations of these graphs are generated and the clique number of
each graph is compared against the largest clique size. Graphs where 
these two values are not equal are considered failed and are saved.
-------------------------------------------------------
Author:  Tom LaMantia, Dallas Fraser, Kevin Holmes
Email:   lama3790@mylaurier.ca, fras2560@mylaurier.ca
Version: June 10, 2015
-------------------------------------------------------
"""
from graph.helper import make_cycle, make_cok4
from graph.container import induced_subgraph
from copy import deepcopy
from itertools import product
from file import File
from os import getcwd
from os.path import join
from graph.colorable import chromatic_number
from networkx.algorithms.clique import graph_clique_number
import logging

LOG_FILE_NAME = "CS_Many_Z_Enumerate.log"
GRAPH_FAMILY = "(C4-C6-4k1)-free-C5-Many-Zs"
DIRECTORY = join(getcwd(), "GraphFamilies", GRAPH_FAMILY)
MY_LOGGER = logging.getLogger(__name__)

NUMBER_OF_Z_SETS = 5
Z_SETS = []
FORBIDDEN_INDUCED_SUBGRAPHS = {make_cok4(), make_cycle(4), make_cycle(6)}

def WriteToLogFile(strMsg):
    
    logFileHandle = open(LOG_FILE_NAME, "a+", encoding = "utf-8")
    thisLine = logFileHandle.readline().strip()
    while thisLine != "":
        thisLine =  logFileHandle.readline().strip()

    print(strMsg, file = logFileHandle)
    logFileHandle.close()
    
    return

"""
-------------------------------------------------------
This function determines if the clique number of some arbitrary
graph G equals the chromatic number
-------------------------------------------------------
Preconditions:
    G: a Networkx graph
Postconditions:
    Returns True if the clique number of G equals the chromatic number
    of G, False otherwise.
-------------------------------------------------------
"""
def CliqueNumEqualsChromaticNum(G):
    
    result = False
    if (graph_clique_number(G) == chromatic_number(G)):
        result = True
    
    return result

"""
-------------------------------------------------------
This function determines if a given graph is H-free
-------------------------------------------------------
Preconditions:
    G: a Networkx graph
    H: a set of Networkx graphs
Postconditions:
    Returns True if G has no induced subgraph contained in H
-------------------------------------------------------
"""
def GIsHFree(G, H):
    
    result = True
    
    for thisForbiddenInducedSubgraph in H:
        if induced_subgraph(G, thisForbiddenInducedSubgraph):
            result = False
            break
    return result

"""
-------------------------------------------------------
This function generates all the possible configurations
of Z vertices.
-------------------------------------------------------
Preconditions: none

Post-conditions: Returns an array of tuples, where each
tuple in the array represents the encoding of the cardinality
of our 5 sets of Z's. Each tuple consists of 5 integers, each of which
are 1 or 2. The ith integer in each tuple represents the cardinality 
of Zi in each configuration.
-------------------------------------------------------
"""
def GenerateZSetPossibilities():
    return list(product(range(1,3),repeat = NUMBER_OF_Z_SETS))

"""
-------------------------------------------------------
This function constructs a 5-cycle with 5 sets of Z vertices.
-------------------------------------------------------
Preconditions: 
G - a Networkx graph G
additionalEdges - a tuple of integers (0 or 1), where the ith integer
corresponds to the existence of an edge between vertex i,i+1.

Post-conditions: The edges encoded in the tuple given by
addditionalEdges are added to G.
-------------------------------------------------------
"""
def AddEdges(G, additionalEdges, allZVertices):
    
    for i in range(0,len(additionalEdges)):
        if additionalEdges[i] != 0:
            G.add_edge(allZVertices[i], allZVertices[(i+1) % len(additionalEdges)])
    return

"""
-------------------------------------------------------
This function constructs a 5-cycle with 5 sets of Z vertices.
-------------------------------------------------------
Preconditions: none

Post-conditions: Returns a 5-cycle Networkx graph with 5
unique sets of 3-vertices (of type Z). 
-------------------------------------------------------
"""
def ConstructBaseGraph():
    
    baseGraph = make_cycle(5)
    
    for i in range(0,NUMBER_OF_Z_SETS):
        #add this Z vertex
        thisNodeIndex = baseGraph.number_of_nodes()
        baseGraph.add_node(thisNodeIndex)
        Z_SETS.append([thisNodeIndex])
        #add Z edges
        baseGraph.add_edge((i-1) % NUMBER_OF_Z_SETS, thisNodeIndex)
        baseGraph.add_edge(i % NUMBER_OF_Z_SETS ,thisNodeIndex)
        baseGraph.add_edge((i+1) % NUMBER_OF_Z_SETS, thisNodeIndex)
        
    return baseGraph

"""
-------------------------------------------------------
This function generates all possible graphs from the base
graph, checks that they are free of forbidden induced subgraphs
and calls helper functions to carry out graph processing.
-------------------------------------------------------
"""
def Process():

    allZSetPossibilities = GenerateZSetPossibilities()
    thisGraph = ConstructBaseGraph()
    
    for thisZConfig in allZSetPossibilities:
        #add the extra Z's (and appropriate edges) if needed
        for thisZ in enumerate(thisZConfig):
            if thisZ[1] != 1:
                #add the extra node
                nodeIndex = thisGraph.number_of_nodes()
                thisGraph.add_node(nodeIndex)
                Z_SET[thisZ[0]].append(nodeIndex)
                #Z forms a clique
                for thisExistingZ in Z_SETS[thisZ[0]]:
                    if nodeIndex != thisExistingZ:
                        thisGraph.add_edge(nodeIndex, thisExistingZ)
                #add the edges for C5
                    thisGraph.add_edge((thisZ[0] - 1) % NUMBER_OF_Z_SETS, nodeIndex)
                    thisGraph.add_edge(thisZ[0] % NUMBER_OF_Z_SETS, nodeIndex)
                    thisGraph.add_edge((thisZ[0] + 1) % NUMBER_OF_Z_SETS, nodeIndex)
                    
        #generate all possible edge permutations
        allZVertices = []
        for thisZSet in Z_SETS:
            for thisZ in thisZSet:
                allZVertices.append(thisZ)

        graphToTest = deepcopy(thisGraph)
        for thisEdgePosssibility in product(range(2),repeat = len(allZVertices)):
            #add each of these edge sets to the graph we will test
            AddEdges(graphToTest, thisEdgePosssibility, allZVertices)
            #Check to ensure it does not contain a forbidden induced subgraph
            
            if GIsHFree(graphToTest, FORBIDDEN_INDUCED_SUBGRAPHS):
                #Check that the clique number is equal to the chromatic number
                if CliqueNumEqualsChromaticNum(graphToTest):
                    WriteToLogFile("Graph Passed.")
                else:
                    WriteToLogFile("Graph Failed!")
                    f = File(DIRECTORY, G = graphToTest, logger = MY_LOGGER, base="C5-")
                    f.save()
                    
            graphToTest.clear()
            graphToTest = deepcopy(thisGraph)
        quit()

    return

#G1 doit
Process()