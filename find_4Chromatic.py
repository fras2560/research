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
from graph.helper import make_diamond
from os import getcwd
from os.path import join
from generator import Generator2 
from file import File
import logging
from pprint import PrettyPrinter
from graph.colorable import coloring
pp = PrettyPrinter(indent = 4)

# create forbidden graph
Diamond = make_diamond()
C4 = make_cycle(4)
Claw = make_claw()
K4 = make_clique(4)

# these constants are what should change
FAMILY = "(Diamond-C4-Claw-K4)-free"
DIRECTORY = join(getcwd(), 'GraphFamilies', FAMILY)
FORBIDDEN = [Diamond, C4, Claw, K4]
STARTING = make_cycle(5)

logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
LOGGER = logging.getLogger(__name__)
# processing work 
generator = Generator2(STARTING, 5, FORBIDDEN)
index = 0
print("Started")
for graph in generator.iterate():
    LOGGER.info("Number of Nodes: %d" % len(graph.nodes()))
    if len(coloring(graph, logger=LOGGER)) == 4:
        f = File(DIRECTORY, G=graph, logger=LOGGER, base="C5-")
        fp = f.save()
        if fp is not None:
            index += 1
            print("Created Graph: %d" % index)
LOGGER.info("Complete")
print("Total Graphs Created: %d" % index)