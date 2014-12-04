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
from multiprocessing import Process, Lock, Queue
from queue import Empty
import time
FORBIDDEN = forbidden_line_subgraphs() + [make_cok4(), make_cycle(7)]
DIRECTORY=os.path.join(os.getcwd(), "GraphFamilies", "Line(Co-K4)-free")
STARTING = make_cycle(5)
VERTICES = 2
logging.basicConfig(filename="finding_critical.log", level=logging.INFO,
                            format='%(asctime)s %(message)s')
LOGGER = logging.getLogger(__name__)
DROPS = 1
FOUND = 0
class Counter():
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def get(self):
        return self.count

COUNTER = Counter()

def consume(lock, graphs, done, critical):
    while done.empty():
        try:
            g = graphs.get(block=True, timeout=5)
            d = DalGraph(graph=g, logger=LOGGER)
            if d.is_critical():
                f = File(DIRECTORY, G=g, logger=LOGGER)
                fp = f.save()
                if fp is not None:
                    critical.put(fp)
        except Empty:
            print("Empty")
            pass
    return

def work(lock, graphs, done):
    added = 0
    for graph in Generator2(STARTING, 1, FORBIDDEN, logger=LOGGER).iterate():
        while graphs.full():
            time.sleep(1)
        graphs.put(graph)
        added += 1
        if added % 1000 == 0:
            print("Checked %d" % added)
    done.put("Done Baby")
    print("Closing the graph pool")
    return

def go():
    lock = Lock()
    graphs = Queue()
    done = Queue()
    critical_graphs = Queue()
    consumers = []
    worker = Process(target=work, args=[lock, graphs, done])
    worker.start()
    for _i in range(5):
        pid = Process(target=consume, args=[lock, graphs,
                                             done, critical_graphs])
        pid.start()
        consumers.append(pid)
    worker.join()
    for p in consumers:
        p.join()
    for p in consumers:
        p.terminate()
    worker.terminate()
    created = critical_graphs.qsize()
    print("Total Critical Graphs found: %d" % created)

if __name__ == '__main__':
    go()