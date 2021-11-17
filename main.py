from classes import Graph

g = Graph("t1.txt")
print(g.name)
print(g.date)
print(g.description)
print(g.isMultiGraph)
print(g.isDirected)
print(g.isWeighted)
print(g.adjacencyLists)
print(g.adjacencyMatrix)