from classes import Graph
from classes import CollectionOfGraphs

g = Graph(name="testGraph", description="just another test graph", seed=1, numNodes=5, numConnections=20, weightsRange=[1,9], isMultiGraph=True, isDirected=False, isWeighted=True)
g.display()
# g.deleteEdges(source='1',destination='3',weightsToRemove=[6,8])
# g.display()

g.deleteNode("1")
g.display()
