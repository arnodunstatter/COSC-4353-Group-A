import numpy as np
import pandas as pd
from sys import exit  # used to end program if an invalid keyword is given to addNode
import numpy.random as npr  # used for creating random graphs (one of the __init__ functions for Graph class)
import datetime  # used for giving default date to graph generator as today's date
import copy
from math import floor


class Graph:
    # default Attributes ------------------------------------------------------------------------
    ## meta-data
    name = ""
    date = ""
    description = ""
    ## bools
    isMultiGraph = False
    isDirected = False
    isWeighted = False
    ## data structures
    adjacencyLists = {}  # a dictionary - each key's value is a set of tuples where the first value in the tuple is the destination node's name and every value after that is a weight
    adjacencyMatrix = pd.DataFrame()  # for directed graphs rows are sources, columns are destinations


    # Methods ------------------------------------------------------------------------

    ## Initializers
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

    def copy(self):
            return copy.deepcopy(self)



    ## Adders
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

        if source == '1' and destination == '0':
            mark = 'hey'
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



    ## Deleters
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
        #a helper function: basically set difference but with duplicate values
        def removeFromList(original, removables):
            #a helper function that sorts an arrayLike and then searches for a val, if found returns the index, otherwise returns None
            def sort_n_search(arrayLike, val):
                sortedArrayLike = np.sort(arrayLike)
                insertionIndex = np.searchsorted(sortedArrayLike, val)
                if insertionIndex >= len(sortedArrayLike) or sortedArrayLike[insertionIndex] != val:
                    return None
                else:
                    return insertionIndex

            removables = removables.copy() #we don't want to alter the original object so we get a copy
            original = np.sort(original)  #sort the original list
            returnMe = [] #where we will accumulate values not in removables

            #for each value, i, in original, add only so many instances to returnMe as do not exist in removables - i.e. removeFromList([1,1], [1]) returns [1] - kind of like a set difference, but with duplicates
            j = 0
            for i in range(len(original)):
                if sort_n_search(removables[j:], original[i]) == None:
                    returnMe.append(original[i])
                else: j+=1
            return np.asarray(returnMe)

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



    ## Output
    def formattedAdjacencyList(self):
        '''
        formats the following:
        {"a":{("b", 1, 2),("c", 1)},
        "b":{("a", 1, 2)},
        "c":{("a", 1)}}
        to a string like this:
        "a -> b 1 2, c 1
        b -> a 1 2
        c -> a 1"
        and returns it
        '''
        formAdjLists = ""
        counter1 = 0
        for key in self.adjacencyLists:
            formAdjLists += key + " ->"
            destinations = self.adjacencyLists.get(key)
            counter2 = 0 #used to determine if we are at the last element in the set - we don't want to add a comma if we are at the last destination for that key(source)
            for dest in destinations:
                for val in dest:
                    formAdjLists += " " + str(val)

                if counter2 != len(destinations)-1:
                    formAdjLists += ","

                counter2 += 1
            if counter1 != len(self.adjacencyLists)-1:
                formAdjLists += "\n"
            counter1 += 1
        return formAdjLists

    def display(self):
        print(f"Name: {self.name}")
        print(f"Date: {self.date}")
        print(f"Description: {self.description}")
        print(f"Settings: isMultiGraph={self.isMultiGraph}, isDirected={self.isDirected}, isWeighted={self.isWeighted}")
        print("Adjacency Lists:")
        print(self.formattedAdjacencyList())
        print("Adjacency Matrix:")
        print(self.adjacencyMatrix)

    def writeToTxt(self, fileName, flag="w"):
        thisFile = open(fileName, flag)
        thisFile.write("Graph Name: " + self.name + "\n")
        thisFile.write("Date: " + str(self.date) + "\n")
        thisFile.write("Description: " + self.description + "\n")
        isMultiGraph = "T" if self.isMultiGraph else "F"
        thisFile.write("MultiGraph: " + isMultiGraph + "\n")
        isDirected = "T" if self.isDirected else "F"
        thisFile.write("Directed: "+isDirected + "\n")
        isWeighted = "T" if self.isWeighted else "F"
        thisFile.write("Weighted: " + isWeighted + "\n")
        thisFile.write(self.formattedAdjacencyList())
        thisFile.close()



    ## Evaluation
    def isSymmetric(self):
        return self.adjacencyMatrix.size > 0 and self.adjacencyMatrix.equals(self.adjacencyMatrix.transpose())

    def evaluateSymmetry(self):
        #based on whether the graph is directed or not we should be able to predict if it's symmetric or not.
        #Here we print our prediction and the reality, ex:
        #"Expected: symmetric
        #Actual: asymmetric"
        expected = "symmetric" if not self.isDirected else "asymmetric"
        if self.isSymmetric():
            actual = "symmetric"
        else:
            actual = "asymmetric"
        print(f"Expected: {expected}\nActual: {actual}")
        print("\n")

    def equals(self, graph2):
        # this compares two graphs and returns true iff they have all the same node names and same connections between said nodes
        # this returns false even if the two graphs are equivalent (but have different node names)
        # furthermore, this function assumes that the adjacencyLists objects in each graph will correspond with their respective adjacencyMatrix so
            # only the adjacencyMatrices are compared
        #first need to sort the columns and rows of both
        self.adjacencyMatrix.sort_index(axis=1, inplace=True)
        self.adjacencyMatrix.sort_index(axis=0, inplace=True)
        graph2.adjacencyMatrix.sort_index(axis=1, inplace=True)
        graph2.adjacencyMatrix.sort_index(axis=0, inplace=True)
        #now that both are sorted we compare with pd.DataFrame.equals()
        return self.adjacencyMatrix.equals(graph2.adjacencyMatrix)


