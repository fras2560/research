"""
-------------------------------------------------------
graph
A place holder for the graph package
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-10
-------------------------------------------------------
"""
import networkx as nx
class DalGraph():
    def __init__(self, graph=None):
        '''
        init
            Parameters:
                graph: the existing networkx graph, default to None (Graph)
        '''
        if graph is None:
            self._g = nx.Graph()
        else:
            self._g = graph

    def clique_number(self):
        '''
        is_clique
        returns the clique number of the graph
            Parameters:
                None
            Returns:
                int: the clique number 
                None if not a clique
        '''
        edges = self._g.number_of_edges()
        nodes = self._g.number_of_nodes()
        clique = None
        if edges == (nodes * (nodes-1) / 2):
            # is a clique (k=#nodes)
            clique = nodes
        return clique

    def hole_number(self):
        '''
        hole_number
        return the hole number (cycle number) of the graph
            Parameters:
                None
            Returns:
                int: the hole number
                None if not a cycle
        '''
        edges = self._g.number_of_edges()
        nodes = self._g.number_of_nodes()
        hole = nodes
        if edges != nodes:
            hole = None
        if hole:
            vertex = 0
            while hole and vertex < nodes:
                neighbours = self._g.neighbors(vertex)
                expect = sorted([(vertex-1) % nodes, (vertex+1) % nodes])
                if sorted(neighbours) != expect :
                    hole = None
                vertex += 1
        return hole
