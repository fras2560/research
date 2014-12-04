"""
-------------------------------------------------------
find_critical
just a combination where it create_graphs and then
only saves the critical graph
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-10-16
-------------------------------------------------------
"""
from graph.helper import make_cycle, make_cok4
from graph.helper import forbidden_line_subgraphs
from graph import DalGraph
import os
from generator import Generator2 
from file import File
import logging
from pprint import PrettyPrinter
pp = PrettyPrinter(indent = 4)
from multiprocessing import Process, Lock
FORBIDDEN = forbidden_line_subgraphs() + [make_cok4()]
DIRECTORY=os.path.join(os.getcwd(), "GraphFamilies", "Line(Co-K4)-free")
STARTING = make_cycle(5)
VERTICES = 2
logging.basicConfig(filename="finding_critical.log", level=logging.INFO,
                            format='%(asctime)s %(message)s')
LOGGER = logging.getLogger(__name__)
GENERATOR = Generator2(STARTING, 2, FORBIDDEN, logger=LOGGER).iterate()
FOUND = 0
def process(lock):
    work = True
    print("Process")
    while work:
        try:
            lock.acquire()
            g = next(GENERATOR)
            lock.release()
            d = DalGraph(graph=g, logger=LOGGER)
            if d.is_critical():
                f = File(DIRECTORY, G=g, logger=LOGGER)
                fp = f.save()
                if fp is not None:
                    lock.acquire()
                    FOUND += 1
                    lock.release()
        except StopIteration:
            lock.release()
            work = False
        except:
            lock.release()
            print('''
                    -------------------
                    Weird error
                    -------------------
                ''')
            work = False
    print("Done")
    return

def go():
    lock = Lock()
    processes = []
    for i in range(5):
        pid = Process(target=process, args=[lock])
        pid.start()
        processes.append(pid)
    for p in processes:
        p.join()
    for p in processes:
        p.terminate()

if __name__ == '__main__':
    go()