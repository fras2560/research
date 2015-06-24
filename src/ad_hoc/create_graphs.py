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
from graph.helper import make_co_claw, make_cycle, make_clique, make_co_cycle
from graph.helper import make_2K2, make_co_diamond, make_cok4
from graph.helper import join as graphjoin
from os import getcwd
from os.path import join
from generator import Generator2
from file import File
import logging
from EmailHelper import send_email
from config import TO_ADDRESS, CREATE_MESSAGE

# create forbidden graph
coclaw = make_co_claw()
k2 = make_2K2()
cok4 = make_cok4()
codiamond = make_co_diamond()

# these constants are what should change
FAMILY = "Coclaw-Codiamond-Cok4-Coc4"
DIRECTORY = join(getcwd(), 'GraphFamilies', FAMILY)
FORBIDDEN = [coclaw, k2, cok4, codiamond]
STARTING = make_co_cycle(9)
BASE = "C9-Bar-"
logging.basicConfig(filename=BASE+FAMILY+".log", level=logging.INFO,
                            format='%(asctime)s %(message)s')
LOGGER = logging.getLogger(__name__)
# processing work 
generator = Generator2(STARTING, 4, FORBIDDEN)
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
