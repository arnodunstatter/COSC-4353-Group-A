from classes import Graph
from classes import CollectionOfGraphs

graphParams = [] # a list of lists with each inner list having the order:
# [seed, numNodes, numConnections, name, date, description, weightsRange, isMultiGraph, isDirected, isWeighted]
possibleCases = [True, False]
counter = 1
for isMultiGraph in possibleCases:
    for isDirected in possibleCases:
        for isWeighted in possibleCases:
            graphParams.append([1,5,10,f"graph{counter}","",f"test graph {counter}", [1,9], isMultiGraph, isDirected, isWeighted])
            counter += 1

generatedTestCollection = CollectionOfGraphs("testCollection1","","Our first test collection", graphParams)

generatedTestCollection.writeToTxt("./testingWriteToTxtFunction/testCollection1.txt")

readTestCollection = CollectionOfGraphs("./testingWriteToTxtFunction/testCollection1.txt")
readTestCollection.display()
