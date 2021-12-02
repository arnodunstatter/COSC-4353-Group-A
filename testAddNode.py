from classes import *

def testAddNode():
    possibleCases = [True, False]
    count = 1
    for isMultiGraph in possibleCases:
        for isDirected in possibleCases:
            for isWeighted in possibleCases:
                for n in range(2,21):
                    numNodes = n
                    if isDirected:
                        numConnections = n*(n-1)
                    else:
                        numConnections = floor(n*(n-1)/2)
                    g = Graph(seed=2, numNodes=numNodes, numConnections=numConnections, name="", date="", description="", weightsRange=[1,5], isMultiGraph=isMultiGraph, isDirected=isDirected, isWeighted=isWeighted)
                    count += 1

                    originalNumberOfNodes = len(g.adjacencyLists.keys())
                    g.addNode(str(originalNumberOfNodes))
                    newNumberOfNodes = len(g.adjacencyLists.keys())
                    if newNumberOfNodes != originalNumberOfNodes+1:
                        print("False")
                        return
    print("True")
