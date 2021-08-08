from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher, Schema
import entity


class Embedding_Prepare:
    def __init__(self):
        # Connect to the Neo4j data base, the default passwrd for the local host is "123456"
        self.g = Graph("http://localhost:7474", auth=("neo4j", "123456"))
        # 'nodes' is a list of Node class defined in the entity.py

    def relation2id_tofile(self):
        graph_schema = Schema(self.g)
        with open('./data/relation2id.txt', "w") as fhand:
            print(len(graph_schema.relationship_types), file=fhand)
            i = 0
            for rel in graph_schema.relationship_types:
                print(rel, "\t", str(i), file=fhand)
                i = i+1

    @classmethod
    def relationDic(self):
        relation_dic = {}
        with open('./data/relation2id.txt', 'r') as fhand:
            next(fhand)
            for line in fhand:
                rel = [x for x in line.split('\t')]
                rel_name = rel[0].strip()
                rel_id = rel[1].strip()
                relation_dic[rel_name] = rel_id
        return relation_dic

    def entity2id_tofile(self):
        keydic = entity.Entities.labeldic()
        nmatcher = NodeMatcher(self.g)
        with open('./data/entity2id.txt', 'w+') as fhand:
            print(len(nmatcher.match()), file=fhand)
            for n in nmatcher.match().order_by("_.identity"):
                nodetype = str(n.labels).lstrip(":")
                nodekey = keydic[nodetype]
                print(
                    nodetype+'/'+str(n[nodekey]).replace(" ", "_"), '\t', n.identity, file=fhand)

    def train2id_tofile(self):
        rmatcher = RelationshipMatcher(self.g)
        relationdic = Embedding_Prepare.relationDic()
        with open('./data/train2id.txt', 'w+')as fhand:
            print(len(rmatcher.match()), file=fhand)
            for r in rmatcher.match():
                print(r.start_node.identity, r.end_node.identity,
                      relationdic[type(r).__name__], sep='\t', file=fhand)


if __name__ == '__main__':
    ep = Embedding_Prepare()
    ep.relation2id_tofile()
    ep.entity2id_tofile()
    ep.train2id_tofile()
