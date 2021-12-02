from classes import *

def testDeleteEdges():
    possibleCases = [True, False]
    count = 1
    for isMultiGraph in possibleCases:
        for isWeighted in possibleCases:
            for isDirected in possibleCases:
                for n in range(2,21):
                    numNodes = n
                    if isDirected:
                        numConnections = n*(n-1)
                    else:
                        numConnections = floor(n*(n-1)/2)
                    g = Graph(seed=2, numNodes=numNodes, numConnections=numConnections, name="", date="", description="", weightsRange=[1,5], isMultiGraph=isMultiGraph, isDirected=isDirected, isWeighted=isWeighted)
                    count += 1

                    #select our source and destination pair - we need at least 1 edge between them
                    breakOuterForloop = False
                    for row in g.adjacencyLists.keys():
                        for col in g.adjacencyLists.keys():
                            if row != col:
                                if isinstance(g.adjacencyMatrix.at[row,col], type(np.array([]))):
                                    source, destination = row, col
                                    breakOuterForloop = True
                                    break
                        if breakOuterForloop:
                            break

                    #get our original number of edges b/w source and destiantion, and their weights
                    originalNumberOfEdgesBetweenSourceAndDestination = len(g.adjacencyMatrix.at[source,destination])
                    originalWeightsBetweenSourceAndDestination = sorted(g.adjacencyMatrix.at[source,destination])

                    #select an edge to be deleted
                    deleteThisEdge = originalWeightsBetweenSourceAndDestination[0]

                    #now delete the edge
                    g.deleteEdges(source, destination, weightsToRemove=[deleteThisEdge])

                    #get our new number of edges b/w source and destination, and their weights
                    newNumberOfEdgesBetweenSourceAndDestination = len(g.adjacencyMatrix.at[source,destination]) if isinstance(g.adjacencyMatrix.at[source,destination], type(np.array([]))) else 0
                    newWeightsBetweenSourceAndDestination = sorted(g.adjacencyMatrix.at[source,destination]) if isinstance(g.adjacencyMatrix.at[source,destination], type(np.array([]))) else []

                    #check that everything is as it should be (newNumEdges = originalNumEdges-1 and that the edge removed was the first)
                    if originalNumberOfEdgesBetweenSourceAndDestination-1 == newNumberOfEdgesBetweenSourceAndDestination:
                        if originalWeightsBetweenSourceAndDestination[1:] != newWeightsBetweenSourceAndDestination:
                            print("False")
                            return
                    else:
                        print("False")
                        return
    print("True")

testDeleteEdges()