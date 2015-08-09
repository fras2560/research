"""
-------------------------------------------------------
This utility module checks if any (C4,C5,4K1)-free graphs
with a C6 and no C7 are critical. 
-------------------------------------------------------
Author:  Tom LaMantia
ID:      110242560
Email:   tom.lamantia@mail.utoronto.ca
Version: 2015-08-09
-------------------------------------------------------
"""
import sys
sys.path.append("..") #Adds higher directory modules to python path
from graph.helper import make_cycle, make_cok4
from os import getcwd
from os.path import join
from utility.generator import Generator2
from utility.file import File
import logging

FORBIDDEN_SUBGRAPHS = [make_cycle(4), make_cycle(5), make_cycle(7), make_cok4()]

FAMILY = "C7-free"
DIRECTORY = join(getcwd(), 'GraphFamilies', FAMILY)
BASE_CYCLE = make_cycle(6)
BASE = "C7-free"
logging.basicConfig(filename=BASE+FAMILY+".log", level=logging.INFO, format='%(asctime)s %(message)s')
LOGGER = logging.getLogger(__name__)

generator = Generator2(BASE_CYCLE, 4, FORBIDDEN_SUBGRAPHS)
index = 0

for graph in generator.iterate():
    print("t")
    f = File(DIRECTORY, G=graph, logger=LOGGER, base=BASE)
    fp = f.save()
    if fp is not None:
        index += 1
        LOGGER.info("Unique graph found %s" % fp)
print("Total Graphs Produced: %d" % index)
print("Complete")
LOGGER.info("Total Graphs Produced %d" % index)
LOGGER.info("Complete")