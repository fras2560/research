"""
-------------------------------------------------------
dcolor
a module to determine the chromatic number of a graph
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-17
-------------------------------------------------------
"""
import networkx as nx
from itertools import permutations
import logging
import copy
from pprint import PrettyPrinter
class Dcolor():
    def __init__(self, graph, logger=None):
        if logger is None:
            logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger = logger
        self.coloring = None
        self.graph = graph
        self.pp = PrettyPrinter(indent=4)

    def chromaic_number(self):
        '''
        a method to determine the chromatic number of the graph
        Parameters:
            None
        Returns:
            : the chromatic number (int)
        '''
        if self.coloring is None:
            self.color()
        return len(self.coloring)
    
    def color(self):
        '''
        a method to determine a graph coloring
        Parameters:
            None
        Returns:
            self.coloring: the graph coloring (list)
        '''
        if self.coloring is None:
            self.color_aux()
        return self.coloring

    def create_clique_list(self):
        '''
        a method to create a list of cliques
        Parameters:
            None
        Returns:
            cliques: the list of cliques (list)
            chromatic: the chromatic number (int)
            l_index: the largest clique index (int)
        '''
        g = self.graph.copy()
        chromatic = 0
        l_index = 0
        index = 0
        cliques = []
        while len(g.nodes()) > 0:
            largest = 0
            for clique in nx.find_cliques(g):
                if len(clique) > largest:
                    largest = len(clique)
                    largest_clique = clique
            clique = []
            for node in largest_clique:
                g.remove_node(node)
                clique.append([node])
            if len(clique) > chromatic:
                chromatic = len(clique)
                largest = clique
                l_index = index
            cliques.append(clique)
            index += 1
        return cliques, chromatic, l_index

    def color_aux(self):
        '''
        a method to help with coloring
        Sets self.coloring to a valid coloring
        Parameters:
            None
        Returns:
            None
        '''
        self.logger.debug("Coloring")
        cliques, chromatic, index = self.create_clique_list()
        done = False
        if chromatic == len(self.graph.nodes()):
            done = True
            coloring = cliques[0]
            self.logger.debug("Graph is a Clique: %d" % chromatic)
        elif chromatic == 2:
            cycles = nx.cycle_basis(self.graph)
            odd = False
            for cycle in cycles:
                if len(cycle) % 2 == 1:
                    odd = True
            if odd:
                largest = cliques.pop(index)
                largest.append([])
                chromatic += 1
            else:
                largest = cliques.pop(index)
        else:
            largest = cliques.pop(index)
        while not done:
            self.logger.info('Testing Chromatic Number: %d' % chromatic)
            coloring = self.coloring_step(cliques, largest)
            if coloring is None:
                largest.append([]) # equivalent to adding a new color
                chromatic += 1
            else:
                done = True
        self.coloring = coloring

    def coloring_step(self, cliques, coloring):
        '''
        a recursive function that acts as one step in the coloring
        Parameters:
            cliques: a list of the cliques (list)
            coloring: an initial coloring (list)
        Returns:
            coloring: None if no coloring is possible
        '''
        
        if len(cliques) == 0:
            result =  coloring
        else:
            added = False
            valid = []
            for pc in combine_color_clique(coloring, cliques[0]):
                if self.valid_coloring(pc):
                    added = True
                    valid.append(pc)
            if not added:
                result = None
            else:
                for pc in valid:
                    result = self.coloring_step(cliques[1:], pc)
                    if result is not None:
                        break
        return result

    def copy_list(self, l):
        '''
        a method to copy a list
        Parameters:
            l: the list to copy (list)
        Returns:
            result: the copied list (list)
        '''
        result = []
        for element in l:
            result.append(copy.deepcopy(element))
        return result

    def valid_coloring(self, coloring):
        '''
        a method that determines if the coloring is valid
        Parameters:
            coloring: a list of colors in which each color is a list of nodes 
                      e.g. [[1,2],[3]]
        Returns:
            valid: True if valid coloring,
                   False otherwise
        '''
        valid = False
        if coloring is not None:
            valid = True
            for color in coloring:
                for vertex in color:
                    neighbors = self.graph.neighbors(vertex)
                    for neighbor in neighbors:
                        if neighbor in color:
                            valid = False
                            break;
                    if not valid:
                        break;
                if not valid:
                    break;
        return valid

