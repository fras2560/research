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
import graph.helper
import copy
import math
from graph.colorable import chromatic_number
from graph.helper import text_to_networkx
from graph.classify import classify
from graph.dcolor import Dcolor
import logging

class DalGraph():
    def __init__(self, graph=None, file=None, logger=None):
        '''
        init
            Parameters:
                graph: the existing networkx graph, default to None (Graph)
                file: the text file representing the graph
        '''
        if graph is None and file is None:
            self._g = nx.Graph()
        elif graph is not None:
            self._g = graph
        else:
            read = False
            with open(file) as f:
                content = f.read()
                lines = content.replace("\r", "")
                lines = lines.split("\n")
                self._g = text_to_networkx(lines)
                read = True
            if not read:
                raise Exception("Not a valid file")
        if logger is not None:
            self.logger = logger
        else:
            logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
            self.logger = logging.getLogger(__name__)

    def clique_number(self):
        '''
        is_clique
        returns the clique number of the graph
            Parameters:
                None
            Returns:
                int: the maximal clique number 
        '''
        edges = self._g.number_of_edges()
        nodes = self._g.number_of_nodes()
        clique = None
        if nodes <= 1:
            clique = nodes
        if edges == (nodes * (nodes-1) / 2):
            # is a clique (k=#nodes)
            clique = nodes
        return clique

    def alpha_number(self):
        '''
        returns the stabe set number of the graph
            Parameters:
                None
            Returns:
                stable: the max size of the stable set (int)
                        None if no stable set
        '''
        complement = nx.complement(self._g)
        return len(list(nx.find_cliques(complement)))

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
        finds if graph G is k-is_critical for some k
        requires the G to be claw and co-claw free
        Parameters:
            None
        Returns:
            int: the k-is_critical graph
            None: if graph is not k-is_critical
        '''
        clique = self.clique_number()
        print("Clique number:", clique)
        print(self._g.nodes())
        k = None
        if clique is None:
            # is not a clique
            cycle = self.cycle_nodes()
            if len(cycle) > 3:
                cycle.pop() # don't need the full cycle path just the vertices
            if len(cycle) == 0 or len(cycle) % 2 == 0:
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
                if len(cycle) > 3:
                    cycle.pop() # don't need the full cycle path just the vertices
                if len(cycle) == 0 or len(cycle) % 2 == 0:
                    # even hole or no hole
                    k = None
                else:
                    co_g._g = nx.complement(co_g._g)
                    co_g.remove_vertices(cycle)
                    k2 = co_g.k_color()
                    if k2 is not None:
                        k = math.ceil(len(cycle) / 2) + k2
                    else:
                        k = None
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
            cycle = self.cycle_nodes_aux([self._g.nodes()[node]])
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

    def find_co_claw(self):
        '''
        a method that finds a co-claw in G
        Parameters:
            none
        Returns:
            co_claw: the list of nodes forming the co-claw
                    None if no co-claw is present
        '''
        co_claw = None
        cycles = nx.cycle_basis(self._g)
        print(cycles)
        for cycle in cycles:
            neighbors = self.union_neighbors(cycle)
            for node in self._g.nodes():
                if node not in neighbors and len(cycle) == 3:
                    co_claw = cycle + [node]
                    break
            if co_claw is not None:
                break
        return co_claw

    def find_claw(self):
        '''
        a method that finds a claw in G
        Parameters:
            None
        Returns:
            claw: the list of nodes forming the claw
                 None if there is no claw
        '''
        temp = self._g.copy()
        self._g = nx.complement(self._g)
        claw = self.find_co_claw()
        self._g = temp.copy()
        return claw

    def union_neighbors(self, nodes):
        '''
        a method the creates a list of neighbors of the list of nodes
        Parameters:
            nodes: the list of nodes (list)
        Returns:
            neighbors: the list of neighbors (list)
        '''
        neighbors = []
        for node in nodes:
            for n in self._g.neighbors(node):
                if n not in neighbors:
                    neighbors.append(n)
        return neighbors

    def critical_aprox(self):
        '''
        a method that approximates if the graph is critical
        Parameters:
            None
        Returns:
            True if graph is critical
            False otherwise
        '''
        critical = True
        nodes = self._g.nodes()
        index = 0
        chromatic = len(Dcolor(self._g).color())
        self.logger.info("Chromatic number of G is %d" % chromatic)
        while critical  and index < len(nodes):
            g = self._g.copy()
            g.remove_node(nodes[index])
            check = len(Dcolor(g).color())
            if check != (chromatic - 1):
                self.logger.info("G is not critical: %d", index)
                critical = False
            index += 1
        return critical

    def is_critical(self):
        '''
        a method that finds if the graph is is_critical
        Parameters:
            None
        Returns:
            True if graph is is_critical
            False otherwise
        '''
        is_critical = True
        nodes = self._g.nodes()
        index = 0
        chromatic = chromatic_number(self._g)
        self.logger.info("Chromatic number of G is %d" %chromatic)
        while is_critical and index < len(nodes):
            g = self._g.copy()
            g.remove_node(nodes[index])
            check = chromatic_number(g)
            if check != (chromatic -1):
                self.logger.info(index)
                self.logger.info("G is not critical")
                is_critical = False
            index += 1
        return is_critical

    def k4_codiamond_critical(self):
        '''
        a method i think will find whether this graph family is critical
        Parameters:
            None
        Returns:
            True if critical
            False otherwise
        '''
        cycle = self.cycle_nodes()[:-1]
        critical = False
        if len(cycle) == 5:
            k = classify(self._g, cycle)
            k = self.delete_2(k)
            k_set = list(k.keys())
            i1 = 0
            if len(k) == 0:
                critical = True
            while not critical and len(k)!= 0:
                v1 = k_set[i1]
                del k[k_set[i1]]
                i2 = i1 + 1
                while not critical and i2 < len(k_set):
                    v2 = k_set[i2]
                    critical = self.cover_c5(v1, v2)
                    i2 += 1
                i1 += 1
        return critical

    def delete_2(self, k):
        '''
        a method that deletes all the 2-vertex
        Parameters:
            k: the k-vertex dictionary (dict)
        Returns:
            k: the updated dictionary (dict) 
        '''
        result = k.copy()
        index = 0
        keys = list(result.keys())
        while index < len(keys):
            key = keys[index]
            if key.count(",") < 2:
                del result[key]
            index += 1
        return result

    def cover_c5(self,v1, v2):
        '''
        a method to check if the two values cover
        all the vertices of the C5
        Parameters:
            v1: the string value of adjacency (string)
            v2: the second string value of adjacency (string)
        Returns:
            True if covers all of them
            False otherwise
        '''
        nodes = ['i','i+1','i+2', 'i+3', 'i+4']
        check = v1 + v2
        covered = True
        index = 0
        while covered and index < len(nodes):
            if nodes[index] not in check:
                covered = False
            index += 1
        return covered

