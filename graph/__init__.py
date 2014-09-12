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
import helper
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
        self.claw = helper.make_claw()
        self.co_claw = helper.make_co_claw()
        

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

    def k_critical(self):
        '''
        k_critical
        tells if graph G is k-critical for some k
        Parameters:
            None
        Returns:
            int: the k-critical
            None: if graph is not k-critical
        '''
        claw_free = self.induced_subgraph(self.claw)
        co_claw_free = self.induced_subgraph(self.co_claw)
        if claw_free and co_claw_free:
            return self._claw_and_co_free()

    def _claw_and_co_free(self):
        '''
        _claw_and_co_free
        finds if graph G is k-critical for some k
        requires the G to be claw and co-claw free
        Parameters:
            None
        Returns:
            int: the k-critical graph
            None: if graph is not k-critical
        '''
        clique = self.clique_number()
        k = None
        if clique is None:
            #is not a clique
            c5 = self.find_c5(self._g)
            if len is not None:
                #special case C5
                #recursively call function on subgraph
                h = self._g.copy()
                subgraph = DalGraph(h)
                subgraph.remove_vertices(c5)
                return 3 + subgraph._claw_and_co_free()
            else:
                hole = self.hole_number()
                if hole % 2 ==0:
                    #odd cycle
                    k = 3
        else:
            k = clique
        return k

    def find_c5(self):
        '''
        find_c5
        finds one cycle of with 5 vertices
        Parameters:
            None
        Returns:
            list: a list of the C5
            None: otherwise
        '''
        c5 = None
        cycles = nx.cycle_basis(self._g)
        print(cycles)
        index = 0
        while c5 is None and index <  len(cycles):
            if len(cycles[index]) == 5:
                # is a cycle with 5 vertices
                c5 = sorted(cycles[index])
            index += 1
        return c5

    def remove_vertices(self,vertices):
        '''
        remove_vertices
        remove a list of vertices
        Parameters:
            vertices: the list of vertices (int)
        Returns:
            None
        '''
        for vertex in vertices:
            self._g.remove_node(vertex)

    def induced_subgraph(self, H):
        '''
        induced_subgraph
        returns vertices of G which make an induced subgraph H
        Parameters:
            H: the induced subgraph (Graph)
        Returns:
            list: the list of vertices which make up induced subgraph (int)
            None if no induced subgraph
        '''
        induced = None
        # TODO
        return induced