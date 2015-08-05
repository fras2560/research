import sys
from networkx.classes.function import neighbors
sys.path.append("..") # Adds higher directory to python modules path
from itertools import product, combinations
import networkx as nx
from networkx.algorithms.operators import union
from graph.container import induced_subgraph
from graph.helper import make_cycle
from http.client import FORBIDDEN

FORBIDDEN_SUBGRAPHS = {make_cycle(4)}

def MakeClique(n, vertexStartIndex):
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

def CalculateGraphDensity(G):
    
    E = len(G.edges())
    V = len(G.nodes())
    
    numerator = 2 * E
    denominator = V * (V - 1)
    
    result = numerator/denominator
    
    return result

def IsComparable(G, vertices):
    
    result = True
    
    for v in vertices:
        for u in vertices:
            if u != v:
                closedNeighbourhoodU = G.neighbors(u)
                closedNeighbourhoodV = G.neighbors(v)
                #We are only interested neighbors in the other clique!
                for thisVertex in vertices:
                    if thisVertex in closedNeighbourhoodU:
                        closedNeighbourhoodU.remove(thisVertex)
                    if thisVertex in closedNeighbourhoodV:
                        closedNeighbourhoodV.remove(thisVertex)
                
                if closedNeighbourhoodU == closedNeighbourhoodV:
                    result = False
                    break
        if result == False:
            break
        
    return result

def GenerateAllCobipartiteGraphs(c1Size, c2Size):

    c1 = MakeClique(c1Size,0)
    c2 = MakeClique(c2Size, c1Size)

    for size in range(0, (c1Size*c2Size) + 1):
        for thisEdgeSet in combinations(product(c1.nodes(), c2.nodes()), size):
            
            graphToTest = union(c1, c2)
            
            for thisEdge in thisEdgeSet:
                graphToTest.add_edge(thisEdge[0], thisEdge[1])
                
            if GIsHFree(graphToTest, FORBIDDEN_SUBGRAPHS):
                
                #Check to make sure every vertex in c1 and c2 is comparable
                if IsComparable(graphToTest, c1) == True and IsComparable(graphToTest, c2) == True:
                    print({i for i in thisEdgeSet if (i not in c1) and (i not in c2)})
                    #thisGraphDensity = CalculateGraphDensity(graphToTest)
                    #print("Density: {0}".format(thisGraphDensity))
            graphToTest.clear()
    return

GenerateAllCobipartiteGraphs(3, 3)