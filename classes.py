import numpy as np
import pandas as pd
from sys import exit  # used to end program if an invalid keyword is given to addNode
import numpy.random as npr  # used for creating random graphs (one of the __init__ functions for Graph class)
import datetime  # used for giving default date to graph generator as today's date
import copy
from math import floor


class Graph:
    # default Attributes ------------------------------------
        # meta-data
    name = ""
    date = ""
    description = ""
        # bools
    isMultiGraph = False
    isDirected = False
    isWeighted = False
    ## data structures
    adjacencyLists = {}  # a dictionary - each key's value is a set of tuples where the first value in the tuple is the destination node's name and every value after that is a weight
    adjacencyMatrix = pd.DataFrame()  # for directed graphs rows are sources, columns are destinations - this change was made so that accessing elements with

    # df.loc[] (and df.at[]) will have the syntax df.loc[source,destination] instead of df.loc[destination,source]

    # Methods


class CollectionOfGraphs:
    # Attributes
        # meta-data
    name = ""
    date = ""
    description = ""
        # data-structure
    Graphs = []

    # Methods