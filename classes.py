from numpy.core.numeric import NaN
import pandas as pd
import numpy as np
from sys import exit

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
                                    # df.loc[] will have the syntax df.loc[source,destination] instead of df.loc[destination,source]

    # Methods -----------------------------------------
    def __init__(self, file): # this will read files directly
        f = open(file)
        self.name = f.readline()[len("GraphName: "):].split("\n")[0]
        self.date = f.readline()[len("Date: "):].split("\n")[0]
        self.description = f.readline()[len("Description: "):].split("\n")[0]
        self.isMultiGraph = True if f.readline()[len("MultiGraph: "):] == "T\n" else False
        self.isDirected = True if f.readline()[len("Directed: "):] == "T\n" else False
        self.isWeighted = True if f.readline()[len("Weighted: "):] == "T\n" else False
        #the remaining lines in f should be the adjacency lists
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
            self.addNode(sourceNode, "source") # adds sourceNode to adjacencyList and adjacencyMatrix

            if len(destinationNodes[0]) == 0: #for "Source ->" rows in .txt
                continue

            for destination in destinationNodes:
                self.addEdges(sourceNode, destination)
                print("adding row:\t", eachRow[:len(eachRow)-1])
                print("adjacencyMatrix:\n", self.adjacencyMatrix,"\n")
                print("adjacencyLists:\n",self.adjacencyLists, "\n")
                print(f"type at source {sourceNode}, destination {destination[0]} is {type(self.adjacencyMatrix.loc[sourceNode,destination[0]])}\n\n\n")

    def addSourceToAdjacencyMatrix(self, source):
        self.adjacencyMatrix.loc[source] = pd.Series(name=source, dtype='object')

    def addDestinationToAdjacencyMatrix(self, destination):
        self.adjacencyMatrix.insert(loc=len(self.adjacencyMatrix.columns), column=destination, value=np.NaN)
        self.adjacencyMatrix[destination] = self.adjacencyMatrix[destination].astype(object)

    def addNode(self, node, nodePurpose = None):
        #first we add it to the adjacencyLists as a source
        if self.adjacencyLists.get(node) is None: # if the adjacency List doesn't have the node present
            self.adjacencyLists.update({node: {}}) # then add it

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

        if self.isMultiGraph or self.isWeighted:
            weights = destList[1:]
        else: #unweighted and not a multiGraph
            weights = [1]
        weights = np.array(weights)
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

        # do adjacencyMatrix now
        # first check if destination is in adjacencyMatrix as an index (i.e. a row)
        if destination not in set(self.adjacencyMatrix.columns): # if the destination is not already a column in the adjMat then we need to add it
            self.addDestinationToAdjacencyMatrix(destination)

        # whether directed or not we add the weights to adjacencyMatrix
        # but are we initializing it or just appending to already existent weights?
        if np.isnan(self.adjacencyMatrix.loc[source,destination]): # we are initializing it
            type1 = type(weights)
            self.adjacencyMatrix.loc[source,destination] = weights
            type2 = type(self.adjacencyMatrix.loc[source,destination])
        #if np.isnan(self.adjacencyMatrix[destination][source]):
            #self.adjacencyMatrix[destination][source] = np.array(weights)
        else: # we are adding a new weights to already existing weights
            #self.adjacencyMatrix[source][destination] = np.append(self.adjacencyMatrix[source][destination], weights)
            self.adjacencyMatrix.loc[source,destination] = np.append(self.adjacencyMatrix.loc[source,destination], weights)

        if not self.isDirected: # undirected -> add weights to both places
            if np.isnan(self.adjacencyMatrix.loc[source, destination]):  # we are initializing all weights
                #self.adjacencyMatrix[destination][source] = np.array(weights)
                self.adjacencyMatrix.loc[destination,source] = weights
            else:  # we are adding a new weights to already existing weights
                #self.adjacencyMatrix[destination][source] = np.append(self.adjacencyMatrix[source][destination], weights)
                self.adjacencyMatrix.loc[destination,source] = np.append(self.adjacencyMatrix[source][destination], weights)

# class GraphCollection:
#     def __init__(self, file):
#         f = open(file)