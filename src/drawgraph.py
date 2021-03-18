import networkx as nx
import matplotlib.pyplot as plt

def printGraph(triples):
    """ the function takes a triple statement and graw a graph"""
    G = nx.Graph()
    G.add_node(triples[0])
    G.add_node(triples[1])
    G.add_node(triples[2])
    G.add_edge(triples[0],triples[1])
    G.add_edge(triples[1],triples[2])

    pos = nx.spring_layout(G)
    plt.figure()
    nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='seagreen', alpha=0.9,
            labels={node: node for node in G.nodes()})
    plt.axis('off')
    plt.show()

printGraph((1,2,3))