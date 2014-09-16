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
import copy
import math
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

    def k_color(self):
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
            # is not a clique
            cycle = self.cycle_nodes()
            if len(cycle) == 0 or len(cycle) % 2:
                # no cycle or even hole so done
                k = None
            elif len(cycle) > 5:
                # odd-hole
                if len(cycle) == len(self._g.nodes()):
                    # just an odd-hole
                    k = 3
            if k is None:
                # check for anti-hole
                co_g = DalGraph(nx.complement(nx.Graph.copy(self._g)))
                cycle = co_g.cycle_nodes()
                if len(cycle) == 0 or len(cycle) % 2:
                    k = None
                co_g._g = nx.complement(co_g._g)
                co_g.remove_vertices(cycle)
                k2 = co_g.k_color()
                k = math.ceil(cycle / 2) + k2
        else:
            k = clique
        return k

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

    def cycle_nodes(self):
        '''
        cycle_nodes
        returns a list of vertices of G which form a cycle > 5 vertices
        Parameters:
        Returns:
            list: the list of vertices which make up induced cycle
            None if no cycle
        '''
        cycle = []
        node = 0
        while node < len(self._g.nodes()) and len(cycle) == 0:
            cycle = self.cycle_nodes_aux([node])
            node += 1
        return cycle

    def cycle_nodes_aux(self, visited):
        '''
        cycle_nodes_aux
        a function that checks if any cycles
        Parameters:
            visited: the visited nodes so far
        Returns:
            list: a empty list if no cycle else the cycle
        '''
        last_one = visited.pop()
        neighbor = self._g.neighbors(last_one)
        cycle = [] # assume no cycle
        if len(neighbor) != 0:
            add_vertex = 0
            cont = True
            while add_vertex < len(neighbor) and cont:
                if neighbor[add_vertex] not in visited:
                    print(visited, neighbor[add_vertex], last_one)
                    cycle = self.check_smaller_cycle(visited, 
                                                     neighbor[add_vertex],
                                                     last_one)
                    print("Cycle:", cycle)
                    if len(cycle) != 0:
                        if cycle[-1] == cycle[0]: 
                            # cycle was formed
                            cont = False
                        elif cycle[-1] == neighbor[add_vertex]:
                            print("Longer path")
                            # longer path was produced
                            cycle = self.cycle_nodes_aux(cycle)
                            if len(cycle) != 0 and cycle[-1] == cycle[0]:
                                # cycle was formed
                                cont = False
                        else:
                            cycle = []
                else:
                    #just a neighbor already
                    pass
                add_vertex += 1 #increment counter
        return cycle

    def check_smaller_cycle(self, visited, add_vertex, last_one):
        '''
        check_smaller_cycle
        a function that finds if vertex to add forms a cycle with any previous
        visited node
        Parameters:
            G: the graph (networkx)
            visited: the list of visited nodes (list)
            add_vertex: the vertex considering to add (int)
            last_one: the previous node (int)
        Returns:
            cycle: a list of vertices that form a cycle, a valid path or empty
                    list if added vertex forms a smaller cycle
        '''
        check = 0
        neighbors = self._g.neighbors(add_vertex)
        print("Visited:", visited, "adding:", add_vertex)
        cont = True
        cycle = []
        while check < len(neighbors) and cont:
            print("Checking:", neighbors[check])
            if neighbors[check] in visited[1:]:
                print("Backtrack")
                # backtrack to smaller cycle
                cont = False
                cycle = []
            elif len(visited) >= 1 and neighbors[check] == visited[0]:
                # forms a cycle
                print("Forms a cycle")
                if len(visited) + 2 >= 5:
                    # got a cycle > 5
                    cycle = copy.deepcopy(visited)
                    # add the node previous node, next node,
                    # first node to form the cycle
                    cycle.append(last_one)
                    cycle.append(add_vertex)
                    cycle.append(visited[0])
                else:
                    # cycle is too small
                    print("Cycle too small")
                    cycle = []
                    cont = False
            elif len(visited) == 1 and add_vertex == visited[0]:
                # don't want cycles of 2
                cont = False
                cycle = copy.deepcopy(visited)
                cycle.append(last_one)
            check += 1
        if cont and len(cycle) == 0:
            # could add since no smaller cycle is formed so can add
            cycle = copy.deepcopy(visited)
            cycle.append(last_one)
            cycle.append(add_vertex)
        return cycle
