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
from itertools import product, repeat
import unittest
from networkx.algorithms.clique import graph_clique_number

MAX_Z_SIZE = 10
FORBIDDEN = {make_cok4(), make_cycle(4), make_cycle(6)}
LOG_FILE_NAME = "C5_Z_CliqueSize_ChromaticNum.log"

def chromaticNumberEqualsCLiqueNumber(g):
    
    if(chromatic_number(g) == graph_clique_number(g)):
        result = True
    else:
        result = False
    
    return result

def isHFreeGraph(H,g):
    
    result = True
    for thisForbiddenGraph in H:
        if induced_subgraph(g, thisForbiddenGraph):
            result = False
            break
        
    return result

def logGraphInfo(str):
    
    myLogFile = open(LOG_FILE_NAME, "a+", encoding = 'utf-8')
    thisEntry = myLogFile.readline().strip()
    
    while thisEntry != "":
        thisEntry = myLogFile.readline().strip()
        
    print(str, file = myLogFile)
    
    myLogFile.close()
    return

def constructGraphs():
    
    currentZSize = 1
    
    #construct each graph
    while currentZSize <= MAX_Z_SIZE:
        
        logGraphInfo("Checking graphs with |Z| = " + str(currentZSize))
        thisGraph = make_cycle(5)
        firstZVertices = set()
        secondZVertices = set()
        
        #add the z vertices
        for i in range(1,currentZSize + 1):
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
            
        #Look at all possible edge configurations
        for vertexI in firstZVertices:
             for vertexZ in secondZVertices:
                 thisGraph.add_edge(vertexI, vertexZ)
                 #check that this graph does not contain a forbidden induced subgraph
                 if isHFreeGraph(FORBIDDEN, thisGraph):
                     #check that the clique size is equal to the chromatic number
                     if chromaticNumberEqualsCLiqueNumber(thisGraph):
                         logGraphInfo("Graph Passed.")
                     else:
                        logGraphInfo("Graph Failed!")
                        
                 else:
                     thisGraph.remove_edge(vertexI, vertexZ)
                    
        currentZSize += 1
        thisGraph.clear()
    
    return

class Tester(unittest.TestCase):
     
    def setUp(self):
        print("Starting Tests")
        pass
     
    def testProcess(self):
         
        constructGraphs()
         
        return