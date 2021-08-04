# This file intend to classify question type and transfer a question to the query
# Not working yet

import json
import relation
import entity
import nltk
import string
from nltk.util import everygrams


class WrdList:
    def __init__(self, wordlist, wordtype, wordproperty):
        self.wordtype = wordtype
        self.wordlist = wordlist
        self.wordproperty = wordproperty


class QuestionPaser:
    def __init__(self, txt):
        self.txt = txt.lower()
        # TODO create a list of keyword dictionaries, to be match from a natural language question
        with open('./data/nodeList.json') as f:
            self.nodelist = json.load(f)
        self.wrdsComponent_Number = list(
            v for v in self.nodelist["Component"]['Component_Number'])
        self.wrdListComponent_Number = WrdList(
            self.wrdsComponent_Number, "Component", "Component_Number")
        self.wrdsComponent_Name = list(
            v for v in self.nodelist["Component"]['Name'])
        self.wrdListComponent_Name = WrdList(
            self.wrdsComponent_Name, "Component", "Name")
        self.wrdAssembly_Name = list(
            v for v in self.nodelist["Assembly"]["Name"])
        self.wrdListAssembly_Name = WrdList(
            self.wrdAssembly_Name, "Assembly", "Name")
        self.wrdSystem_Name = list(
            v for v in self.nodelist["System"]["Name"])
        self.wrdListSystem_Name = WrdList(
            self.wrdSystem_Name, "System", "Name")
        self.wrdDepartment_Name = list(
            v for v in self.nodelist["Department"]["Name"])
        self.wrdListDepartment_Name = WrdList(
            self.wrdDepartment_Name, "Department", "Name")
        self.wrdProduct_Name = list(
            v for v in self.nodelist["Products"]["Name"])
        self.wrdListProduct_Name = WrdList(
            self.wrdProduct_Name, "Product", "Name")
        self.wrdStaff_ID = list(
            v for v in self.nodelist["Staff"]["StaffID"])
        self.wrdListStaff_ID = WrdList(
            self.wrdStaff_ID, "Staff", "StaffID")
        self.wrdStaff_Name = list(v for v in self.nodelist["Staff"]["Name"])
        self.wrdListStaff_Name = WrdList(self.wrdStaff_Name, "Staff", "Name")
        self.wrdRole_Name = list(v for v in self.nodelist["Role"]["Name"])
        self.wrdListRole_Name = WrdList(self.wrdRole_Name, "Role", "Name")
        self.wrdSupplier_Name = list(
            v for v in self.nodelist["Supplier"]["Name"])
        self.wrdListSupplier_Name = WrdList(
            self.wrdSupplier_Name, "Supplier", "Name")
        self.wrdSupplier_ID = list(
            v for v in self.nodelist["Supplier"]["SupplierID"])
        self.wrdListSupplier_ID = WrdList(
            self.wrdSupplier_ID, "Supplier", "SupplierID")
        self.wrdWorkstation_ID = list(
            v for v in self.nodelist["Workstation"]["WorkstationID"])
        self.wrdListWorkstation_ID = WrdList(
            self.wrdWorkstation_ID, "Workstation", "WorkstationID")
        self.targetWordLists = [self.wrdListAssembly_Name, self.wrdListComponent_Name, self.wrdListComponent_Number, self.wrdListDepartment_Name, self.wrdListProduct_Name,
                                self.wrdListRole_Name, self.wrdListStaff_ID, self.wrdListStaff_Name, self.wrdListSupplier_ID, self.wrdListSupplier_Name, self.wrdListSystem_Name, self.wrdListWorkstation_ID]

    def wrddict(self):  # build a dictionary key as {name:[*wordtype]}
        wd_dict = {}
        for i in self.targetWordLists:
            for j in i.wordlist:
                if j.lower() not in wd_dict:
                    wd_dict[j.lower()] = [(i.wordtype, i.wordproperty)]
                else:
                    wd_dict[j.lower()].append((i.wordtype, i.wordproperty))
        return wd_dict

    def wrdkeys(self):
        return self.nodelist.keys()

    def checkwords(self):
        result = []
        for word in self.nGram(3):
            a = self.wrddict().get(word, False)
            if a != False:
                result.append(a)
        return result

    def nGram(self, n):  # To deal with phrases,split all words into the list with the maximum of n words
        a = list(everygrams(self.parseQuestion(), max_len=3))
        b = [" ".join(word) for word in a]
        return b

    def parseQuestion(self):  # Split the question sentense into words
        lem = nltk.WordNetLemmatizer()
        tokenized_text = nltk.word_tokenize(self.txt.lower())
        parsed = [
            lem.lemmatize(word) for word in tokenized_text if word[0] not in string.punctuation]
        return parsed

    def toSqls(self):
        sqls = []
        relations = []
        entities = []
        nodeTypes = []
        parsedQuestion = self.nGram(3)
        wrdDict = self.wrddict()
        relationdict = relation.Relation.getRelationDict()
        relationEqDict = relation.Relation.getEquivalenceDict()
        relationInvDict = relation.Relation.getInverseDict()
        entityDict = entity.myNode.getNodeDict()

        for word in parsedQuestion:
            if word in wrdDict:
                for v in wrdDict[word]:
                    entities.append((word, v))
                nodeTypes.append(wrdDict[word][0][0])
            if word in relationEqDict:
                for v in relationEqDict[word]:
                    relations.append(v)
            if word in relationInvDict:
                for v in relationInvDict[word]:
                    relations.append(v)
            if word in entityDict:
                nodeTypes.append(entityDict[word])

        for r in relations:
            snode = relationdict[r].startnodetype
            enode = relationdict[r].endnodetype
            for i in entities:
                if i[1][0] == snode:
                    sqls.append(
                        f"MATCH (n:{snode})-[r:{r}]->(m:) where n.{i[1][1]} = '{i[0]}' RETURN r")
                if i[1][0] == enode:
                    sqls.append(
                        f"MATCH (n)-[r:{r}]->(m:{enode}) where n.{i[1][1]} = '{i[0]}' RETURN r")

        if not relations:
            for i in entities:
                sqls.append(
                    f"MATCH (n:{[1][0]}) where n.{i[1][1]} = '{i[0]}' RETURN n")

        return sqls, entities, relations, nodeTypes


if __name__ == "__main__":
    q = QuestionPaser("Who designed C0010009")
    print(q.toSqls())

# sample question:
# who is responsible for design engineer
# who designed C0010009
# who works in the department of powertrain
