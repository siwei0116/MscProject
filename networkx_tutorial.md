# Networkx

## node

### add one node
### add nodes with list parameter
### add nodes with attributes
### add a node from another graph
### Use another graph as a node
* Example
``` python
import networkx as nx

G=nx.Graph() 

G.add_node(1) # add one node at a time

G.add_node_from([2,3]) # add_nodes_from to add node from iterable container

G.add_nodes_from([  
     # add nodes along with node attribute (node, node_attribute_dict)                   
    (4, {"color": "red"}),
    (5, {"color": "green"}),
])

# Nodes from one graph can be incorportated into another
H=nx.path_graph(10)
G.add_nodes_from(H)

# Use the graph H as a node in G
G.add_node(H)
```

