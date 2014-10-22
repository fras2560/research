"""
-------------------------------------------------------
file
a set of function to deal with the files and directories
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-10-20
-------------------------------------------------------
"""
import logging
import networkx as nx
import os
from graph.helper import networkx_to_text,  text_to_networkx
from graph.container import induced_subgraph

class File():
    def __init__(self, directory, G=None, logger=None, file=None):
        '''
        G: a networkx graph (networkx)
        directory: the filepath to the directory (filepath)
        logger: the logger to log information (logging)
        file: the file of the graph to load
        '''
        self.directory = directory
        if G is None and file is None:
            raise Exception("File not initialized properly")
        if G is not None:
            self.G = G
        else:
            self.G = self.load(file)
        self.clique = nx.graph_clique_number(self.G)
        if logger is None:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(message)s')
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    def load(self, file):
        '''
        a method to help load a graph from a file
        Parameters:
            file: the graph file (filepath)
        Returns:
            G: the graph G (networkx)
        '''
        fp = os.path.join(self.directory, file)
        with open(fp) as file:
            text = file.read()
            lines = text.split("\n")
            G = text_to_networkx(lines)
        return G

    def save(self):
        '''
        a method that takes a graph G and saves it to the appropriate folder
        does not save the file if isomorphic to a previously saved file
        Parameters:
        Returns:
            name: the file path of where it was saved (filepath)
                None if return if did not save the file
        '''
        name = self.get_name()
        fp = self.file_path(name)
        index = 1
        should_save = True
        self.logger.debug(fp)
        while not (self.check_unique(fp)) and should_save:
            directory = os.path.dirname(fp)
            self.logger.info("Comparing to %s" %(name))
            if self.compare(File(directory, logger=self.logger, file=name)):
                should_save = False
            else:
                fp = self.file_path(self.get_name(index))
                name = self.get_name(index)
                index += 1
        if should_save:
            text = networkx_to_text(self.G)
            self.logger.info("Saving Graph %s", fp)
            self.logger.debug("File Text \n" + text)
            with open(fp, "w") as file:
                file.write(text)
        else:
            self.logger.info("Graph was already saved")
            fp = None
        return fp

    def get_name(self, index=None):
        '''
        a method that determines the name of G
        based upon properties of the graph
        Parameters:
            index: a value index to add to the end of the name
        Returns:
            name: the name of the graph
        '''
        edges = len(self.G.edges())
        nodes = len(self.G.nodes())
        if index is None:
            name = ("has_K" + str(self.clique) + "_edges-" + str(edges) + '_nodes-'
                    + str(nodes) + ".txt")
        else:
            name = ("has_K" + str(self.clique) + "_edges-" + str(edges) + '_nodes-'
                    + str(nodes) +"--" + str(index) + ".txt")
        return name

    def file_path(self, name):
        '''
        a method that takes a name and returns the file path for 
        a Graph with that name
        Note:
            Will create directory if it does not exist
        Parameters:
            name: the name of graph (string)
        Returns:
            fp: the filepath for the graph (filepath)
        '''
        directory = os.path.join(self.directory, "hasK" + str(self.clique))
        fp = os.path.join(directory, name)
        if not os.path.exists(directory):
            self.logger.info("Created directory for K%d" % self.clique)
            os.makedirs(directory)
        return fp

    def check_unique(self, filepath):
        '''
        a method that checks if the name is unique in that directory
        (Will create directory if does not exist)
        Parameters:
            filepath: the filepath of the
        '''
        return not os.path.exists(filepath)

    def compare(self, B):
        '''
        a method use to compare the two graphs of the File objects given
        Parameter:
            B: the object to compare to (File)
        Returns:
            True if the two graphs are the same (isomorphic)
            False otherwise
        '''
        self.logger.debug("Comparing two graphs")
        same = False
        cond1 = len(self.G.nodes()) == len(B.G.nodes())
        cond2 = len(self.G.edges()) == len(B.G.edges())
        self.logger.debug("same edges: %r Same nodes: %r" %(cond1, cond2))
        if cond1 and cond2:
            induced = induced_subgraph(self.G, B.G)
            induced_2 = induced_subgraph(B.G, self.G)
            if induced is not None or induced_2 is not None:
                same = True
        self.logger.debug("The two graphs are the same: %r" % same)
        return same

