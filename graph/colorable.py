"""
-------------------------------------------------------
colorable
a module to determine the chromatic number of a graph
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-17
-------------------------------------------------------
"""
import unittest
import networkx as nx
from itertools import permutations
import logging
import copy

def valid_coloring(coloring, G):
    '''
    a function that determines if the coloring is valid
    Parameters:
        coloring: a list of colors in which each color is a list of nodes 
                  e.g. [[1,2],[3]]
        G: a networkx graph (networkx)
    Returns:
        valid: True if valid coloring,
               False otherwise
    '''
    valid = False
    if coloring is not None:
        valid = True
        for color in coloring:
            for vertex in color:
                neighbors = G.neighbors(vertex)
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

def coloring(G, logger=None):
    '''
    a function that finds the chromatic number of graph G
    using brute force
    Parameters:
        G: the networkx graph (networkx)
        logger: the logger for the function (logging)
    Returns:
        chromatic: the chromatic number (int)
    '''
    if logger is None:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)

    valid = False
    largest = 0
    largest_clique = []
    # find largest clique
    for clique in nx.find_cliques(G):
        if len(clique) > largest:
            largest = len(clique)
            largest_clique = clique
    # set chromatic to the largest clique
    chromatic  = largest - 1 # one less since add at start of loop
    if chromatic == 0:
        # can be no edge between any node
        coloring = [G.nodes()]
        valid = True
    nodes = G.nodes()
    # remove nodes from largest clique
    i = 0
    clique = []
    # reformat the clique
    for node in largest_clique:
        clique.append([node])
    while i < len(nodes):
        if nodes[i] in largest_clique:
            nodes.pop(i)
        else:
            i += 1
    balls = len(nodes)
    print("Nodes:", nodes)
    while not valid:
        chromatic += 1
        logger.info('''
                    ------------------------------\n
                    Testing Chromatic Number of %s\n
                    ------------------------------\n
                    ''' %chromatic)
        boxes = [balls] * chromatic
        for combo in permutations(nodes):
            logger.debug(combo)
            for split in unlabeled_balls_in_unlabeled_boxes(balls, boxes):
                coloring = None
                node_combo = convert_combo(combo)
                coloring = assemble_coloring(node_combo, split)
                print("Coloring:", coloring, " Clique: ",clique)
                for check in combine_color_clique(clique, coloring):
                    if valid_coloring(check, G):
                        coloring = check
                        valid = True
                        break;
                if valid:
                    break
            if valid:
                break
        if chromatic > 10:
            # stop case
            valid = True
            coloring = None
        if chromatic == len(nodes):
            valid = True
    return coloring

def chromatic_number(G):
    '''
    a function that finds the chromatic number of a graph
    Parameter:
        G: the networkx graph
    Returns:
        : the chromatic number (int)
    '''
    return len(coloring(G))

def valid_split(split):
    '''
    a function that checks if the split of nodes is valid 
    for that number of colors
    Parameters:
        split: the split of each color (tuple)
    Returns:
        True if valid
        False otherwise
    '''
    valid = True
    for color in split:
        if color == 0:
            valid = False
    return valid

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

def assemble_coloring(nodes, split):
    '''
    a function that assembles the coloring
    Parameters:
        nodes: the list of node (list)
        split: the list of split (how many nodes for each color) (list)
    Returns:
        coloring: list of color's list
                 E.G.  [[n1, n2], [n3]]
    '''
    coloring = None
    if len(split) == 0:
        coloring = [nodes]
    else:
        coloring = []
        for size in split:
            color = []
            while len(color) < size:
                color.append(nodes.pop())
            coloring.append(color)
    return coloring

def unlabeled_balls_in_unlabeled_boxes(balls, box_sizes):
    '''
    @author Dr. Phillip M. Feldman
    '''
    if not isinstance(balls, int):
        raise TypeError("balls must be a non-negative integer.")
    if balls < 0:
        raise ValueError("balls must be a non-negative integer.")
    if not isinstance(box_sizes,list):
        raise ValueError("box_sizes must be a non-empty list.")
    capacity= 0
    for size in box_sizes:
        if not isinstance(size, int):
            raise TypeError("box_sizes must contain only positive integers.")
        if size < 1:
            raise ValueError("box_sizes must contain only positive integers.")
        capacity+= size
    if capacity < balls:
        raise ValueError("The total capacity of the boxes is less than the "
                         "number of balls to be distributed.")
    box_sizes= list( sorted(box_sizes)[::-1] )
    return unlabeled_balls_in_unlabeled_boxe(balls, box_sizes)