def add_list(l1, l2, index):
    '''
    a function that  adds the list l1 to the two dimensional
    list l2
    Parameters:
        l1: the first list (list)
        l2: the second list (list of lists)
        i1: the starting index to l1 (int)
    Returns:
        l: the list of lists(list of lists)
    '''
    l = copy.deepcopy(l1)
    i = 0
    while i < len(l2):
        l[index] += l2[i]
        i += 1
        index += 1
    return l

def convert_combo(combo):
    '''
    a function that converts a combo tuple to a list
    Parameters:
        combo: a tuple of combinations (tuple)
    Returns:
        conversion: the converted combination (list)
    '''
    conversion = []
    for c  in combo:
        conversion.append(c)
    return conversion

def combine_color_clique(clique, color):
    '''
    a function that takes a clique list and a color split
    and yields all the ways the clique list can be combine with coloring
    Parameters:
        clique: the clique (list of lists)
        color: the coloring (list of lists)
        index: the index
    Returns:
        coloring: the combined color (list of lists)
    '''
    color_length = len(color)
    clique_number = len(clique)
    for c in permutations(clique):
        c = convert_combo(c)
        if clique_number < color_length:
            index = 0
            while index <= color_length - clique_number:
                yield add_list(color, c, index)
                index += 1
        elif clique_number > color_length:
            index = 0
            while index <= clique_number - color_length:
                yield add_list(c, color, index)
                index += 1
        else:
            yield add_list(c, color, 0)

import unittest
from graph.helper import make_claw, make_diamond, make_cycle, join
class Test(unittest.TestCase):

    def setUp(self):
        self.dcolor = Dcolor(make_claw())

    def tearDown(self):
        pass

    def testColoringAux(self):
        self.dcolor.color_aux()

    def testCreateCliqueList(self):
        c, k, i = self.dcolor.create_clique_list()
        self.assertEqual([[[0], [1]], [[2]], [[3]]], c)
        self.assertEqual(k, 2)
        self.assertEqual(i, 0)
        self.dcolor = Dcolor(make_diamond())
        c, k, i = self.dcolor.create_clique_list()
        self.assertEqual([[[0], [1], [2]], [[3]]], c)
        self.assertEqual(k, 3)
        self.assertEqual(i, 0)
        
    def testColor(self):
        result = self.dcolor.color()
        expect = [[0], [1, 2, 3]]
        self.assertEqual(expect, result, "Coloring: Claw Case")
        self.dcolor = Dcolor(make_diamond())
        result = self.dcolor.color()
        expect = [[0], [1], [2, 3]]
        self.assertEqual(expect, result, "Coloring: Diamond Case")
        g = nx.Graph()
        g.add_node(0)
        g.add_node(1)
        self.dcolor = Dcolor(g)
        result = self.dcolor.color()
        expect = [[0, 1]]
        self.assertEqual(expect, result, "Coloring: Stable Set")

    def testColoringCritical(self):
        self.dcolor = Dcolor(make_cycle(5))
        color = self.dcolor.color()
        expect = [[0], [1, 3], [2, 4]]
        self.assertEqual(len(color), 3)
        self.assertEqual(color, expect)
        k1 = nx.Graph()
        k1.add_node(0)
        g = join(make_cycle(5), k1)
        self.dcolor = Dcolor(g)
        color = self.dcolor.color()
        self.assertEqual(len(color), 4)
        expect = [[5], [0],  [1, 3], [2, 4]]
        self.assertEqual(expect, color)

    def testColoringHardGraph(self):
        # C5 + 5 Xi
        g = make_cycle(5)
        index = 0
        for i in range(5, 10):
            g.add_node(i)
            # make it a two vertex
            g.add_edge(i, (index+0) % 5) # xi
            g.add_edge(i, (index+1) % 5)
            index += 1
        g.add_edge(5, 6)
        g.add_edge(5, 8)
        g.add_edge(6, 8)
        g.add_edge(7, 9)
        self.dcolor = Dcolor(g)
        color = self.dcolor.color()
        expect = [[1, 8, 9], [5, 4, 7], [2], [0, 3, 6]]
        self.assertEqual(self.dcolor.valid_coloring(color), True)
        self.assertEqual(color, expect)
        # C5 + 2 Yi
        g = make_cycle(5)
        g.add_node(5)
        g.add_edge(0,5)
        g.add_edge(1,5)
        g.add_edge(2,5)
        g.add_node(6)
        g.add_edge(0,6)
        g.add_edge(3,6)
        g.add_edge(4,6)
        self.dcolor = Dcolor(g)
        color = self.dcolor.color()
        expect = [[0, 3], [1, 4], [5, 6], [2]]
        self.assertEqual(self.dcolor.valid_coloring(color), True)
        self.assertEqual(color, expect)
        
        # C5 Joined K5
        # does not work efficiently for this atm
