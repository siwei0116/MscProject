import py2neo
from py2neo import Graph, Node, Relationship, NodeMatcher

g = Graph("http://localhost:7474", auth=("neo4j", "123456"))
matcher = NodeMatcher(g)
node1 = matcher.match(name="Zhu").first()
print(g.nodes.match("Person", name="Zhu").first())
