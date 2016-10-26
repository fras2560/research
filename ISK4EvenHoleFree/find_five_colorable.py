"""
-------------------------------------------------------
a program to find if there is a five colorable (ISK4, even-hole) graph
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2015-09-16
-------------------------------------------------------
"""
# imports
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from networkx.algorithms import cycle_basis
from graph.clique_cutset import clique_cutset
import copy
from graph.colorable import coloring
from utility.file import File
from utility.generator import Generator
from graph.helper import make_cycle, make_clique, make_co_twin_c5
import logging
from os.path import join
from os import getcwd

# constants
REQUIREMENT = 4

logging.basicConfig(filename="dallas_conjecture.log", level=logging.INFO,
                            format='%(asctime)s %(message)s')
LOGGER = logging.getLogger(__name__)

DROPS  = 10
FORBIDDEN = [make_clique(4), make_co_twin_c5(),make_cycle(4), make_cycle(6), make_cycle(8)]
MYPATH = join(getcwd(), "counter_example", )
GRAPH = make_cycle(5)

def go():
    count = 0
    for g in Generator(GRAPH, DROPS, FORBIDDEN, logger=LOGGER).iterate():
        count += 1
        if not conjecture_holds(g):
            f = File(MYPATH, G=g, logger=LOGGER, base="")
            fp = f.save()
            LOGGER.info("Found the special graph")
            print("Found the special graph")
        if count % 1000 == 0:
            print("Checked {} graphs".format(count))
    print("Done")

def conjecture_holds(G):
    '''
    a function that checks if the above conjecture holds
    Parameters:
        G: the graph to check (networkx)
    Returns:
        valid: True if held, False otherwise (boolean)
    '''
    valid = True
    if len(coloring(G)) >= 5:
        valid = False
    return valid

if __name__ == "__main__":
    go()
