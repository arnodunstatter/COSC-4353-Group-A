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

for isDirected in [True, False]:
    for isWeighted in [True, False]:
        for isMultiGraph in [True, False]:
            print(f"Settings: isMultiGraph={isMultiGraph}, isDirected={isWeighted}, isWeighted={isWeighted}")
            g = Graph(seed=1, numNodes=5, numConnections=5, name="", date="", description="", weightsRange=[1,10], isMultiGraph=isMultiGraph, isDirected=isWeighted, isWeighted=isWeighted)
            print(g.adjacencyLists)
            print(g.adjacencyMatrix)

            expected = "symmetric" if not g.isDirected else "asymmetric"
            if g.adjacencyMatrix.equals(g.adjacencyMatrix.transpose()):
                actual = "symmetric"
            else:
                actual = "asymmetric"
            print(f"Expected: {expected}\nActual: {actual}")
            print("\n")