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
    def __init__(self, **kwargs):
        # The __init__ constructor wasn't setting the default values by default, so we added the next 8 lines to force the default values at the beginning of each constructor call
        self.name = ""
        self.date = ""
        self.description = ""
        self.isMultiGraph = False
        self.isDirected = False
        self.isWeighted = False
        self.adjacencyLists = {}
        self.adjacencyMatrix = pd.DataFrame()

        if len(kwargs) == 1 or len(kwargs) == 2:
            self.makeFromTxt(**kwargs)
        else:
            self.generateGraph(**kwargs)

    def generateGraph(self, seed, numNodes, numConnections, name="", date="", description="", weightsRange=None,
                      isMultiGraph=False, isDirected=False, isWeighted=False):  # random graph generator
        # set attributes
        self.name = name
        if date == "":
            self.date = datetime.date.today()
        else:
            self.date = date
        self.description = description
        self.isMultiGraph = isMultiGraph
        self.isDirected = isDirected
        self.isWeighted = isWeighted
        # For each numNodes initialize adjacencyMatrix and adjacencyLists
        for i in range(numNodes):
            self.addNode(str(i), "source")
            self.addNode(str(i), "destination")
        # For each numConnections, use rng to determine the source and destination (bound by numNodes) and weight (bound by weightsRange) then add that edge to adjLis and adjMat
        npr.seed(seed=seed)  # for repeatability
        for edge in range(numConnections):
            source = str(npr.randint(0, numNodes))
            destination = str(npr.randint(0, numNodes))
            self.helperMakeRandEdge(numNodes, source, destination, weightsRange)

    def helperMakeRandEdge(self, numNodes, source, destination, weightsRange):
        if not self.isMultiGraph:  # if it's not a multigraph then (destination cannot be the same as source) AND (source, destination pair must not be in adjacencyLists already), while either constraint is broken, reselect source and destination
            counter = 0
            while source == destination or destination in set([x[0] for x in self.adjacencyLists.get(source)]):
                if counter > 10000:
                    print(f"Breaking an infinite while-loop in the construction of Graph: {self.name}, with source: {source}, and destination: {destination}")
                    exit(1)
                source = str(npr.randint(0,numNodes))
                destination = str(npr.randint(0, numNodes))
                counter += 1
        if self.isWeighted:
            weight = npr.randint(weightsRange[0], weightsRange[1] + 1)
        else:
            weight = 1

        self.addEdges(source, [destination, weight])
        #print(f"adding an edge between {source} and {destination} with weight {weight}","\n",self.adjacencyLists,"\n",self.adjacencyMatrix,"\n")

    def makeFromTxt(self, file, f=None):  # this will read files directly
        needToClose = False
        if None == f:
            f = open(file)
            needToClose = True
        self.name = f.readline()[len("Graph Name: "):].split("\n")[0]
        self.date = f.readline()[len("Date: "):].split("\n")[0]
        self.description = f.readline()[len("Description: "):].split("\n")[0]
        self.isMultiGraph = True if f.readline()[len("MultiGraph: "):] == "T\n" else False
        self.isDirected = True if f.readline()[len("Directed: "):] == "T\n" else False
        self.isWeighted = True if f.readline()[len("Weighted: "):] == "T\n" else False
        # the remaining lines in f should be the adjacency lists
        rows = []
        for eachRow in f:  # example of eachRow "A -> B 1 2, D 2\n"
            # if the row is empty (other than the new line marker) then return to calling function - necessary to enable CollectionOfGraphs.makeFromTxt() to call this function
            if eachRow == "\n":
                return
            # if the line ends in "\n", then remove it - example result: "A -> B 1 2, D 2"
            if "\n" == eachRow[len(eachRow) - 1:]:
                row = eachRow[:len(eachRow) - 1]
            else:
                row = eachRow  # otherwise do just get the line as is
            # element 0 is source node, element 2 is destination nodes and associated weights - example result: ["A ", " B 1 2, D 2"]
            row = row.split("->")
            row[0] = row[0].split(" ")  # isolate source node's name from the space - example result: ["A",""]
            row[1] = row[1].split(",")  # split destination nodes - example result: [" B 1 2"," D 2"]
            # split destination nodes up from their weights - example of result:[["","B","1","2"],["","D","2"]]]
            for i in range(len(row[1])):
                row[1][i] = row[1][i].split(" ")
            # row = [['A', ''], [['', 'B', '1', '2'], ['', 'D', '2']]]
            sourceNode = row[0][0]
            destinationNodes = row[1]
            for i in range(len(destinationNodes)):  # ['', 'B', '1', '2'] -> ['B', '1', '2']
                destinationNodes[i] = destinationNodes[i][1:]

            for i in range(len(destinationNodes)):  # this converts the weights from being strings to floats
                for j in range(len(destinationNodes[i])):
                    if j > 0:  # only changes weights
                        if float(destinationNodes[i][j]) == int(destinationNodes[i][j]):
                            destinationNodes[i][j] = int(destinationNodes[i][j])
                        else:
                            destinationNodes[i][j] = float(destinationNodes[i][j])
            self.addNode(sourceNode, "source")
            self.addNode(sourceNode, "destination")
            if len(destinationNodes[0]) == 0:  # for "Source ->" rows in .txt
                continue
            for destination in destinationNodes:
                self.addEdges(sourceNode, destination)

        if needToClose:
            f.close()

    def addSourceToAdjacencyMatrix(self, source):
        self.adjacencyMatrix.loc[source] = pd.Series(name=source, dtype=object)

    def addDestinationToAdjacencyMatrix(self, destination):
        self.adjacencyMatrix.insert(loc=len(self.adjacencyMatrix.columns), column=destination, value=np.NaN)
        self.adjacencyMatrix[destination] = self.adjacencyMatrix[destination].astype(object)

    def addNode(self, node, nodePurpose="source"):
        # first we add it to the adjacencyLists as a source
        if self.adjacencyLists.get(node) == None:  # if the adjacency List doesn't have the node present
            self.adjacencyLists.update({node: {}})  # then add it

        # now we add to the adjacencyMatrix
        if self.isDirected:
            if nodePurpose == "source":  # if the node is a source, then...
                if node not in set(self.adjacencyMatrix.index):  # if the node is not already a row, then...
                    # add it as a row (index)
                    if len(self.adjacencyMatrix.columns) == 0:  # if we have no columns (i.e. no destinations yet)
                        if len(self.adjacencyMatrix.index) != 0:  # for when we already have indexes
                            newIndex = self.adjacencyMatrix.index
                            newIndex.append(node)
                        else:  # for when we have no indexes
                            newIndex = [node]
                        self.adjacencyMatrix = pd.DataFrame(
                            index=newIndex)  # re-initialize the adjMat and update the index
                    else:  # we already have columns
                        self.addSourceToAdjacencyMatrix(node)
            elif nodePurpose == "destination":  # if the node is a destination, then...
                if node not in set(self.adjacencyMatrix.columns):  # if we don't already have it as a column, then...
                    # add it as a column
                    self.addDestinationToAdjacencyMatrix(node)  # adds node as a column
            else:
                print("ERROR: Invalid keyword given as `nodePurpose` in call to `addNode()`")
                exit()
        else:  # undirected, we don't care about nodePurpose
            # for undirected graphs when we add a node it will get added as both a row(source) and column(destination)
            if node not in set(self.adjacencyMatrix.columns) and node not in set(self.adjacencyMatrix.index):
                self.addDestinationToAdjacencyMatrix(
                    node)  # add as destination first so we ensure we have a column so we can...
                self.addSourceToAdjacencyMatrix(node)  # add as source

    def addEdges(self, source, destList):  # doesn't matter if it's directed or not, does matter if it's weighted
        destination = destList[0]
        if not self.isDirected and not self.isMultiGraph:  # if it's undirected or is not a multigraph and we already have source->destination then return (don't want to double-add that edge)
            # the first condition is to prevent an exception when checking the second condition (NoneType is not iterable)
            if None != self.adjacencyLists.get(destination) and source in set([x[0] for x in self.adjacencyLists.get(destination)]):
                return
        if self.isMultiGraph or self.isWeighted:
            weights = destList[1:]
        else:  # unweighted and not a multiGraph
            weights = [1]
        weights = np.asarray(weights)
        self.addNode(source, "source")  # if the node is already in adjacencyLists then this will do nothing. We have this line for when this function is used later on
        self.addNode(destination, "destination")

        # do adjacencyLists first
        # first check if destination is in source's set
        found = ()
        for eachDest in self.adjacencyLists[source]:  # for each destination in source's destinations
            if destination == eachDest[0]:  # try to find the destination
                found = eachDest  # found is now a tuple
                break  # once we find it we can break this loop
        if 0 == len(found):  # we never found the destination so the destination is not yet there for source
            updatedDestinations = set(self.adjacencyLists[source])  # need to keep the other destinations
            updatedDestinations.add(tuple(destList))
            self.adjacencyLists.update({source: updatedDestinations})
        else:  # found the destination
            updated = list(found)
            for i in destList[1:]:  # update the weights of the destination
                updated.append(i)
            updated = tuple(updated)
            self.adjacencyLists[source].remove(found)
            self.adjacencyLists[source].add(updated)

        # if it's undirected we need to do the above but for the reverse, i.e. destination->source
        revDestList = destList  # reverse destination list (i.e. the `source` is used as the destination
        revDestList[0] = source
        found = ()
        if not self.isDirected and source != destination:
            for eachDest in self.adjacencyLists[destination]:  # for each destination in `destination`'s destinations
                if source == eachDest[0]:  # try to find `source` (as a destination)
                    found = eachDest
                    break  # once we find it we can break this loop
            if 0 == len(
                    found):  # we never found `source` as a destination of `destination`'s so `source` is not yet a destination of `destination`
                updatedDestinations = set(self.adjacencyLists[destination])  # need to keep the other destinations
                updatedDestinations.add(tuple(revDestList))
                self.adjacencyLists.update({destination: updatedDestinations})
            else:  # found the destination
                updated = list(found)
                for i in revDestList[1:]:  # update the weights of the destination
                    updated.append(i)
                updated = tuple(updated)
                self.adjacencyLists[destination].remove(found)
                self.adjacencyLists[destination].add(updated)


        # whether directed or not we add the weights to adjacencyMatrix
        # but are we initializing it or just appending to already existent weights?
        # if np.isnan(self.adjacencyMatrix.at[source,destination]): # we are initializing it
        if isinstance(self.adjacencyMatrix.at[source, destination],
                      type(np.NaN)):  # then it's nan so we are initializing it
            self.adjacencyMatrix.at[source, destination] = weights
        else:  # we are adding a new weights to already existing weights
            self.adjacencyMatrix.at[source, destination] = np.append(self.adjacencyMatrix.at[source, destination],
                                                                     weights)

        if not self.isDirected and source != destination:  # undirected -> add weights to both places
            # if np.isnan(self.adjacencyMatrix.at[destination,source]):  # we are initializing all weights
            if isinstance(self.adjacencyMatrix.at[destination, source],
                          type(np.NaN)):  # then it's nan so we are initializing it
                self.adjacencyMatrix.at[destination, source] = weights
            else:  # we are adding a new weights to already existing weights
                # self.adjacencyMatrix[destination][source] = np.append(self.adjacencyMatrix[source][destination], weights)
                self.adjacencyMatrix.at[destination, source] = np.append(self.adjacencyMatrix.at[destination, source],
                                                                         weights)

    def deleteNode(self, node):
        # first remove all edges involving node
        sources = self.adjacencyMatrix.columns
        destinations = self.adjacencyMatrix.index
        for source in sources:
            self.deleteEdges(source=source, destination=node, all=True)
        for destination in destinations:
            self.deleteEdges(source=node, destination=destination, all=True)

        #remove the node from the adjacencyLists' keys
        self.adjacencyLists.pop(node)
        #remove node from adjacencyMatrix's rows (sources)
        self.adjacencyMatrix.drop(index=node, inplace=True)
        self.adjacencyMatrix.drop(columns=node, inplace=True)

    def deleteEdges(self, source, destination, all=False, weightsToRemove=None, secondCall=False):
        # if all is True or self.isMultigraph is False then we remove all edges between source and destination
        if all or not self.isMultiGraph:
            # adjacencyLists
            destinations = self.adjacencyLists.get(source)
            newDestinations = set([])
            for dest in destinations:
                if dest[0] != destination:
                    newDestinations.add(dest)
            self.adjacencyLists.update({source:newDestinations})
            # adjacencyMatrix
            self.adjacencyMatrix.at[source, destination] = np.NaN

        # else if weights != None then delete 1 edge from source to destination for every weight specified in weightsToRemove, having the weight specified in weightsToRemove
        elif weightsToRemove != None:
            # adjacencyLists
            destinations = self.adjacencyLists.get(source)
            newDestinations = set([])
            for dest in destinations:
                if dest[0] != destination:
                    newDestinations.add(dest)
                else:
                    newDest = [dest[0], *list(removeFromList(dest[1:], weightsToRemove))]
                    newDestinations.add(tuple(newDest))
            self.adjacencyLists.update({source:newDestinations})

            # adjacencyMatrix
            newWeights = removeFromList(self.adjacencyMatrix.at[source,destination], weightsToRemove)
            self.adjacencyMatrix.at[source,destination] = newWeights

        # else if all==False and self.isMultiGraph==True and weights==None, then...
        # print error message
        else:
            print("ERROR: deleteEdges() doesn't know which edges to remove. Please specify weightsToRemove as a list or array-like. If the graph is unweighted, pass as many 1's as you want removed.")
            exit()

        if secondCall: # ends recursion - dont' need a third call
            return
        # if it's undirected, call delete edge in the opposite order, pass down other parameters
        if not self.isDirected:
            self.deleteEdges(source=destination, destination=source, all=all, weightsToRemove=weightsToRemove, secondCall=True)
