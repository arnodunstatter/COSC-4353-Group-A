from numpy.core.numeric import NaN
import pandas as pd
import numpy as np
from sys import exit # used to end program if an invalid keyword is given to addNode
import numpy.random as npr # used for creating random graphs (one of the __init__ functions for Graph class)
import datetime # used for giving default date to graph generator as today's date

class Graph:
    # default Attributes ------------------------------------
    ## meta-data
    name = ""
    date = ""
    description = ""
    ## bools
    isMultiGraph = False
    isDirected = False
    isWeighted = False
    ## data structures
    adjacencyLists = {} # a dictionary - each key's value is a set of tuples where the first value in the tuple is the destination node's name and every value after that is a weight
    adjacencyMatrix = pd.DataFrame() # for directed graphs rows are sources, columns are destinations - this change was made so that accessing elements with
                                    # df.loc[] (and df.at[]) will have the syntax df.loc[source,destination] instead of df.loc[destination,source]

    # Methods -----------------------------------------
    def __init__(self, **kwargs):
        if len(kwargs) == 1:
            self.makeFromTxt(**kwargs)
        else:
            self.generateGraph(**kwargs)

    '''Define graph generator method: that takes in parameters that give guidelines to the type of graph to be made (a number of nodes, a number of connections or a connections multiplier, 
    a value to use as the rng's seed, a bool for whether its directed/undirected, a bool for whether its a mulitgraph, a bool for whether connections are weighted, range of connection weights) 
    and then the method uses an rng, in conjunction with the given parameters, to decide which nodes are connected, and (if applicable) the weights of the connections.
    '''
    def generateGraph(self, seed, numNodes, numConnections, name="", date="", description="", weightsRange=None, isMultiGraph=False, isDirected=False, isWeighted=False): # random graph generator
        # set attributes
        self.name = name
        self.date = datetime.date.today()
        self.description = description
        self.isMultiGraph = isMultiGraph
        self.isDirected = isDirected
        self.isWeighted = isWeighted
        # For each numNodes initialize adjacencyMatrix and adjacencyLists
        for i in range(numNodes):
            self.addNode(str(i), "source")
            self.addNode(str(i), "destination")
        # For each numConnections, use rng to determine the source and destination (bound by numNodes) and weight (bound by weightsRange) then add that edge to adjLis and adjMat
        npr.seed(seed=seed) # for repeatability
        for edge in range(numConnections):
            source = str(npr.randint(0,numNodes))
            destination = str(npr.randint(0,numNodes))
            self.helper_makeRandEdge(numNodes, source, destination, weightsRange)

    def helper_makeRandEdge(self, numNodes, source, destination, weightsRange):
        if not self.isMultiGraph: # if it's not a multigraph then destination cannot be the same as source AND source, destination pair must not be in adjacencyLists already
            while(source == destination): #if source is the same as destination, get a new destination
                destination = str(npr.randint(0,numNodes))
            # we need all destinations that source goes to, but self.adjacencyLists.get() returns the set of tuples with the first value of each being each destination's name
            if destination in set([x[0] for x in self.adjacencyLists.get(source)]): # if it's a non multigraph and we already have an edge between source and destination, we need a new source and destination
                source = str(npr.randint(0,numNodes))
                destination = str(npr.randint(0,numNodes))
                self.helperMakeRandEdge(numNodes, source, destination, weightsRange)
        if self.isWeighted:
            weight = npr.randint(weightsRange[0],weightsRange[1]+1)
        else:
            weight = 1

        #print(f"adding an edge between {source} and {destination} with weight {weight}")
        self.addEdges(source, [destination,weight])


    def makeFromTxt(self, file): # this will read files directly
        f = open(file)
        self.name = f.readline()[len("GraphName: "):].split("\n")[0]
        self.date = f.readline()[len("Date: "):].split("\n")[0]
        self.description = f.readline()[len("Description: "):].split("\n")[0]
        self.isMultiGraph = True if f.readline()[len("MultiGraph: "):] == "T\n" else False
        self.isDirected = True if f.readline()[len("Directed: "):] == "T\n" else False
        self.isWeighted = True if f.readline()[len("Weighted: "):] == "T\n" else False
        #the remaining lines in f should be the adjacency lists
        rows = []
        for eachRow in f: # example of eachRow "A -> B 1 2, D 2\n"
            if("\n"==eachRow[len(eachRow)-1:]): # if the line ends in "\n", then remove it - example result: "A -> B 1 2, D 2"
                row = eachRow[:len(eachRow)-1]
            else: row = eachRow # otherwise do just get the line as is
            row = row.split("->") # element 0 is source node, element 2 is destination nodes and associated weights - example result: ["A ", " B 1 2, D 2"]
            row[0]=row[0].split(" ") # isolate source node's name from the space - example result: ["A",""]
            row[1]=row[1].split(",") # split destination nodes - example result: [" B 1 2"," D 2"]
            for i in range(len(row[1])): # split destination nodes up from their weights - example of result:[["","B","1","2"],["","D","2"]]]
                row[1][i] = row[1][i].split(" ")
            # row = [['A', ''], [['', 'B', '1', '2'], ['', 'D', '2']]]
            sourceNode = row[0][0]
            destinationNodes = row[1]
            for i in range(len(destinationNodes)): # ['', 'B', '1', '2'] -> ['B', '1', '2']
                destinationNodes[i] = destinationNodes[i][1:]

            for i in range(len(destinationNodes)): # this converts the weights from being strings to floats
                for j in range(len(destinationNodes[i])):
                    if j > 0: #only changes weights
                        destinationNodes[i][j] = float(destinationNodes[i][j])
            self.addNode(sourceNode, "source")
            self.addNode(sourceNode, "destination")
            if len(destinationNodes[0]) == 0: #for "Source ->" rows in .txt
                continue
            for destination in destinationNodes:
                self.addEdges(sourceNode, destination)

    def addSourceToAdjacencyMatrix(self, source):
        self.adjacencyMatrix.loc[source] = pd.Series(name=source, dtype=object)

    def addDestinationToAdjacencyMatrix(self, destination):
        self.adjacencyMatrix.insert(loc=len(self.adjacencyMatrix.columns), column=destination, value=np.NaN)
        self.adjacencyMatrix[destination] = self.adjacencyMatrix[destination].astype(object)

    def addNode(self, node, nodePurpose = None):
        #first we add it to the adjacencyLists as a source
        if self.adjacencyLists.get(node) == None: # if the adjacency List doesn't have the node present
            self.adjacencyLists.update({node: {}}) # then add it

        #now we add to the adjacencyMatrix
        if self.isDirected:
            if nodePurpose == "source": # if the node is a source, then...
                if node not in set(self.adjacencyMatrix.index): # if the node is not already a row, then...
                    # add it as a row (index)
                    if len(self.adjacencyMatrix.columns) == 0: # if we have no columns (i.e. no destinations yet)
                        if len(self.adjacencyMatrix.index) != 0: # for when we already have indexes
                            newIndex = self.adjacencyMatrix.index
                            newIndex.append(node)
                        else: # for when we have no indexes
                            newIndex = [node]
                        self.adjacencyMatrix = pd.DataFrame(index=newIndex) # re-initialize the adjMat and update the index
                    else: # we already have columns
                        self.addSourceToAdjacencyMatrix(node)
            elif nodePurpose == "destination": # if the node is a destination, then...
                if node not in set(self.adjacencyMatrix.columns): # if we don't already have it as a column, then...
                    # add it as a column
                    self.addDestinationToAdjacencyMatrix(node) # adds node as a column
            else:
                print("ERROR: Invalid keyword given as `nodePurpose` in call to `addNode()`")
                exit()
        else: # undirected, we don't care about nodePurpose
            # for undirected graphs when we add a node it will get added as both a row(source) and column(destination)
            if node not in set(self.adjacencyMatrix.columns) and node not in set(self.adjacencyMatrix.index):
                self.addDestinationToAdjacencyMatrix(node) # add as destination first so we ensure we have a column so we can...
                self.addSourceToAdjacencyMatrix(node) # add as source

    def addEdges(self, source, destList): # doesn't matter if it's directed or not, does matter if it's weighted
        destination = destList[0]
        if not self.isDirected and not self.isMultiGraph: #if it's undirected and is not a multigraph and we already have source->destination then return (don't want to double-add that edge)
            # the first condition is to prevent an exception when checking the second condition (NoneType is not iterable)
            if None != self.adjacencyLists.get(destination) and source in set([x[0] for x in self.adjacencyLists.get(destination)]):
                return
        if self.isMultiGraph or self.isWeighted:
            weights = destList[1:]
        else: #unweighted and not a multiGraph
            weights = [1]
        weights = np.asarray(weights)
        self.addNode(source, "source") # if the node is already in adjacencyLists then this will do nothing. We have this line for when this function is used later on
        self.addNode(destination, "destination")

        # do adjacencyLists first
        # first check if destination is in source's set
        found = ()
        for eachDest in self.adjacencyLists[source]: # for each destination in source's destinations
            if destination == eachDest[0]: # try to find the destination
                found = eachDest #found is now a tuple
                break #once we find it we can break this loop
        if 0 == len(found): # we never found the destination so the destination is not yet there for source
            updatedDestinations = set(self.adjacencyLists[source]) #need to keep the other destinations
            updatedDestinations.add(tuple(destList))
            self.adjacencyLists.update({source: updatedDestinations})
        else: # found the destination
            updated = list(found)
            for i in destList[1:]: #update the weights of the destination
                updated.append(i)
            updated = tuple(updated)
            self.adjacencyLists[source].remove(found)
            self.adjacencyLists[source].add(updated)

        #if it's undirected we need to do the above but for the reverse, i.e. destination->source
        revDestList = destList #reverse destination list (i.e. the `source` is used as the destination
        revDestList[0] = source
        found = ()
        if not self.isDirected and source != destination:
            for eachDest in self.adjacencyLists[destination]: #for each destination in `destination`'s destinations
                if source == eachDest[0]: # try to find `source` (as a destination)
                    found = eachDest
                    break #once we find it we can break this loop
            if 0 == len(found): # we never found `source` as a destination of `destination`'s so `source` is not yet a destination of `destination`
                updatedDestinations = set(self.adjacencyLists[destination]) #need to keep the other destinations
                updatedDestinations.add(tuple(revDestList))
                self.adjacencyLists.update({destination: updatedDestinations})
            else: # found the destination
                updated = list(found)
                for i in revDestList[1:]: #update the weights of the destination
                    updated.append(i)
                updated = tuple(updated)
                self.adjacencyLists[destination].remove(found)
                self.adjacencyLists[destination].add(updated)

        if source == '1' and destination == '0':
            mark = 'hey'
        # whether directed or not we add the weights to adjacencyMatrix
        # but are we initializing it or just appending to already existent weights?
        #if np.isnan(self.adjacencyMatrix.at[source,destination]): # we are initializing it
        if isinstance(self.adjacencyMatrix.at[source,destination], type(np.NaN)): #then it's nan so we are initializing it
            self.adjacencyMatrix.at[source,destination] = weights
        else: # we are adding a new weights to already existing weights
            self.adjacencyMatrix.at[source,destination] = np.append(self.adjacencyMatrix.at[source,destination], weights)

        if not self.isDirected and source != destination: # undirected -> add weights to both places
            #if np.isnan(self.adjacencyMatrix.at[destination,source]):  # we are initializing all weights
            if isinstance(self.adjacencyMatrix.at[destination,source], type(np.NaN)):  # then it's nan so we are initializing it
                self.adjacencyMatrix.at[destination,source] = weights
            else:  # we are adding a new weights to already existing weights
                #self.adjacencyMatrix[destination][source] = np.append(self.adjacencyMatrix[source][destination], weights)
                self.adjacencyMatrix.at[destination,source] = np.append(self.adjacencyMatrix.at[destination,source], weights)
