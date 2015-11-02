"""
-------------------------------------------------------
A conjecture made that if G is (kite, Even-hole)-free then the following hold:
    1. G is (diamond)-free
    2. G contains a clique cutset
-------------------------------------------------------
Author:  Dallas Fraser
Email:   fras2560@mylaurier.ca
Version: 2015-10-21
-------------------------------------------------------
"""
import sys
sys.path.append("..") # Adds higher directory to python modules path.

from graph.clique_cutset import clique_cutset
from graph.helper import make_diamond, make_cycle, make_kite, make_wheel
from os import getcwd
from os.path import join

from utility.generator import Generator
import logging
from utility.file import File
from graph.container import induced_subgraph
logging.basicConfig(filename="find_special_graph.log", level=logging.INFO,
                            format='%(asctime)s %(message)s')
LOGGER = logging.getLogger(__name__)

REQUIREMENT = 4
DROPS  = 5
MYPATH = join(getcwd(), "special_graphs")

def check_graph(drops, graph, forbidden):
    for g in Generator(graph, drops, forbidden, logger=LOGGER).iterate():
        if special_graph(g):
            f = File(MYPATH, G=g, logger=LOGGER, base="")
            fp = f.save()
            if fp is not None:
                LOGGER.info("Found the special graph")
                print("Found the special graph")

def go():
    forbidden = [make_kite(),
                 make_cycle(4),
                 make_cycle(6),
                 make_cycle(8),
                 make_wheel(6)]
    g = make_cycle(5)
    check_graph(DROPS, g, forbidden)
    return

def special_graph(g):
    valid = False
    if induced_subgraph(g, make_diamond()) is not None:
        if clique_cutset(g) is None:
            valid = True
    return valid

if __name__ == "__main__":
    go()