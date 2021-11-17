from numpy.core.numeric import NaN
import pandas as pd
import numpy as np

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
    adjacencyLists = {} # a dictionary - each key's value is a set of lists - first element in each list is the destination node name, second element is a numpy array of weights
    adjacencyMatrix = pd.DataFrame()

    # Methods -----------------------------------------
    def __init__(self, file): #this will read files directly
        f = open(file)
        self.name = f.readline()[len("GraphName: "):].split("\n")[0]
        self.date = f.readline()[len("Date: "):].split("\n")[0]
        self.description = f.readline()[len("Description: "):].split("\n")[0]
        self.isMultiGraph = True if f.readline()[len("MultiGraph: "):] == "T\n" else False
        self.isDirected = True if f.readline()[len("Directed: "):] == "T\n" else False
        self.isWeighted = True if f.readline()[len("Weighted: "):] == "T\n" else False
        #handle adjacencyList
        for eachRow in f: #example of eachRow "A -> B 1 2, D 2\n"
            if("\n"==eachRow[len(eachRow)-1:]): #if the line ends in "\n", then remove it - example result: "A -> B 1 2, D 2"
                row = eachRow[:len(eachRow)-1]
            else: row = eachRow #otherwise do just get the line as is
            row = row.split("->") #element 0 is source node, element 2 is destination nodes and associated weights - example result: ["A ", " B 1 2, D 2"]
            row[0]=row[0].split(" ") #isolate source node's name from the space - example result: ["A",""]
            row[1]=row[1].split(",") #split destination nodes - example result: [" B 1 2"," D 2"]
            for i in range(len(row[1])): #split destination nodes up from their weights - example of result:[["","B","1","2"],["","D","2"]]]
                row[1][i] = row[1][i].split(" ")
            #row = [['A', ''], [['', 'B', '1', '2'], ['', 'D', '2']]]
            sourceNode = row[0][0]
            self.addNode(sourceNode) #adds sourceNode to adjacencyList and adjacencyMatrix
            destinationNodes = row[1]
            for dest in destinationNodes: #removes the empty string so we are left with just node names and weights
                dest = dest[1:]  
                #destinationNodes = [['B', '1', '2'], ['D', '2']]

    def addNodeToAdjacencyMatrix(self, df, node):
        df.insert(loc=len(df.columns), column=node, value= NaN)
        newRow = pd.Series(name=node, dtype='object')
        return df.append(newRow)

    def addNode(self, node):
        if(None == self.adjacencyLists.get(node)):
            self.adjacencyLists.update({node:{} })
            self.adjacencyMatrix = self.addNodeToAdjacencyMatrix(self.adjacencyMatrix, node)
    
    def addEdges(self, source, destArray): #doesn't matter if it's directed or not, does matter if it's weighted
        destination = destArray[0]
        if(self.isWeighted):
            weights = destArray[1:]
        self.addNode(source) #if the node is already in adjacencyLists then this will do nothing. We have this line for when this function is used later on

        #do adjacencyList first
        #first check if destination is in source's set
        if destination in self.adjacencyLists.get(source): #if the destination is already in 




class GraphCollection:
    def __init__(self, file):
        f = open(file)