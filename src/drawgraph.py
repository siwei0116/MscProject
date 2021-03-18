import networkx as nx
import matplotlib.pyplot as plt

def printGraph(list_of_triples):
    """ the function takes a triple statement and graw a graph"""
    labels=dict()
    for triples in list_of_triples:
        G = nx.DiGraph()
        G.add_node(triples[0])
        G.add_node(triples[2])
        G.add_edge(triples[0],triples[2])
        labels[(triples[0],triples[2])]=triples[1]


    pos = nx.spring_layout(G)
    plt.figure()
    nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='seagreen', alpha=0.9,
            labels={node: node for node in G.nodes()})
    nx.draw_networkx_edge_labels(G,edge_labels=labels,font_color='red',pos=nx.spring_layout(G))
    plt.axis('off')
    print(labels)
    plt.show()
    
printGraph([(1,'a',3)])
