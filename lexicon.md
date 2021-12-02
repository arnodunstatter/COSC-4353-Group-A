txt: a file containing Comma Separated Values - this will be the file format of our input

Graph: 
    Mathematical definition: A graph G = (V,E) consists of V, a non-empty set of vertices (or nodes) and E, a set of edges. Each edge has either one or two vertices associated with it, called its endpoints. An edge is said to connect its endpoints.
    As a Class: this will be the objects which represent each individual graph passed in as a txt string. This object will contain meta-data about the graph as well as a pandas dataframe and a dictionary which represent the graph's features as an adjacency matrix and an adjacency list, respectively.

Node/Vertex: a point at which edges can meet within each graph.

Edge: a connection between two nodes (may or may not be between a node and a different node, or between a node and itself)

CollectionOfGraphs: A class which will contain metadata about the collection of graphs passed in to the program, as well as a list of Graph objects corresponding to each graph in the collection.