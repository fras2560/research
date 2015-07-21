import sys
sys.path.append("..") # Adds higher directory to python modules path
from itertools import product, combinations
import networkx as nx
from networkx.algorithms.operators import union
from graph.container import induced_subgraph
from graph.helper import make_cycle
from http.client import FORBIDDEN

FORBIDDEN_SUBGRAPHS = {make_cycle(4)}

def make_clique(n, vertexStartIndex):
    '''
    makes a clique of size n
    Parameters:
        n: the size of the clique (int)
    Returns:
        clique: the graph (networkx)
    '''
    clique = nx.Graph()
    for v in range(vertexStartIndex, n + vertexStartIndex):
        clique.add_node(v)
    end = len(clique.nodes())
    for target in clique.nodes():
        for source in range(target+1, end + vertexStartIndex):
            clique.add_edge(target, source)
    return clique

def GIsHFree(G, H):
    
    result = True
    
    for thisForbiddenInducedSubgraph in H:
        if induced_subgraph(G, thisForbiddenInducedSubgraph):
            result = False
            break
    return result

def calculateGraphDensity(G):
    
    E = len(G.edges())
    V = len(G.nodes())
    
    numerator = 2 * E
    denominator = V * (V - 1)
    
    result = numerator/denominator
    
    return result

def generateAllCobipartiteGraphs(c1Size, c2Size):

    c1 = make_clique(c1Size,0)
    c2 = make_clique(c2Size, c1Size)

    #allEdgeConfigurations = product(c1.nodes(), c2.nodes())
    for size in range(0, (c1Size*c2Size) + 1):
        for thisEdgeSet in combinations(product(c1.nodes(), c2.nodes()), size):
            
            graphToTest = union(c1, c2)
            
            for thisEdge in thisEdgeSet:
                graphToTest.add_edge(thisEdge[0], thisEdge[1])
                
            if GIsHFree(graphToTest, FORBIDDEN_SUBGRAPHS):
                print(thisEdgeSet)
                thisGraphDensity = calculateGraphDensity(graphToTest)
                print("Density: {0}".format(thisGraphDensity))
            graphToTest.clear()

    return

generateAllCobipartiteGraphs(3, 3)