# This file intend to classify question type and transfer a question to the query
# Not working yet

import ahocorasick
import json
import relation


class WrdList:
    def __init__(self, wordlist, wordtype):
        self.wordtype = wordtype
        self.wordlist = wordlist


class QuestionPaser:
    def __init__(self):
        # TODO create a list of keyword dictionaries, to be match from a natural language question
        with open('./data/nodeList.json') as f:
            self.nodelist = json.load(f)
        self.wrdsComponent_Number = list(
            v for v in self.nodelist["Component"]['Component_Number'])
        self.wrdsComponent_Name = list(
            v for v in self.nodelist["Component"]['Name'])
        self.wrdComponent = self.wrdsComponent_Name+self.wrdsComponent_Number
        self.wrdListComponent = WrdList(self.wrdComponent, "Component")
        self.wrdAssembly_Name = list(
            v for v in self.nodelist["Assembly"]["Name"])
        self.wrdListAssembly = WrdList(self.wrdAssembly_Name, "Assembly")
        self.wrdSystem_Name = list(
            v for v in self.nodelist["System"]["Name"])
        self.wrdListSystem = WrdList(self.wrdSystem_Name, "System")
        self.wrdDepartment_name = list(
            v for v in self.nodelist["Department"]["Name"])
        self.wrdListDepartment = WrdList(self.wrdDepartment_name, "Department")
        self.wrdProduct_name = list(
            v for v in self.nodelist["Products"]["Name"])
        self.wrdListProduct = WrdList(self.wrdProduct_name, "Product")
        self.wrdStaff_Number = list(
            v for v in self.nodelist["Staff"]["StaffID"])
        self.wrdStaff_Name = list(v for v in self.nodelist["Staff"]["Name"])
        self.wrdStaff = self.wrdStaff_Number+self.wrdStaff_Name
        self.wrdListStaff = WrdList(self.wrdStaff, "Staff")
        self.wrdRole_Name = list(v for v in self.nodelist["Role"]["Name"])
        self.wrdListRole = WrdList(self.wrdRole_Name, "Role")
        self.wrdSupplier_Name = list(
            v for v in self.nodelist["Supplier"]["Name"])
        self.wrdSupplier_Number = list(
            v for v in self.nodelist["Supplier"]["SupplierID"])
        self.wrdSupplier = self.wrdSupplier_Name+self.wrdSupplier_Number
        self.wrdListSupplier = WrdList(self.wrdSupplier, "Supplier")
        self.wrdWorkstation = list(
            v for v in self.nodelist["Workstation"]["WorkstationID"])
        self.wrdListWorkstation = WrdList(self.wrdWorkstation, "Workstation")
        self.targetWordLists = [self.wrdListAssembly, self.wrdListComponent, self.wrdListDepartment, self.wrdListProduct,
                                self.wrdListRole, self.wrdListStaff, self.wrdListSupplier, self.wrdListSystem, self.wrdListWorkstation]
        self.actree = self.build_actree(self.wrdComponent, self.wrdAssembly_Name, self.wrdSystem_Name, self.wrdDepartment_name,
                                        self.wrdProduct_name, self.wrdStaff, self.wrdRole_Name, self.wrdSupplier, self.wrdWorkstation)

    def wrddict(self):  # build a dictionary key as {name:[*wordtype]}
        wd_dict = {}
        for i in self.targetWordLists:
            for j in i.wordlist:
                if j not in wd_dict:
                    wd_dict[j] = [i.wordtype]
                else:
                    wd_dict[j].append(i.wordtype)
        return wd_dict

    def wrdkeys(self):
        return self.nodelist.keys()

    def build_actree(self, *wordlists):
        actree = ahocorasick.Automaton()
        for wordlist in wordlists:
            for i, word in enumerate(wordlist):
                actree.add_word(word, (i, word))
                actree.make_automaton()
        return actree


q = QuestionPaser()
print(relation.StafftoDepartment.label)
