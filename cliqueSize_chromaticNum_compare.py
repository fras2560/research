"""
-------------------------------------------------------
This program looks at (C4, C6, 4K1)-free graphs which are created by adding 3-vertices to a cycle of
length 5. This program looks at 2 distinct sets of 3-vertices with equal cardinality. This program
attempts to find such graphs where the chromatic number is not equal to the clique size, if such 
graphs exist (we suspect not). 
-------------------------------------------------------
Author:  Tom LaMantia, Dallas Fraser, Kevin Holmes
Email:   lama3790@mylaurier.ca
Version: 2015-06-04
-------------------------------------------------------
"""
from graph.helper import make_cycle, make_cok4
from graph.container import induced_subgraph
from graph.colorable import chromatic_number
from itertools import product, repeat, combinations
import unittest
import copy
from networkx.algorithms.clique import graph_clique_number

MAX_Z_SIZE = 3
FORBIDDEN = {make_cok4(), make_cycle(4), make_cycle(6)}
LOG_FILE_NAME = "C5_Z_CliqueSize_ChromaticNum.log"

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
def ChromaticNumberEqualsCLiqueNumber(G):
    
    if(chromatic_number(G) == graph_clique_number(G)):
        result = True
    else:
        result = False
    
    return result

"""
-------------------------------------------------------
This function determines if a given graph is H-free
-------------------------------------------------------
Preconditions:
    G: a Networkx graph
    H: a set of Networkx graphs
Postconditions:
    Returns True if no graph in H is an induced subgraph of G,
    False otherwise.
-------------------------------------------------------
"""
def IsHFreeGraph(H,G):
    
    result = True
    for thisForbiddenGraph in H:
        if induced_subgraph(G, thisForbiddenGraph):
            result = False
            break
        
    return result

"""
-------------------------------------------------------
This function writes a message to a log file
-------------------------------------------------------
Preconditions:
    str: a message to output to the log file
Postconditions:
    str is written to the log file
-------------------------------------------------------
"""
def LogGraphInfo(str):
    
    myLogFile = open(LOG_FILE_NAME, "a+", encoding = 'utf-8')
    thisEntry = myLogFile.readline().strip()
    
    while thisEntry != "":
        thisEntry = myLogFile.readline().strip()
        
    print("{0}" .format(str), file = myLogFile)
    
    myLogFile.close()
    return


"""
-------------------------------------------------------
This function constructs a base graph, which is a C5 and
2 3-vertex sets
-------------------------------------------------------
Preconditions:
    zSize: an integer which specifies the size of both 3-vertex
    sets
Postconditions:
    Returns a Networkx graph which models a C5 with Z0, Z1 such
    that the size of both 3-vertex sets is equal to zSize. 
-------------------------------------------------------
"""
def ConstructGraph(zSize):
    
    thisGraph = make_cycle(5)
    firstZVertices = set()
    secondZVertices = set()
    
    #add the z vertices
    for i in range(1, zSize + 1):
        #add the vertices in Zi
        thisNodeIndex = thisGraph.number_of_nodes()
        thisGraph.add_node(thisNodeIndex)
        firstZVertices.add(thisNodeIndex)
        #add the vertices in Zi+1
        thisNodeIndex = thisGraph.number_of_nodes()
        thisGraph.add_node(thisNodeIndex)
        secondZVertices.add(thisNodeIndex)
        
    #add the edges for Zi
    for vertex in firstZVertices:
        thisGraph.add_edge(0,vertex)
        thisGraph.add_edge(1,vertex)
        thisGraph.add_edge(2,vertex)
        
    #zi forms a clique
    for edge in product(firstZVertices, repeat = 2):
        #Loops are not allowed
        if edge[0] != edge[1]:
            thisGraph.add_edge(edge[0],edge[1])
        
    #add the edges for Zi+1
    for vertex in secondZVertices:
        thisGraph.add_edge(1,vertex)
        thisGraph.add_edge(2,vertex)
        thisGraph.add_edge(3,vertex)
        
    #zi+1 forms a clique
    for edge in product(secondZVertices,repeat = 2):
        if edge[0] != edge[1]:
            thisGraph.add_edge(edge[0], edge[1])
    
    return thisGraph, firstZVertices, secondZVertices

"""
-------------------------------------------------------
This function constructs all the possible edge combinations between
a given base graph over a range of Z sizes.
-------------------------------------------------------
Preconditions: None
Postconditions:
    After constructing each graph, this function checks that it does not
    contain a forbidden induced subgraph. If it does not, the clique number
    of the graph in question is compared to the chromatic number. The result
    of this test is then written to the log file. 
-------------------------------------------------------
"""
def Process():
    
    currentZSize = 1
    
    #construct each graph
    while currentZSize <= MAX_Z_SIZE:
        
        LogGraphInfo("Checking graphs with |Zi| = |Zi+1| = " + str(currentZSize))
        
        thisGraph, firstZVertices, secondZVertices = ConstructGraph(currentZSize)
        baseGraph = copy.deepcopy(thisGraph)
        
        #Look at all possible edge configurations between the two Z sets
        
        #Create a set of all edges
        allPossibleEdges = set()
        for i in product(firstZVertices, secondZVertices):
            allPossibleEdges.add(i)
            
        #Now, we need to look at/create all possible graphs we can create from Zi and Zi+1
        for i in range(0, 2 * currentZSize + 1):
            for thisCombination in combinations(allPossibleEdges,i):
                for edge in thisCombination:
                    thisGraph.add_edge(edge[0], edge[1]) #create the graph for each config
                    
                #Now we need to make sure the graph we created is (4k1, C4, C6)-free
                if IsHFreeGraph(FORBIDDEN, thisGraph):
                    if ChromaticNumberEqualsCLiqueNumber(thisGraph):
                        LogGraphInfo("Graph Passed.")
                    else:
                        LogGraphInfo("Graph Failed.")
                
                thisGraph.clear()
                thisGraph = copy.deepcopy(baseGraph)
                    
        currentZSize += 1
        thisGraph.clear()
        baseGraph.clear()
    
    return

#Initiate graph processing   
Process()
