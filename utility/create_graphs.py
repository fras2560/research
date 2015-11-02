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
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from graph.helper import make_co_claw, make_cycle, make_clique, make_co_cycle
from graph.helper import make_2K2, make_co_diamond, make_cok4
from graph.helper import join as graphjoin
from os import getcwd
from os.path import join
from utility.generator import Generator2
from utility.file import File
import logging
from utility.EmailHelper import send_email


TO_ADDRESS = "fras2560@mylaurier.ca"
CREATE_MESSAGE = "Create Graphs was completed"
# create forbidden graph
c4 = make_cycle(4)
c6 = make_cycle(6)
c8 = make_cycle(8)
c10 = make_cycle(10)
k4 = make_clique(4)

coclaw = make_co_claw()
k2 = make_2K2()
cok4 = make_cok4()
codiamond = make_co_diamond()

# these constants are what should change
FAMILY = "Even-Hole"
DIRECTORY = join(getcwd(), 'GraphFamilies', FAMILY)
FORBIDDEN = [c4, c6, c8, c10, k4]
STARTING = make_co_cycle(5)
BASE = "C5"
logging.basicConfig(filename=BASE+FAMILY+".log", level=logging.INFO,
                            format='%(asctime)s %(message)s')
LOGGER = logging.getLogger(__name__)
# processing work 
generator = Generator2(STARTING, 5, FORBIDDEN)
index = 0
for graph in generator.iterate():
    f = File(DIRECTORY, G=graph, logger=LOGGER, base=BASE)
    fp = f.save()
    if fp is not None:
        index += 1
        LOGGER.info("Unique graph found %s" % fp)
print("Total Graphs Produced: %d" % index)
print("Complete")
LOGGER.info("Total Graphs Produced %d" % index)
LOGGER.info("Complete")
send_email(CREATE_MESSAGE, TO_ADDRESS)
