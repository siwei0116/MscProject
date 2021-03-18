import networkx as nx
import matplotlib.pyplot as plt

def printGraph(list_of_triples):
    """ the function takes a triple statement and graw a graph"""
    labels=dict()
    G = nx.DiGraph()
    for triples in list_of_triples:
   
        G.add_node(triples[0])
        G.add_node(triples[2])
        G.add_edge(triples[0],triples[2])
        labels[(triples[0],triples[2])]=triples[1]
        
    pos1 = nx.spring_layout(G)
    plt.figure()
    nx.draw(G, pos1, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='seagreen', alpha=0.9,
            labels={node: node for node in G.nodes()})
    nx.draw_networkx_edge_labels(G,edge_labels=labels,font_color='red',pos=pos1)
    plt.axis('off')
 
    plt.show()

# Test   
# printGraph([(1,2,3),(4,5,6)])
