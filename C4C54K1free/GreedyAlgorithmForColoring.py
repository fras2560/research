"""
-------------------------------------------------------
This program attempts to color (C4,C5,4K1)-free graphs
using a greedy algorithm, which colors this graph
class by removing stable sets.
-------------------------------------------------------
Author:  Tom LaMantia
Email:   lama3790@mylaurier.ca
Version: 2015-06-15
-------------------------------------------------------
"""
import sys
sys.path.append("..")
from copy import deepcopy
from graph.helper import make_cycle, make_cok4
from graph.colorable import valid_coloring
from graph.container import induced_subgraph
from networkx.algorithms import find_cliques, maximal_independent_set
from utility.file import File
from math import ceil
from itertools import product
from os import getcwd
from os.path import join
import logging

CYCLE_LENGTH = 7
CURRENT_X_SETS = [ [] for i in range(0, CYCLE_LENGTH)]
CURRENT_Y_SETS = [ [] for i in range(0, CYCLE_LENGTH)]
FORBIDDEN_SUBGRAPHS = {make_cycle(4), make_cycle(5), make_cok4()}

GRAPH_FAMILY = "GreedyColoring"
DIRECTORY = join(getcwd(), "GraphFamilies", GRAPH_FAMILY)
MY_LOGGER = logging.getLogger(__name__)

def ConstructBaseGraph():
    global CURRENT_X_SETS, CURRENT_Y_SETS
    
    CURRENT_X_SETS = [ [i] for i in range(0, CYCLE_LENGTH)]
    CURRENT_Y_SETS = [ [] for i in range(0, CYCLE_LENGTH)]
    
    result = make_cycle(CYCLE_LENGTH)
    
    return deepcopy(result)

def GIsHFree(G, H):
    
    result = True
    
    for thisForbiddenInducedSubgraph in H:
        if induced_subgraph(G, thisForbiddenInducedSubgraph):
            result = False
            break
    return result

def AddYSet(G, setSize, addAllOptionalXYEdges, offset):
    
    y_sets = [ [] for i in range(0,CYCLE_LENGTH)]
    
    yNodes  =  list()
    for i in range(0, setSize):
        thisVertexIndex = G.number_of_nodes()
        yNodes.append(thisVertexIndex)
        G.add_node(thisVertexIndex)
        CURRENT_Y_SETS[(offset) % 7].append(thisVertexIndex)
        
        #Because Stream1 has only 1 Y set (by definition), its
        #placement does not matter. All other placements are isomorphic
        G.add_edge((offset + 0) % 7, thisVertexIndex)
        G.add_edge((offset + 1) % 7, thisVertexIndex)
        G.add_edge((offset + 2) % 7, thisVertexIndex)
        G.add_edge((offset + 3) % 7, thisVertexIndex)
        
        #Yi forms a clique
        for thisYNode in yNodes:
            if thisYNode != thisVertexIndex:
                G.add_edge(thisYNode, thisVertexIndex)
        
        #yi joins Y_i+1
        for thisCurrentYi1 in CURRENT_Y_SETS[(offset + 1) % 7]:
            G.add_edge(thisCurrentYi1, thisVertexIndex)
        #Yi joins Y_i+6    
        for thisCurrentYi6 in CURRENT_Y_SETS[(offset + 6) % 7]:
            G.add_edge(thisCurrentYi6, thisVertexIndex)
        
        #Y1 joins Xi
        for thisCurrentXi in CURRENT_X_SETS[(1 + offset) % 7]:
            G.add_edge(thisVertexIndex, thisCurrentXi)
            
        #Yi joins X_i+1    
        for thisCurrentXi2 in CURRENT_X_SETS[(2 + offset) % 7]:
            G.add_edge(thisVertexIndex, thisCurrentXi2)
            
        #We must avoid 4k1
        for thisCurrentXi6 in CURRENT_X_SETS[(0 + offset) % 7]:
            G.add_edge(thisVertexIndex, thisCurrentXi6)
            
        #The user may request optional edges, that is: Yi joins Xi+2
        if addAllOptionalXYEdges == True:
            for thisCurrentXi2 in CURRENT_X_SETS[(3 + offset) % 7]:
                G.add_edge(thisVertexIndex, thisCurrentXi2)
                
    return deepcopy(G)

def AddXSet(G, setSize, addAllOptionalXEdges, offset):
    
    currentXAtOffset = list()
    currentXAtOffset.append( offset % 7)
    
    for i in range(0, setSize):
        thisXVetexToAdd = G.number_of_nodes()
        currentXAtOffset.append(thisXVetexToAdd)
        G.add_node(thisXVetexToAdd)
        CURRENT_X_SETS[(offset) % 7].append(thisXVetexToAdd)
        
        #X is a 3-vertex
        G.add_edge((offset + 0) % 7, thisXVetexToAdd)
        G.add_edge((offset - 1) % 7, thisXVetexToAdd)
        G.add_edge((offset + 1) % 7, thisXVetexToAdd)
        
        #Xi joins X_i+1, X_i+6
        for thisXi1Vertex in CURRENT_X_SETS[(offset + 1) % 7]:
            G.add_edge(thisXVetexToAdd, thisXi1Vertex)
            
        for thisXi6Vertex in CURRENT_X_SETS[(offset + 6) % 7]:
            G.add_edge(thisXVetexToAdd, thisXi6Vertex)
        
        #X is a clique
        for thisCurrentXVertex in currentXAtOffset:
            if thisCurrentXVertex != thisXVetexToAdd:
                G.add_edge(thisCurrentXVertex, thisXVetexToAdd)
        
        #Add optional X edges if needed, that is: xi joins xi+2
        if addAllOptionalXEdges  == True:
            for thisXi2Vertex in CURRENT_X_SETS[(offset + 2) % 7]:
                G.add_edge(thisXVetexToAdd, thisXi2Vertex)
        
    return deepcopy(G)