class CollectionOfGraphs:
    # Attributes
        # meta-data
    name = ""
    date = ""
    description = ""
        # data-structure
    Graphs = []

    # Methods
    def __init__(self, *arg):
        self.name = ""
        self.date = ""
        self.description = ""
        self.Graphs = []

        if len(arg) == 1:
            self.makeFromTxt(arg[0])
        else:
            self.makeFromGenerator(arg[0],arg[1],arg[2],arg[3])

    def makeFromTxt(self, fileName):
        f = open(fileName)
        self.name = f.readline()[len("Graph Collection Name: "):].split("\n")[0]
        self.date = f.readline()[len("Date: "):].split("\n")[0]
        self.description = f.readline()[len("Description: "):].split("\n")[0]
        # need to move read-stream marker forward to where the graph specifications begin
        f.readline()
        f.readline()
        while True: # there's probably a better way to do this, but we're running out of time. Will fix later
            g = Graph(file=fileName, f=f) # make the graph from the text file
            # if we read in an empty line, our g object will be empty - that's how we detect the eof and break the while loop
            if len(g.adjacencyLists)==0 and len(g.adjacencyMatrix.index)==0 and len(g.adjacencyMatrix.columns)==0 and g.name=="" and g.description=="":
                del g
                break
            self.Graphs.append(g)
        f.close()

    def makeFromGenerator(self, name, date, description, graphParams):
        self.name = name
        if date == "":
            self.date = datetime.date.today()
        else:
            self.date = date
        self.description = description
        # def generateGraph(self, seed, numNodes, numConnections, name="", date="", description="", weightsRange=None, isMultiGraph=False, isDirected=False, isWeighted=False)
        for i in range(len(graphParams)):
            g = Graph(seed=graphParams[i][0], numNodes=graphParams[i][1], numConnections=graphParams[i][2], name=graphParams[i][3], date=graphParams[i][4], description=graphParams[i][5],
                                    weightsRange=graphParams[i][6], isMultiGraph=graphParams[i][7], isDirected=graphParams[i][8], isWeighted=graphParams[i][9])
            self.Graphs.append(g)

    def display(self):
        for each in self.Graphs:
            each.display()
            print("\n")

    def writeToTxt(self, fileName):
        f = open(fileName, "w")
        f.write(f"Graph Collection Name: {self.name}\nDate: {self.date}\nDescription: {self.description}\n") # write our metadata
        f.close()
        for i in range(len(self.Graphs)):
            f = open(fileName, "a")
            f.write("\n\n")
            f.close()
            self.Graphs[i].writeToTxt(fileName, flag="a")
            # if i != len(self.Graphs)-1: # if it's not the last graph in the collection then output two new lines for formatting
            #     thisFile = open(fileName, "a")
            #     thisFile.write("\n\n")
            #     #thisFile.close()

    def copy(self):
        return copy.deepcopy(self)

    def sort(self):
        self.Graphs.sort(key=lambda graph: graph.name)

    def equals(self, collection2):
        # this function seeks to compare two collection of graphs. All names must be the same, as well as all node names, connections, and weights, but dates and descriptions don't matter
        # first we'll compare their lengths, if the lengths are different, obviously they're two different collections
        if len(self.Graphs) != len(collection2.Graphs): return False
        # else we sort both and then compare each
        self.sort()
        collection2.sort()
        # now iterate through both at once and compare each object
        counter = 1

        return True





