# This file contains a Relation Class and its Child class (for specific relations in the graph)

from py2neo import Node
import pandas as pd
import part_connections


class Relation:
    # Define a relation class, which contains start node, start node type, endnode, endnode type, type of relation, and its property and direction
    def __init__(self, startnodetype, endnodetype, startnodeID, endnodeID, relationtype, bidirection=False, **karg):
        self.startnodeID = startnodeID
        self.endnodeID = endnodeID
        self.property = karg
        self.relationType = relationtype
        self.startnodeType = startnodetype
        self.endnodeType = endnodetype
        self.bidirection = bidirection

    @classmethod
    def getsubClasses(cls):  # get all subclasses of a class
        result = []
        for subclass in cls.__subclasses__():
            result.append(subclass)
        return result

    @classmethod
    def getRelationLabel(cls):  # get all labels of the relations
        result = [a.label for a in cls.getsubClasses()]
        return result

    @classmethod
    def getRelationDict(cls):  # get the {label:class} dictionary of a relation
        dic = {}
        for a in cls.getsubClasses():
            dic[a.label] = a
        return dic

    @classmethod
    # get the equivalence(synonym) dictionary for relations
    def getEquivalenceDict(cls):
        dic = {}
        for a in cls.getsubClasses():
            for b in a.equivalence:
                if b in dic:
                    dic[b].append(a.label)
                else:
                    dic[b] = [a.label]
        return dic

    @classmethod
    def getInverseDict(cls):  # get the inverse(antonym) dictionary for relations
        dic = {}
        for a in cls.getsubClasses():
            for b in a.inverse:
                if b in dic:
                    dic[b].append(a.label)
                else:
                    dic[b] = [a.label]
        return dic

    def __str__(self):
        if self.bidirection == False:
            return(f"Relation(({self.startnodeType}:{self.startnodeID})-({self.relationType}:{self.property})->({self.endnodeType}:{self.endnodeID})")
        else:
            return(f"Relation(({self.startnodeType}:{self.startnodeID})-({self.relationType}:{self.property})-({self.endnodeType}:{self.endnodeID})")

    def __repr__(self):
        if self.bidirection == False:
            return(f"Relation(({self.startnodeType}:{self.startnodeID})-({self.relationType}:{self.property})->({self.endnodeType}:{self.endnodeID})")
        else:
            return(f"Relation(({self.startnodeType}:{self.startnodeID})-({self.relationType}:{self.property})-({self.endnodeType}:{self.endnodeID})")


class fromStafftoDepartment(Relation):
    label = "works_in"
    startnodetype = "Staff"
    endnodetype = "Department"
    inverse = []
    equivalence = ['the personnel of', 'belong to', 'work for', 'work in']

    def __init__(self, staffID, department):
        super().__init__(self.startnodetype, self.endnodetype, staffID,
                         department, self.label)


class fromStafftoRole(Relation):
    label = "works_as"
    startnodetype = "Staff"
    endnodetype = "Role"
    inverse = ['have']
    equivalence = ['is responsible for', 'work as']

    def __init__(self, staffID, role):
        super().__init__(self.startnodetype, self.endnodetype, staffID,
                         role, self.label)


class fromAssemblytoComponent(Relation):
    label = "consists_of"
    startnodetype = "Assembly"
    endnodetype = "Component"
    inverse = ['composes']
    equivalence = ['consist of', 'compose of']

    def __init__(self, assembly, component_number):
        super().__init__(self.startnodetype, self.endnodetype, assembly,
                         component_number, self.label)


class fromAssemblytoSystem(Relation):
    label = "assemled_to"
    startnodetype = "Assembly"
    endnodetype = "System"
    inverse = ['assemble by', 'consist of', 'compose of', 'compose']
    equivalence = []

    def __init__(self, assembly, system):
        super().__init__(self.startnodetype, self.endnodetype, assembly,
                         system, self.label)


class fromSystemtoModel(Relation):
    label = "system_of"
    startnodetype = "System"
    endnodetype = "Product"
    inverse = ['assemble by', 'consist of', 'compose of', 'compose']
    equivalence = []

    def __init__(self, system, product):
        super().__init__(self.startnodetype, self.endnodetype, system, product, self.label)


class fromComponenttoStaff(Relation):
    label = "designed_by"
    startnodetype = "Component"
    endnodetype = "Staff"
    inverse = ['design', 'designed']
    equivalence = []

    def __init__(self, component, staff):
        super().__init__(self.startnodetype, self.endnodetype, component, staff, self.label)


class fromComponenttoSupplier(Relation):
    label = "supplied_by"
    startnodetype = "Component"
    endnodetype = "Supplier"
    inverse = ['supply']
    equivalence = ['purchase from', "supply by"]

    def __init__(self, component, supplier):
        super().__init__(self.startnodetype, self.endnodetype, component, supplier, self.label)


class fromComponenttoWorkstation(Relation):
    label = "Assemblied_At"
    startnodetype = "Component"
    endnodetype = "Workstation"
    inverse = ["assembly"]
    equivalence = ['assembly location of', 'assembly at']

    def __init__(self, component, workstation):
        super().__init__(self.startnodetype, self.endnodetype,
                         component, workstation, self.label)


