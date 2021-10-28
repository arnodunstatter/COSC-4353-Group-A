CSV: a file containing Comma Separated Values - this will be the file format of our input

Graph: 
    Mathematical definition: A graph G = (V,E) consists of V, a non-empty set of vertices (or nodes) and E, a set of edges. Each edge has either one or two vertices associated with it, called its endpoints. An edge is said to connect its endpoints.
    As a Class: this will be the objects which represent each individual graph passed in in the CSV. This object will contain meta-data about the graph as well as pandas dataframes which represent the graph's features. Additionally each graph object will have functions which can perform low level transformations

Node/Vertex: a point of within each graph.

Edge: a connection between two nodes (may or may not be between a node and a different node, or between a node and itself)

CollectionOfGraphs: A class which will contain metadata about the CSV file which represents the collection of graphs passed in to the program. Each CollectionOfGraphs object will aslo contain a data structure that contains the Graph objects that were represented in the CSV