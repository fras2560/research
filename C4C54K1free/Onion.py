"""
-------------------------------------------------------
This program analyzes (C4,C5,4K1)-free "Onion" graphs.

For these purposes, an "Onion" is a n-cycle with n distinct
3-vertices. As the size of these sets increases, we add successive
"layers" to our onion.

This program generates onions with 3-vertices on cycles of 
any length with X sets of any cardinality.

Might be useful. It generates some really cool looking graphs
when you load the saved ones into our Induced Subgraph program!!!!
-------------------------------------------------------
Author:  Tom LaMantia
Email:   lama3790@mylaurier.ca
Version: 2015-06-15
-------------------------------------------------------
"""
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from graph.helper import make_cycle, make_cok4
from utility.file import File
from os import getcwd
from os.path import join
import logging
from graph.colorable import chromatic_number
from networkx.algorithms.clique import graph_clique_number
from itertools import product

GRAPH_FAMILY = "Onion"
DIRECTORY = join(getcwd(), "GraphFamilies", GRAPH_FAMILY)
MY_LOGGER = logging.getLogger(__name__)

NUMBER_OF_LAYERS = 2
CYCLE_LENGTH = 7

def Construct():
    
    resultGraph = make_cycle(CYCLE_LENGTH)
    
    x_sets = [ [] for i in range(0,CYCLE_LENGTH)]
    
    #Add the nodes
    for vertexIndex in range(0, NUMBER_OF_LAYERS * CYCLE_LENGTH):
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
                    
    return resultGraph
 
result = Construct()
print("Clique number: {0}".format(graph_clique_number(result)))
# f = File(DIRECTORY, G = result, logger = MY_LOGGER, base="C5-")
# f.save()
