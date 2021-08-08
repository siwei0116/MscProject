# A file which defines a knowledge graph

from py2neo import Graph, Node, NodeMatcher
import pandas as pd
import entity as et
import relation as rel


class BuildGraph:
    # a BuldGraph class takes a list of nodes and edges
    def __init__(self, nodes, edges):
        # Connect to the Neo4j data base, the default passwrd for the local host is "123456"
        self.g = Graph("http://localhost:7474", auth=("neo4j", "123456"))
        # 'nodes' is a list of Node class defined in the entity.py
        self.nodes = nodes
        # 'edges' is a list of Relation class defined in relation.py
        self.edges = edges

    def createNodes(self, *nodes):
        # A funciotn to create nodes in the Neo4j graph database from the list of nodes
        for node in nodes:
            # this g.create function is from py2neo API to create one node in the Neo4j
            self.g.create(node)

    def deleteAll(self):
        # delete all nodes and edges in the Neo4j Graph database
        self.g.delete_all()

    def createRelations(self, *relations):
        '''create a relationship on the neo4j graph'''
        labeldict = et.Entities.labeldic()
        for r in relations:
            if r.bidirection == False:
                query = f"match(p:{r.startnodeType}) " +\
                    f"match (q:{r.endnodeType}) " +\
                    f"where p.{labeldict[r.startnodetype]} = '{r.startnodeID}' and q.{labeldict[r.endnodetype]} = '{r.endnodeID}' " +\
                    f"merge(p)-[r:{r.relationType}] -> (q) "
            else:
                query = f"match(p: {r.startnodeType}) " +\
                    f"match(q: {r.endnodeType}) " +\
                    f"where p.{labeldict[r.startnodetype]} = '{r.startnodeID}' and q.{labeldict[r.endnodetype]} = '{r.endnodeID}' " +\
                    f"merge(p)-[r:{r.relationType}]->(q)"
            for k, v in r.property.items():
                addQuery = f"set r.{k}='{v}'\n "
                query = query + " " + addQuery
            self.g.run(query)
            print(query)

    def initialize(self):
        '''initialize the neo4j knowledge graph using the data(nodes and edges) assigned to the graph atrributes '''
        # clear the graph
        self.deleteAll()
        # create all nodes in the Neo4j database
        self.createNodes(*self.nodes.allnodes())
        # create edges in the Neo4j database TODO (to be refactored as the first two arguments are not needed)
        self.createRelations(*self.edges.allRelations())


if __name__ == "__main__":
    datafile = pd.ExcelFile("./data/Data.xlsx")
    # create a Entities object which stores different kinds of nodes (empty)
    n = et.Entities()
    # create a Relations object which stores different kinds of edges(empty)
    e = rel.Relations()
    # extract all node information from the excel file
    n.extractAllNodes(datafile)
    # extract all relation information from the excel file
    e.extractAllRelation(datafile)
    # create a BuildGraph object
    g = BuildGraph(n, e)
    g.initialize()
    print("finished")