class fromComponenttoComponent(Relation):
    label = "Connected_with"
    startnodetype = "Component"
    endnodetype = "Component"
    equivalence = ['linked_with']

    def __init__(self, component1, component2, connectionType):
        self.connectionType = connectionType
        super().__init__(self.startnodetype, self.endnodetype,
                         component1, component2, self.label, bidirection=True, connection_type=connectionType)


class Relations:
    rel_stafftoDepartment = []
    rel_stafftoRole = []
    rel_assemblytoComponent = []
    rel_assemblytoSystem = []
    rel_systemtoModel = []
    rel_componentConnectedto = []
    rel_componentDesignedby = []
    rel_componentSuppliedby = []
    rel_componentAssembliedat = []

    def addStafftoDepartment(self, staffID, department):
        # extract staff-to-department relationship as (staffnumber,"belongs_to","department name") tuple
        # and append it to the list
        r = fromStafftoDepartment(staffID, department)
        self.rel_stafftoDepartment.append(r)

    def addStafftoRole(self, staffID, role):
        r = fromStafftoRole(staffID, role)
        self.rel_stafftoRole.append(r)

    def addAssemblytocomponent(self, assemblyName, componentNumber):
        r = fromAssemblytoComponent(assemblyName, componentNumber)
        self.rel_assemblytoComponent.append(r)

    def addcomponentDesignedby(self, componentNumber, staffNumber):
        r = fromComponenttoStaff(componentNumber, staffNumber)
        self.rel_componentDesignedby.append(r)

    def addcomponentSuppliedby(self, componentNumber, SupplierNumber):
        r = fromComponenttoSupplier(componentNumber, SupplierNumber)
        self.rel_componentSuppliedby.append(r)

    def addAssemblytoSystem(self, assemblyName, system):
        r = fromAssemblytoSystem(assemblyName, system)
        self.rel_assemblytoSystem.append(r)

    def addcomponentAssemby(self, componentNumber, workstationNumber):
        r = fromComponenttoWorkstation(componentNumber, workstationNumber)
        self.rel_componentAssembliedat.append(r)

    def addSystemtoModel(self, systemName, modelName):
        r = fromSystemtoModel(systemName, modelName)
        self.rel_systemtoModel.append(r)

    def addComponentConnection(self, component1, component2, connectionType):
        r = fromComponenttoComponent(component1, component2, connectionType)
        self.rel_componentConnectedto.append(r)

    def extractStaffRelation(self, datafile):
        print("Extracting staff-department relationship from the file...")
        datafile = pd.read_excel(
            datafile, index_col=None, sheet_name="Staff List")
        staffNumber = datafile["Staff Number"].tolist()
        department = datafile["Department"].tolist()
        role = datafile["Responsibility/Role"].tolist()
        for i in range(len(staffNumber)):
            self.addStafftoDepartment(staffNumber[i], department[i])
            self.addStafftoRole(staffNumber[i], role[i])

    def extractcomponentRelation(self, datafile, systemName='Electric Motor Systems'):
        print("Extracting component-assembly relationship from the file...")
        datafile = pd.read_excel(
            datafile, index_col=None, sheet_name=systemName)
        componentNumber = datafile["Component Number"].tolist()
        assembly = datafile["Assembly"].tolist()
        staff = datafile["Design Engineer"].tolist()
        supplier = datafile["Supplier"].tolist()
        workstation = datafile["Workstation"].tolist()

        for i in range(len(componentNumber)):
            self.addAssemblytocomponent(assembly[i], componentNumber[i])
            self.addcomponentDesignedby(componentNumber[i], staff[i])
            self.addcomponentSuppliedby(componentNumber[i], supplier[i])
            self.addcomponentAssemby(componentNumber[i], workstation[i])
        assembly = list(set(assembly))
        for i in range(len(assembly)):
            self.addAssemblytoSystem(assembly[i], systemName)

    def extractSystemtoModel(self, datafile, sheetname="Component System"):
        datafile = pd.read_excel(
            datafile, index_col=None, sheet_name=sheetname)
        systemName = datafile['Component System'].tolist()
        for v in systemName:
            self.addSystemtoModel(v, 'Model A')

    def extractComponentConnection(self, connectionList=part_connections.component_connection_list()):
        for connection_pair in connectionList:
            component1 = connection_pair[0]
            component2 = connection_pair[1]
            connectiontype = connection_pair[2]
            self.addComponentConnection(component1, component2, connectiontype)

    def extractAllRelation(self, datafile):
        self.extractStaffRelation(datafile)
        self.extractcomponentRelation(datafile)
        self.extractSystemtoModel(datafile)
        self.extractComponentConnection()

    def allRelations(self):
        return self.rel_assemblytoComponent+self.rel_assemblytoSystem +\
            self.rel_componentAssembliedat+self.rel_componentConnectedto +\
            self.rel_componentDesignedby+self.rel_componentSuppliedby +\
            self.rel_stafftoDepartment+self.rel_stafftoRole+self.rel_systemtoModel


if __name__ == "__main__":
    e = Relations()
    datafile = pd.ExcelFile("./data/Data.xlsx")
    e.extractAllRelation(datafile)
    print(e.rel_componentConnectedto)
