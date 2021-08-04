import py2neo
import numpy as np
import pandas as pd
from py2neo import Graph, Node, Relationship, NodeMatcher


def main1():

    g = Graph("http://localhost:7474", auth=("neo4j", "123456"))
    matcher = NodeMatcher(g)
    node1 = matcher.match(name="Zhu").first()
    print(g.nodes.match("Person", name="Zhu").first())


dates = pd.date_range("20130101", periods=6)
df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
print(df.dtypes)
