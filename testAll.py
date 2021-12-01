from classes import *
def testAll():
    #All Features are implicitly tested together by this last test.
    #Generate Graphs, add to a CollectionOfGraphs, write the collection to a file, read it in from the file, compare read in collection to original collection, if they're equal, print 'True' otherwise print 'False':
    # Read a file representing multiple graphs
        #in order to test this we first we create a collection of graphs and output it to a txt file
        #then we read it in
        #then we compare the original collection to the read-in collection to make sure they're the same

        #1. Create a collection of graphs
            # first we create a list of our parameters
    graphParams = [] # a list of lists with each inner list having the order:
    # [seed, numNodes, numConnections, name, date, description, weightsRange, isMultiGraph, isDirected, isWeighted]
    possibleCases = [True, False]
    counter = 1
    for isMultiGraph in possibleCases:
        for isDirected in possibleCases:
            for isWeighted in possibleCases:
                for n in range(1,21): #testing graphs with between 1 and 20 nodes
                    numNodes = n
                    if isDirected:
                        numConnections = n*(n-1)
                    else: #undirected
                        numConnections = floor(n*(n-1)/2)
                    graphParams.append([1,numNodes,numConnections,f"graph{counter}","",f"test graph {counter}", [1,9], isMultiGraph, isDirected, isWeighted])
                    counter += 1
            #now we produce our collection
    originalTestCollection = CollectionOfGraphs("testCollection1","","A test collection", graphParams)
            #now we output the collection to a file
    originalTestCollection.writeToTxt("testCollection1.txt")
            #now we read the collection into a new object
    readTestCollection = CollectionOfGraphs("testCollection1.txt")
            #now we compare the two objects and print to console


    print(originalTestCollection.equals(readTestCollection))


