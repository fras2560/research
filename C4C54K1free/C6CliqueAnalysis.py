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
from networkx.algorithms.clique import find_cliques


from itertools import product

GRAPH_FAMILY = "Onion"
DIRECTORY = join(getcwd(), "GraphFamilies", GRAPH_FAMILY)
MY_LOGGER = logging.getLogger(__name__)

NUMBER_OF_LAYERS = 1
CYCLE_LENGTH = 6

X_SETS = [[] for i in range(0,CYCLE_LENGTH)]
Y_SETS = [[] for i in range(0,int(CYCLE_LENGTH/2))]

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

def Construct():
    
    global X_SETS
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
                    
                
    X_SETS = x_sets
                    
    return resultGraph
 
G = Construct()

#Lets add the Y sets
k = 0
for i in range(0,3):
    nodeToAdd = G.number_of_nodes()
    G.add_node(nodeToAdd)
    Y_SETS[i].append(nodeToAdd)
    
    G.add_edge(nodeToAdd, 0 + k)
    G.add_edge(nodeToAdd, 1 + k)
    
    G.add_edge(X_SETS[k % CYCLE_LENGTH][0], X_SETS[(k+1) % CYCLE_LENGTH][0])
    G.add_edge(X_SETS[k % CYCLE_LENGTH][0], nodeToAdd)
    G.add_edge(X_SETS[(k+1) % CYCLE_LENGTH][0], nodeToAdd)
    
    k += 2

print(X_SETS)    
print(Y_SETS)
print(G.edges())
print([(x,y) for (x,y) in G.edges() if x not in range(0,6) and y not in range(0,6)])