#         k5 = nx.Graph()
#         for i in range (0,5):
#             k5.add_node(i)
#             for edge in range(0, i):
#                 k5.add_edge(edge, i)
#         g = join(k5, make_cycle(5))
#         self.dcolor = Dcolor(g)
#         print('color hard one')
#         color = self.dcolor.color()
#         print(color)

    def testColorCycle(self):
        g = make_cycle(5)
        for i in range(5, 100):
            g.add_node(i)
            g.add_edge(i - 1, i)
        self.dcolor = Dcolor(g)
        color = self.dcolor.color()
        self.assertEqual(len(color), 3)
        self.assertEqual(self.dcolor.valid_coloring(color), True)

    def testColoringClique(self):
        g = make_cycle(3)
        self.dcolor = Dcolor(g)
        color = self.dcolor.color()
        expect = [[0], [1], [2]]
        self.assertEqual(len(color), 3)
        self.assertEqual(color, expect)

    def testCombineColorClique(self):
        coloring = [[3], [2]]
        clique = [[0], [1]]
        expect = [
                  [[0, 3], [1, 2]],
                  [[1, 3], [0, 2]]
                 ]
        index = 0
        for combo in combine_color_clique(clique, coloring):
            self.assertEqual(combo, expect[index])
            index += 1
        coloring = [[0, 1]]
        clique = [[2], [3]]
        expect = [
                  [[2, 0, 1], [3]],
                  [[2], [3, 0, 1]],
                  [[3, 0, 1], [2]],
                  [[3], [2, 0, 1]]
                 ]
        index = 0
        for combo in combine_color_clique(clique, coloring):
            self.assertEqual(combo, expect[index])
            self.assertEqual(combo, expect[index])
            index += 1
        coloring = [[0], [1], [2]]
        clique = [[3], [4]]
        expect = [
                  [[0, 3], [1, 4], [2]],
                  [[0], [1, 3], [2, 4]],
                  [[0, 4], [1, 3], [2]],
                  [[0], [1, 4], [2, 3]]
                 ]
        index = 0
        for combo in combine_color_clique(clique, coloring):
            self.assertEqual(combo, expect[index])
            index += 1

    def testAddList(self):
        l1 = [[1],[2]]
        l2 = [[3],[4,5]]
        result = add_list(l1, l2, 0)
        expect = [[1, 3], [2, 4, 5]]
        self.assertEqual(result, expect)
        l1 = [[1],[2], [6]]
        l2 = [[3],[4,5]]
        result = add_list(l1, l2, 0)
        expect = [[1, 3], [2, 4, 5], [6]]
        self.assertEqual(result, expect)
        result = add_list(l1, l2, 1)
        expect = [[1], [2, 3], [6, 4, 5]]
        self.assertEqual(result, expect)

    def testConvertCombo(self):
        combo = (4, 1)
        conversion = convert_combo(combo)
        self.assertEqual(type(conversion), list,
                         "Convert Combo: did not return list")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()