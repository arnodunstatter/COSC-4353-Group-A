from classes import Graph
import numpy as np

#def __init__(self, seed, numNodes, numConnections, name="", date="", description="", weightsRange=None, isMultiGraph=False, isDirected=False, isWeighted=False):
g = Graph(seed=1, numNodes=5, numConnections=4, name="MarkyMark", description="testing graph generator")

print(g.adjacencyLists)
print("\n")
print(g.adjacencyMatrix)