def FindGoodStableSet(G):

    graphToSearch = deepcopy(G)
    for i in range(0, CYCLE_LENGTH):
        graphToSearch.remove_node(i)

    for i in range(0,10):
        try:
            result = maximal_independent_set(graphToSearch)
        except IndexError:
            return None
        if len(result) == 3:
            break
    
    if len(result) != 3:
        result = None

    return result

def GreedyColoring(G):
    
    graphToTest = deepcopy(G)
    result = []
    
    thisStableSet = FindGoodStableSet(G)
    
    while thisStableSet != None:
        result.append(thisStableSet)
        for thisStableVertex in thisStableSet:
            graphToTest.remove_node(thisStableVertex)
         
        thisStableSet = FindGoodStableSet(graphToTest)
    
    V = len(G.nodes())
    while len(result) < ceil(V/3):
        result.append([])
        
    if graphToTest.nodes() != []:
        for thisUncoloredNode in graphToTest.nodes():
            for color in range(0,len(result)):
                canUseThisColor = True
                for thisColoredNode in result[color]:
                    x = thisColoredNode
                    y = thisUncoloredNode
                    if((x,y) in G.edges() or (y,x) in  G.edges()):
                        canUseThisColor = False
                if canUseThisColor == True:
                    result[color].append(thisUncoloredNode)
    return result

def GenerateAllGraphsWithManyXNoY(xCardinalityUpperBound):

    t = range(1, xCardinalityUpperBound)
    graphConfigSet = set(set(product(set(t),repeat = CYCLE_LENGTH)))

    for thisGraphConfiguration in graphConfigSet:
        myGraph = ConstructBaseGraph()
        for thisSetIndex in range(0,CYCLE_LENGTH):
            if thisGraphConfiguration[thisSetIndex] >= 2:
                myGraph = AddXSet(myGraph, thisGraphConfiguration[thisSetIndex] - 1, False, thisSetIndex)
                       
        if not (GIsHFree(myGraph, FORBIDDEN_SUBGRAPHS)):
            print("ERROR!")
            print(myGraph.edges())
            f = File(DIRECTORY, G = myGraph, logger = MY_LOGGER, base="C5-")
            f.save()
            exit()
            
        coloring = GreedyColoring(myGraph)
        
        if(valid_coloring(coloring, myGraph)):
            print("Valid coloring")
        else:
            print("INVALID coloring!")
            f = File(DIRECTORY, G = myGraph, logger = MY_LOGGER, base="C5-")
            f.save()
            
        myGraph.clear()

    return

def GenerateAllGraphsWithManyXManyY(xyCardinalityUpperBound):
    
    #ALWAYS ADD X'S ***BEFORE*** adding your Y's!
    t = range(1,xyCardinalityUpperBound)
    xConfigSet = set(set(product(set(t),repeat = CYCLE_LENGTH)))
    yConfigSet = set(set(product(set(t),repeat = CYCLE_LENGTH)))
    
    badYConfigurations = set()
    #Now we need to sift through our Y sets and remove illegal ones
    #No more than 3 Y's
    for thisYConfig in yConfigSet:
        numberYSets = 0
        for i in range(0,CYCLE_LENGTH):
            if thisYConfig[i] >= 2:
                numberYSets += 1;
                if thisYConfig[(i + 3) % CYCLE_LENGTH] == 2 or thisYConfig[(i + 4) % CYCLE_LENGTH] >= 2:
                    badYConfigurations = badYConfigurations.union({thisYConfig})
                    break 
            if numberYSets > 3:
                badYConfigurations = badYConfigurations.union(set(thisYConfig))
                break

    yConfigSet.difference_update(badYConfigurations)

    graphsAnalyzedSoFar = 0
    # now we may construct our graphs!
    for thisXConfig in xConfigSet:
        for thisYConfig in yConfigSet:
            myGraph = ConstructBaseGraph()
            for i in range(0,CYCLE_LENGTH):
                if thisXConfig[i] >= 2:
                    myGraph = AddXSet(myGraph, thisXConfig[i] - 1, False, i)
            for i in range(0,CYCLE_LENGTH):
                if thisYConfig[i] >= 2:
                    myGraph = AddYSet(myGraph, thisXConfig[i] - 1, False, i)
         
            if not (GIsHFree(myGraph, FORBIDDEN_SUBGRAPHS)):
                print("ERROR!")
                f = File(DIRECTORY, G = myGraph, logger = MY_LOGGER, base="C5-")
                f.save()
                exit()
              
            coloring = GreedyColoring(myGraph)
             
            if valid_coloring(coloring, myGraph):
                print("Valid Coloring")
            else:
                print("INVALID coloring!")
                f = File(DIRECTORY, G = myGraph, logger = MY_LOGGER, base="C5-")
                f.save()
                 
            myGraph.clear()
            graphsAnalyzedSoFar += 1
            print("Graphs Analyzed: {0}:" .format(graphsAnalyzedSoFar))

    return

GenerateAllGraphsWithManyXManyY(3)



