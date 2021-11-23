from classes import Graph
import numpy as np

#g = Graph(file="toyInput.txt")
'''
MultiGraph: T
Directed: T
Weighted: T
A -> B 1 2, D 2
B -> C 3
C -> C 2
D ->
'''

#g = Graph(file="toyInput2.txt")
'''
MultiGraph: F
Directed: F
Weighted: F
A -> B, D
B -> A, C
C -> B, C
D -> A
'''


#g = Graph(seed=1, numNodes=2, numConnections=5, name="MarkyMark", description="testing graph generator", isMultiGraph=True)

#g = Graph(seed=1, numNodes=5, numConnections=20, name="MarkyMark", description="testing graph generator", isMultiGraph=True)

#g = Graph(seed=1, numNodes=5, numConnections=20, name="MarkyMark", description="testing graph generator", isMultiGraph=True, isDirected=True, isWeighted=True, weightsRange=[1,10] )


#generateGraph(self, seed, numNodes, numConnections, name="", date="", description="", weightsRange=None, isMultiGraph=False, isDirected=False, isWeighted=False)

possibleCases = [True, False]
counter = 1
for isMultiGraph in possibleCases:
    for isWeighted in possibleCases:
        for isDirected in possibleCases:
            print(f"\n\nSettings: isMultiGraph={isMultiGraph}, isDirected={isDirected}, isWeighted={isWeighted}")
            g =  Graph(seed=2, numNodes=5, numConnections=7, name="", date="", description="", weightsRange=[1,5], isMultiGraph=isMultiGraph, isDirected=isDirected, isWeighted=isWeighted)
            print("Final:")
            print(g.formattedAdjacencyList())
            print(g.adjacencyMatrix)
            print(f"finished graph {counter}")
            g.evaluateSymmetry()
            g.writeToTxt(f"./testingWriteToTxtFunction/Graph{counter}")
            counter += 1

# isMultiGraph = False
# isDirected = False
# isWeighted = True
#g = Graph(seed=2, numNodes=5, numConnections=7, name="", date="", description="", weightsRange=[1,5], isMultiGraph=isMultiGraph, isDirected=isDirected, isWeighted=isWeighted)
#print(f"\n\nSettings: isMultiGraph={isMultiGraph}, isDirected={isDirected}, isWeighted={isWeighted}")
# print("Final:")
# print(g.formattedAdjacencyList())
# print(g.adjacencyMatrix)
# g.evaluateSymmetry()