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
import networkx as nx
import os
from graph.helper import networkx_to_text
class File():
    def __init__(self, G, directory, logger):
        '''
        G: a networkx graph (networkx)
        directory: the filepath to the directory (filepath)
        logger: the logger to log information (logging)
        '''
        self.G = G
        self.directory = directory
        self.clique = nx.graph_clique_number(self.G)
        self.logger = logger

    def save(self):
        '''
        a method that takes a graph G and saves it to the appropriate folder
        Parameters:
        Returns:
            name: the file path of where it was saved
        '''
        name = self.get_name()
        name = self.file_path(name)
        while not (self.check_unique(name)):
            name = name[:-4] + " _1" + ".txt"
        text = networkx_to_text(self.G)
        self.logger.info("Saving Graph %s", name)
        self.logger.debug("File Text \n" + text)
        with open(name, "w") as file:
            file.write(text)
        return name

    def get_name(self):
        '''
        a method that determines the name of G
        based upon properties of the graph
        Parameters:
            
        Returns:
            name: the name of the graph
        '''
        edges = len(self.G.edges())
        nodes = len(self.G.nodes())
        name = ("has_K" + str(self.clique) + "_edges-" + str(edges) + '_nodes-'
                + str(nodes) + ".txt")
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

import unittest
import shutil
from graph.helper import make_claw, make_cycle, text_to_networkx
import logging
class Tester(unittest.TestCase):
    def setUp(self):
        self.directory = os.getcwd()
        self.k2 = os.path.join(self.directory, "hasK2")
        self.k3 = os.path.join(self.directory, "hasK3")
        self.k4 = os.path.join(self.directory, "hasK4")
        self.k5 = os.path.join(self.directory, "hasK5")
        
        self.created = [self.k2, self.k3, self.k4, self.k5]
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)

    def tearDown(self):
        for c in self.created:
            if os.path.exists(c):
                shutil.rmtree(c, ignore_errors=True)

    def testGetName(self):
        g = make_claw()
        f = File(g, self.directory, self.logger)
        self.assertEqual(f.get_name(), "has_K2_edges-3_nodes-4.txt")
        g = make_cycle(5)
        f = File(g, self.directory, self.logger)
        self.assertEqual(f.get_name(), "has_K2_edges-5_nodes-5.txt")

    def testFilePath(self):
        created = os.path.exists(self.k2)
        self.assertEqual(created, False)
        g = make_claw()
        f = File(g, self.directory, self.logger)
        name = "has_K2_edges-5nodes-5.txt"
        fp = f.file_path(name)
        self.assertEqual(os.path.join(self.directory, self.k2, name), fp)
        created = os.path.exists(self.k2)
        self.assertEqual(created, True)

    def testChequeUnique(self):
        f = File(make_claw(), self.directory, self.logger)
        fp = "does not exists"
        self.assertEqual(f.check_unique(fp), True)
        os.makedirs(self.k2)
        self.assertEqual(f.check_unique(self.k2), False)

    def testsave(self):
        g = make_claw()
        f = File(g, self.directory, self.logger)
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

