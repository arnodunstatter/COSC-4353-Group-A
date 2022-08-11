from classes import Graph
possibleCases = [True, False]
counter = 1
for isMultiGraph in possibleCases:
    for isWeighted in possibleCases:
        for isDirected in possibleCases:
            print(f"\n\nSettings: isMultiGraph={isMultiGraph}, isDirected={isDirected}, isWeighted={isWeighted}")
            g = Graph(seed=2, numNodes=5, numConnections=7, name="", date="", description="", weightsRange=[1,5], isMultiGraph=isMultiGraph, isDirected=isDirected, isWeighted=isWeighted)
            print("Final:")
            print(g.formattedAdjacencyList())
            print(g.adjacencyMatrix)
            print(f"finished graph {counter}")
            g.evaluateSymmetry()
            g.writeToTxt(f"./testingWriteToTxtFunction/Graph{counter}")
            counter += 1
            # visually inspect that each graph's adjacencyLists and adjacencyMatrix corroborate one another (rows are sources, columns are destinations for directed graphs)