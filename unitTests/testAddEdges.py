from ../classes import *

def testAddEdges():
    '''
    testAddEdge:
    if undirected
      number of weights between source and destination should increase by 1 after addEdge() AND
      number of weights between destination and source should increase by 1 after addEdge()
    else //it's directed
      number of weights between source and destination should increase by 1 after addEdge() AND
      number of weights between destination and source should NOT CHANGE after addEdge()
  '''
    possibleCases = [True, False]
    counter = 1
    for isMultiGraph in possibleCases:
        for isDirected in possibleCases:
            for isWeighted in possibleCases:
                for n in range(2, 21):
                    numNodes = n
                    if isDirected:
                        numConnections = n * (n - 1) - 1 # we subtract 1 because we need space to add an edge when isMultiGraph = False AND isDirected = False
                    else:
                        numConnections = floor(n * (n - 1) / 2) - 1 # we subtract 1 because we need space to add an edge when isMultiGraph = False AND isDirected = False
                    g = Graph(seed=2, numNodes=numNodes, numConnections=numConnections, name=f"Graph{counter}", date="", description="", weightsRange=[1,5], isMultiGraph=isMultiGraph, isDirected=isDirected, isWeighted=isWeighted)
                    counter += 1

                    #select our source and destination pair
                    if g.isMultiGraph:
                        source = "0"
                        destination = "1"
                    else: # we need to select a source/destination pair that doesnt already have an edge
                        breakOuterForLoop = False
                        for row in g.adjacencyLists.keys():
                            for col in g.adjacencyLists.keys():
                                if row != col:
                                    if not isinstance(g.adjacencyMatrix.at[row,col], type(np.array([]))):
                                        source = row
                                        destination = col
                                        breakOuterForLoop = True
                                        break
                            if breakOuterForLoop: break

                    originalNumberOfEdgesBetweenSourceAndDestiation = len(g.adjacencyMatrix.at[source, destination]) if isinstance(g.adjacencyMatrix.at[source,destination], type(np.array([]))) else 0
                    originalNumberOfEdgesBetweenDestinationAndSource = len(g.adjacencyMatrix.at[destination, source]) if isinstance(g.adjacencyMatrix.at[destination,source], type(np.array([]))) else 0

                    g2 = copy.deepcopy(g)
                    g2.addEdges(source, [destination,1])

                    numberOfEdgesBetweenSourceAndDestiationAfterAddEdges = len(g2.adjacencyMatrix.at[source, destination]) if isinstance(g2.adjacencyMatrix.at[source,destination], type(np.array([]))) else 0
                    numberOfEdgesBetweenDestinationAndSourceAfterAddEdges = len(g2.adjacencyMatrix.at[destination, source]) if isinstance(g2.adjacencyMatrix.at[destination,source], type(np.array([]))) else 0

                    if g.isDirected:
                        if numberOfEdgesBetweenSourceAndDestiationAfterAddEdges != originalNumberOfEdgesBetweenSourceAndDestiation+1 or numberOfEdgesBetweenDestinationAndSourceAfterAddEdges != originalNumberOfEdgesBetweenDestinationAndSource:
                            print("shiiii")
                            print("False")
                            return
                    else: #g is undirected
                        if numberOfEdgesBetweenSourceAndDestiationAfterAddEdges != originalNumberOfEdgesBetweenSourceAndDestiation+1 or numberOfEdgesBetweenDestinationAndSourceAfterAddEdges != originalNumberOfEdgesBetweenDestinationAndSource+1:
                            print()
                            print(f"Settings: isMultigraph={g.isMultiGraph}, isDirected={g.isDirected}, isWeighted={g.isWeighted}")
                            print("original:")
                            g.display()
                            print("\nnew:")
                            g2.display()
                            print("False")
                            return
    print("True")
