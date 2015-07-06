"""
-------------------------------------------------------
This program analyzes (C4,C5,4K1)-free graphs.

X (set of 3-vertices) has limited structure. I conjecture that
theclique number equals the chormatic number when sets of 3-vertices
are added to C7 in this graph class.

This program tests my hypothesis.
-------------------------------------------------------
Author:  Tom LaMantia
Email:   lama3790@mylaurier.ca
Version: 2015-06-15
-------------------------------------------------------
"""
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from graph.helper import make_cycle, make_cok4
from graph.container import induced_subgraph
from itertools import product, combinations
from copy import deepcopy
from utility.file import File
from os import getcwd
from os.path import join
from graph.colorable import chromatic_number
from networkx.algorithms.clique import graph_clique_number
import logging

MAX_X_CARDINALITY = 2
BASE_CYCLE_SIZE = 7
BASE_GRAPH = make_cycle(BASE_CYCLE_SIZE)
LOG_FILE_NAME = "C7_Many_X_Enumerate.log"
GRAPH_FAMILY = "(C4-C5-4k1)-free-C5-Many-Zs"
DIRECTORY = join(getcwd(), "GraphFamilies", GRAPH_FAMILY)
MY_LOGGER = logging.getLogger(__name__)
FORBIDDEN_SUBGRAPHS = {make_cok4(), make_cycle(4), make_cycle(5)}

def GIsHFree(G, H):
    
    result = True
    
    for thisForbiddenInducedSubgraph in H:
        if induced_subgraph(G, thisForbiddenInducedSubgraph):
            result = False
            break
    return result

def WriteToLogFile(strMsg):
    
    logFileHandle = open(LOG_FILE_NAME, "a+", encoding = "utf-8")
    thisLine = logFileHandle.readline().strip()
    while thisLine != "":
        thisLine =  logFileHandle.readline().strip()

    print(strMsg, file = logFileHandle)
    logFileHandle.close()
    
    return

def ConstructGraph(thisXConfiguration, thisGraph):
    
    x_sets = [[] for i in range(0,BASE_CYCLE_SIZE)]
    
    for thisXSet in enumerate(thisXConfiguration):  
        if thisXSet[1] != 0:
            for thisX in range(0,thisXSet[1]):
                #Get the node index for this node
                thisVertexIndex = thisGraph.number_of_nodes()
                #Add the newest vertex
                thisGraph.add_node(thisVertexIndex)
                
                #Keep track of the X sets
                x_sets[thisXSet[0]].append(thisVertexIndex)
                
                #Add its edges to the C7
                thisGraph.add_edge((thisXSet[0] - 1) % BASE_CYCLE_SIZE, thisVertexIndex)
                thisGraph.add_edge(thisXSet[0] % BASE_CYCLE_SIZE, thisVertexIndex)
                thisGraph.add_edge((thisXSet[0] + 1) % BASE_CYCLE_SIZE, thisVertexIndex)
                
                #This vertex is part of a clique
                for thisExistingX in x_sets[thisXSet[0]]:
                    if(thisVertexIndex != thisExistingX): #no loops!
                        thisGraph.add_edge(thisVertexIndex,thisExistingX)
                    
                #X_i joins X_i+1
                for thisXSetIndex in range(0,BASE_CYCLE_SIZE):
                    for thisMandatoryEdge in product(x_sets[thisXSetIndex], x_sets[(thisXSetIndex + 1) % BASE_CYCLE_SIZE]):
                        thisGraph.add_edge(thisMandatoryEdge[0], thisMandatoryEdge[1])
                
    return thisGraph, x_sets

def CliqueNumEqualsChromaticNum(G):
    
    result = False
    if (graph_clique_number(G) == chromatic_number(G)):
        result = True
    
    return result

def FinalProcessGraph(G):
    
    result = ""
    
    if(GIsHFree(G, FORBIDDEN_SUBGRAPHS)):
        #check that the clique number equals the chromatic number
        if CliqueNumEqualsChromaticNum(G):
            result = "Graph Passed"
        else:
            result = "Graph Failed!!"
            #save em'
            f = File(DIRECTORY, G = G, logger = MY_LOGGER, base="C5-")
            f.save()
    else:
        #Mainly for my own interest. This should never happen since we are following the rules!
        result = "CONAINS FORBIDDEN INDUCED SUBGRAPH!!"
    
    return result

def Process():
    
    for thisXConfiguration in product(range(MAX_X_CARDINALITY), repeat = BASE_CYCLE_SIZE):
        
        baseGraph = make_cycle(7)
        baseGraph, x_sets = ConstructGraph(thisXConfiguration, baseGraph)
        thisGraph = deepcopy(baseGraph)
        print(thisGraph.edges())
        #Try all possible combos of X and X_i+2 edges
        for xSetIndex in range(0,BASE_CYCLE_SIZE):
            s1 = x_sets[xSetIndex]
            s2 = x_sets[(xSetIndex + 2) % BASE_CYCLE_SIZE]
        
            for i in range(0,4):
                for thisEdgeCombo in combinations(product(s1,s2),i):
                    for thisEdge in thisEdgeCombo:
                        thisGraph.add_edge(thisEdge[0], thisEdge[1])      
                         
                    WriteToLogFile(FinalProcessGraph(thisGraph))
                
                    #for each of these combos, try it with all combos of X and X_i+5
                    thisGraphMoreJoins = deepcopy(thisGraph)
                    s1 = x_sets[xSetIndex]
                    s2 = x_sets[(xSetIndex + 5) % BASE_CYCLE_SIZE]
                    for i in range(0,4):
                        for thisEdgeCombo in combinations(product(s1,s2),i):
                            for thisEdge in thisEdgeCombo:
                                thisGraphMoreJoins.add_edge(thisEdge[0], thisEdge[1])      
                             
                            WriteToLogFile(FinalProcessGraph(thisGraphMoreJoins))
                    
                thisGraph = deepcopy(baseGraph)
                
        baseGraph.clear()
    return

Process()