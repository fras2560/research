"""
-------------------------------------------------------
create_graphs

a program to help create the family of graphs
and sort it based on clique number
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-10-19
-------------------------------------------------------
"""
from graph.helper import make_claw, make_cycle, make_cok4
from os import getcwd
from os.path import join
from generator import Generator
from file import File
import logging


# create forbidden graph
claw = make_claw()
c4 = make_cycle(4)
cok4 = make_cok4()

# these constants are what should change
FAMILY = "ClawC4CoK4"
DIRECTORY = join(getcwd(), 'GraphFamilies', FAMILY)
FORBIDDEN = [claw, c4, cok4]
STARTING = make_cycle(5)
logging.basicConfig(filename=FAMILY+".log", level=logging.INFO,
                            format='%(asctime)s %(message)s')
LOGGER = logging.getLogger(__name__)
# processing work
generator = Generator(STARTING, 14, FORBIDDEN)
for graph in generator.iterate():
    f = File(graph, DIRECTORY, LOGGER)
    f.save()
LOGGER.info("Complete")