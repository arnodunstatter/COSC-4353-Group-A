from classes import *

def testGraphObject():
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
                    g = Graph(seed=2, numNodes=numNodes, numConnections=numConnections, name=f"Graph{counter}", date="", description="", weightsRange=[1,5], isMultiGraph=isMultiGraph, isDirected=isDirected, isWeighted=isWeighted)

                    # test that for every key in the adjacencyLists we have an index and a column in the adjacencyMatrix, otherwise print "False" and return
                    adjListNodes = sorted(list(g.adjacencyLists.keys()))
                    adjMatrSources = sorted(g.adjacencyMatrix.index)
                    adjMatrDestinations = sorted(g.adjacencyMatrix.columns)
                    if len(adjListNodes) != len(adjMatrSources) or len(adjListNodes) != len(adjMatrDestinations) or len(adjMatrSources) != len(adjMatrDestinations):
                        print("False")
                        return
                    for i,j,k in zip(adjListNodes,adjMatrSources,adjMatrDestinations):
                        if i != j or i != k or j != k:
                            print("False")
                            return

                    # test that all weights are the same for every source->destination pair
                    for source in adjListNodes:
                        destinations = g.adjacencyLists.get(source)
                        for destinationTuple in destinations:
                            destination = destinationTuple[0]
                            adjListWeights = sorted(destinationTuple[1:])
                            adjMatrWeights = sorted(g.adjacencyMatrix.at[source,destination])
                            if adjListWeights != adjMatrWeights:
                                print("False")
                                return

                    #checks for unweighted and non-multigraph issues
                    for row in adjMatrSources:
                        for col in adjMatrDestinations:
                            if not g.isWeighted and isinstance(g.adjacencyMatrix.at[row,col], type(np.array([]))):
                                for w in g.adjacencyMatrix.at[row,col]:
                                    if w != 1: #if it's unweighted, all weights should be 1
                                        print("w!=1")
                                        print("False")
                                        return
                            if not g.isMultiGraph: #if it's not a multigraph
                                # then the leading diagonal should be all NaNs, otherwise print "False"
                                if row == col:
                                    if not np.isnan(g.adjacencyMatrix.at[row,col]):
                                        print(f"value at {row},{col} when it should be NaN")
                                        print("False")
                                        return
                                # and the number of weights between each source and destination should be 1
                                if isinstance(g.adjacencyMatrix.at[row,col], type(np.array([]))) and len(g.adjacencyMatrix.at[row,col]) > 1:
                                    print(f"There should only be 1 value at {row},{col} but instead there are {g.adjacencyMatrix.at[row,col]}")
                                    print("False")
                                    return

                    counter += 1


    print("True")