import unittest
import shutil
from graph.helper import make_claw, make_cycle, make_co_claw
class Tester(unittest.TestCase):
    def setUp(self):
        self.directory = os.getcwd()
        self.k2 = os.path.join(self.directory, "hasK2")
        self.k3 = os.path.join(self.directory, "hasK3")
        self.k4 = os.path.join(self.directory, "hasK4")
        self.k5 = os.path.join(self.directory, "hasK5")
        self.testk2 = os.path.join(self.directory, "test", "hasK2")
        self.testk3 = os.path.join(self.directory, "test", "hasK3")
        self.testk4 = os.path.join(self.directory, "test", "hasK4")
        self.testk5 = os.path.join(self.directory, "test", "hasK5")
        self.created = [self.k2, self.k3, self.k4, self.k5,
                        self.testk2, self.testk3, self.testk4, self.testk5]
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)

    def tearDown(self):
        for c in self.created:
            if os.path.exists(c):
                shutil.rmtree(c, ignore_errors=True)

    def testGetName(self):
        g = make_claw()
        f = File(self.directory,G=g, logger=self.logger)
        self.assertEqual(f.get_name(), "has_K2_edges-3_nodes-4.txt")
        g = make_cycle(5)
        f = File(self.directory,G=g, logger=self.logger)
        self.assertEqual(f.get_name(), "has_K2_edges-5_nodes-5.txt")
        self.assertEqual(f.get_name(1), "has_K2_edges-5_nodes-5--1.txt")
        self.assertEqual(f.get_name(10), "has_K2_edges-5_nodes-5--10.txt")

    def testFilePath(self):
        created = os.path.exists(self.k2)
        self.assertEqual(created, False)
        g = make_claw()
        f = File(self.directory,G=g, logger=self.logger)
        name = "has_K2_edges-5nodes-5.txt"
        fp = f.file_path(name)
        self.assertEqual(os.path.join(self.directory, self.k2, name), fp)
        created = os.path.exists(self.k2)
        self.assertEqual(created, True)

    def testChequeUnique(self):
        f = File(self.directory,G=make_claw(), logger=self.logger)
        fp = "does not exists"
        self.assertEqual(f.check_unique(fp), True)
        os.makedirs(self.k2)
        self.assertEqual(f.check_unique(self.k2), False)

    def testSaveBasic(self):
        g = make_claw()
        f = File(self.directory,G=g, logger=self.logger)
        expect = f.file_path(f.get_name())
        self.assertEqual(os.path.exists(expect), False)
        f.save()
        self.assertEqual(os.path.exists(expect), True)
        # make sure the graph was valid
        with open(expect) as file:
            text = file.read()
            lines = text.split("\n")
            claw = text_to_networkx(lines)
            self.assertEqual(g.nodes(), claw.nodes())
            self.assertEqual(g.edges(), claw.edges())

    def testSaveIsomorphic(self):
        claw = make_claw()
        f = File(self.directory, G=claw, logger=self.logger)
        fp_1 = f.save()
        expect = os.path.join(self.directory, 'hasK2', f.get_name())
        self.assertEqual(fp_1,expect)
        fp = f.save()
        self.assertEqual(fp, None)
        # create a path of length
        p4 = make_cycle(4)
        p4.remove_edge(0, 3)
        g = File(self.directory, G=p4, logger=self.logger)
        fp_2 = g.save()
        expect = os.path.join(self.directory, 'hasK2', g.get_name(1))
        self.assertNotEqual(fp_1, fp_2)
        self.assertEqual(fp_2, expect)

    def testSaveIsomorphic2(self):
        files = ['FileComparetest1.txt',
                 'FileComparetest2.txt',
                 'FileComparetest3.txt',
                 'FileComparetest4.txt',
                 'FileComparetest5.txt',
                 'FileComparetest6.txt',
                 'FileComparetest7.txt',
                 'FileComparetest8.txt',
                 'FileComparetest9.txt',
                 'FileComparetest10.txt',
                 ]
        tests = []
        directory = os.path.join(self.directory, "test")
        for f in files:
            tests.append(File(directory, file=f, logger=self.logger))
        saved = tests[0].save()
        self.assertNotEqual(saved, None, "File should have been saved")
        for a in range(1, len(tests)):
            saved = tests[a].save()
            self.assertEqual(saved, None, "File should not have been saved")

    def testCompare(self):
        claw = make_claw()
        co_claw = make_co_claw()
        f = File(self.directory, G=claw, logger=self.logger)
        g = File(self.directory, G=claw, logger=self.logger)
        self.assertEqual(g.compare(f), True)
        self.assertEqual(f.compare(g), True)
        g = File(self.directory, G=co_claw, logger=self.logger)
        self.assertEqual(g.compare(f), False)
        self.assertEqual(f.compare(g), False)
        h = File(self.directory, G=make_cycle(4), logger=self.logger)
        self.assertEqual(h.compare(f), False)
        self.assertEqual(f.compare(h), False)

    def testCompare2(self):
        files = ['FileComparetest1.txt',
                 'FileComparetest2.txt',
                 'FileComparetest3.txt',
                 'FileComparetest4.txt',
                 'FileComparetest5.txt',
                 'FileComparetest6.txt',
                 'FileComparetest7.txt',
                 'FileComparetest8.txt',
                 'FileComparetest9.txt',
                 'FileComparetest10.txt',
                 ]
        tests = []
        directory = os.path.join(self.directory, "test")
        for f in files:
            tests.append(File(directory, file=f, logger=self.logger))
        for a in range(0, len(tests)):
            for b in range(a, len(tests)):
                result = tests[a].compare(tests[b]) 
                self.assertEqual(result, True, "Graphs should be the same")
        for a in range(len(tests) - 1, -1, -1):
            for b in range(len(tests) - 1, -1, -1):
                result = tests[a].compare(tests[b]) 
                self.assertEqual(result, True, "Graphs should be the same")

    def testCompare3(self):
        directory = os.path.join(self.directory, 'test')
        t_d = os.path.join(self.directory, 'GraphFamilies', 'ClawC4CoK4', 'hasK3')
        f = File(directory, file='FileComparetest1.txt')
        g = File(t_d, file='has_K3_edges-11_nodes-7--1.txt' )
        h = File(t_d, file='has_K3_edges-11_nodes-7--2.txt')
        print(f.compare(g))
        print(h.compare(g))

    def testLoad(self):
        claw = make_claw()
        c7 = make_cycle(7)
        co_claw = make_co_claw()
        tests = {'test1.txt': claw, 'test2.txt': c7, 'test3.txt': co_claw}
        directory = os.path.join(self.directory, "test")
        for file, expect in tests.items():
            file_obj = File(directory, file=file)
            self.assertEqual(expect.nodes() ,file_obj.G.nodes() ,
                            "Load Failed Nodes: %s" % file)
            self.assertEqual(expect.edges() ,file_obj.G.edges() ,
                                 "Load Failed :Edges %s" % file)
