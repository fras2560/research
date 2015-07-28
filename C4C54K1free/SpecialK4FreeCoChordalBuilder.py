import sys
sys.path.append("..")
from graph.container import induced_subgraph
from graph.helper import make_cycle, make_claw
import networkx as nx

def constructGn(rows, cols):
    A_VERTICES = list()
    B_VERTICES = list()
    C_VERTICES = list()
    
    #Initialize networkX graph
    G = nx.Graph()
    
    #Populate the A vertices
    for i in range(0,rows):
        A_VERTICES.append(i)
        G.add_node(i)
    
    #Populate the B vertices
    for i in range(G.number_of_nodes(), G.number_of_nodes() + cols):
        B_VERTICES.append(i)
        G.add_node(i)
    
    #Each A vertex forms a join to each B vertex
    for thisAVertex in A_VERTICES:
        for thisBVertex in B_VERTICES:
            G.add_edge(thisAVertex, thisBVertex)
            
    #Populate the C vertices and create the necessary edges        
    for i in range(0,rows):
        for j in range(0,cols):
            vertexToAdd = G.number_of_nodes()
            G.add_node(vertexToAdd)
            C_VERTICES.append(vertexToAdd)
            
            for thisAVertex in A_VERTICES:
                if thisAVertex >= i:
                    G.add_edge(vertexToAdd, thisAVertex)
                    
            for thisBVertex in B_VERTICES:
                if (thisBVertex - 2) >= j:
                    G.add_edge(vertexToAdd, thisBVertex)
    return G
                
G = constructGn(3, 3)

#Check for forbidden subgraphs
if not induced_subgraph(G, make_cycle(5)):
    print("G has no induced C5!!!")
if not induced_subgraph(G, make_cycle(6)):
    print("G has no induced C6!!!")
    


