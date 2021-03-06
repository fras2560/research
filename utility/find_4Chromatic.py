"""
-------------------------------------------------------
find_4Chromatic
a simple program to help find a graph G
that is (K4, Claw, Diamond, C4)-free which chromatic(G) = 4.
G is planar and by 4-color theorem know chroamtic(G) <= 4
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-10-16
-------------------------------------------------------
"""

from graph.helper import make_claw, make_cycle, make_clique
from graph.helper import make_diamond, forbidden_line_subgraphs
from os import getcwd
from os.path import join
from generator import Generator2 
from file import File
import logging
from pprint import PrettyPrinter
from graph.colorable import coloring
from networkx import complement
pp = PrettyPrinter(indent = 4)
XCHROMATIC = 5

# create forbidden graph
k4 = make_clique(XCHROMATIC)
co_k4 = complement(make_clique(4))

# these constants are what should change
FAMILY = "Line(Co-K4)-free"
DIRECTORY = join(getcwd(), 'GraphFamilies', FAMILY)
FORBIDDEN = forbidden_line_subgraphs() + [co_k4, k4]
print(FORBIDDEN)
STARTING = make_cycle(7)
BASE = "C5"
logging.basicConfig(filename=FAMILY + BASE + ".log", level=logging.INFO,
                            format='%(asctime)s %(message)s')
LOGGER = logging.getLogger(__name__)
# processing work 
generator = Generator2(STARTING, 10, FORBIDDEN)
index = 0
print("Started")
checked = 0
for graph in generator.iterate():
    if len(coloring(graph, logger=LOGGER)) >= XCHROMATIC:
        f = File(DIRECTORY, G=graph, logger=LOGGER, base="C5-")
        fp = f.save()
        if fp is not None:
            index += 1
            print("Created Graph: %d" % index)
    checked += 1
    if checked % 100 == 0:
        print("Checked %d Graphs" % checked)
LOGGER.info("Complete")
print("Total Graphs Created: %d" % index)