def unlabeled_balls_in_unlabeled_boxe(balls, box_sizes):
    '''
    @author Dr. Phillip M. Feldman
    '''
    if not balls:
        yield len(box_sizes) * (0,)
    elif len(box_sizes) == 1:
        if box_sizes[0] >= balls:
            yield (balls,)
    else:
        for balls_in_first_box in range( min(balls, box_sizes[0]), -1, -1 ):
            balls_in_other_boxes = balls - balls_in_first_box
            short = unlabeled_balls_in_unlabeled_boxe
            for distribution_other in short(balls_in_other_boxes,
                                            box_sizes[1:]):
                if distribution_other[0] <= balls_in_first_box:
                    yield (balls_in_first_box,) + distribution_other

from graph.helper import make_claw, make_diamond
class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testColoring(self):
        g = make_claw()
        result = coloring(g)
        expect = [[1, 3, 2], [0]]
        self.assertEqual(expect, result, "Coloring: Claw Case")
        g = make_diamond()
        result = coloring(g)
        expect = [[2, 3], [0], [1]]
        self.assertEqual(expect, result, "Coloring: Diamond Case")
        g = nx.Graph()
        g.add_node(0)
        g.add_node(1)
        result = coloring(g)
        expect = [[0, 1]]
        self.assertEqual(expect, result, "Coloring: Stable Set")
    
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

    def testValidColoring(self):
        g = make_claw()
        # test invalid claw coloring
        coloring = [[0, 1, 2, 3]]
        valid = valid_coloring(coloring, g)
        self.assertEqual(valid, False,
                         "Valid coloring: Failed for one coloring on claw")
        
        coloring = [[1, 3, 2], [0]]
        valid = valid_coloring(coloring, g)
        self.assertEqual(valid, True,
                         "Valid coloring: Failed for valid coloring on claw")
        # test valid claw coloring
        coloring = [[0], [1, 2, 3]]
        valid = valid_coloring(coloring, g)
        self.assertEqual(valid, True,
                         "Valid coloring: Failed for valid coloring on claw")
        # test invalid claw coloring
        coloring = [[0, 1], [2, 3]]
        valid = valid_coloring(coloring, g)
        self.assertEqual(valid, False,
                         "Valid coloring: Failed for invalid coloring on claw")
        # test valid diamond coloring
        g = make_diamond()
        coloring = [[0], [1], [2, 3]]
        valid = valid_coloring(coloring, g)
        self.assertEqual(valid, True, 
                         "Valid coloring: failed for valid coloring on diamond")
        coloring = [[3], [2], [0, 1]]
        valid = valid_coloring(coloring, g)
        self.assertEqual(valid, False, 
                         '''
                         Valid coloring: failed for invalid coloring on diamond
                         ''')

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

    def testChromaticNumber(self):
        g = make_claw()
        chromatic = chromatic_number(g)
        expect = 2
        self.assertEqual(expect, chromatic, "Chromatic Number: Claw Case")
        g = make_diamond()
        chromatic = chromatic_number(g)
        expect = 3
        self.assertEqual(expect, chromatic, "Chromatic Number: Diamond Case")

    def testValidSplit(self):
        split = (4, 0)
        self.assertEqual(valid_split(split), False,
                         "Valid split: True on Invalid Split")
        split = (4, 1)
        self.assertEqual(valid_split(split), True,
                         "Valid split: True on Valid Split")

    def testConvertCombo(self):
        combo = (4, 1)
        conversion = convert_combo(combo)
        self.assertEqual(type(conversion), list,
                         "Convert Combo: did not return list")

    def testAssembleColoring(self):
        split = [1, 2]
        combo = [1, 2, 3]
        result = assemble_coloring(combo, split)
        expect = [[3], [2, 1]]
        self.assertEqual(expect, result, "Assemble Coloring: unexpected result")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()