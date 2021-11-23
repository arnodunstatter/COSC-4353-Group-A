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

#possibleCases = [True, False]

#for isMultiGraph in possibleCases:
#    for isWeighted in possibleCases:
#        for isDirected in possibleCases:

# current issue: Do not call for all 9 possible combinations. Will run into recursion issue.
# Works with at least 4 cases at a time. For now do not use the nested for-loop.
isMultiGraph = False
isDirected = False
isWeighted = True

print(f"Settings: isMultiGraph={isMultiGraph}, isDirected={isDirected}, isWeighted={isWeighted}")
g = Graph(seed=2, numNodes=5, numConnections=7, name="", date="", description="", weightsRange=[1,5], isMultiGraph=isMultiGraph, isDirected=isWeighted, isWeighted=isWeighted)
print("\n\nFinal:")
print(g.adjacencyLists)
print(g.adjacencyMatrix)

expected = "symmetric" if not g.isDirected else "asymmetric"
if g.adjacencyMatrix.equals(g.adjacencyMatrix.transpose()):
    actual = "symmetric"
else:
    actual = "asymmetric"
print(f"Expected: {expected}\nActual: {actual}")
print("\n")
