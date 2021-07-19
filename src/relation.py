# This file contains a Relation Class and its Child class (for specific relations in the graph)

from py2neo import Node
import pandas as pd


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
    inverse = ['']
    equivalence = ['the personnel of', 'belong to']

    def __init__(self, staffID, department):
        super().__init__(self.startnodetype, self.endnodetype, staffID,
                         department, self.label)


class fromStafftoRole(Relation):
    label = "works_as"
    startnodetype = "Staff"
    endnodetype = "Role"
    inverse = ['have']
    equivalence = ['is responsible for ', 'works as']

    def __init__(self, staffID, role):
        super().__init__(self.startnodetype, self.endnodetype, staffID,
                         role, self.label)


class fromAssemblytoComponent(Relation):
    label = "consists_of"
    startnodetype = "Assembly"
    endnodetype = "Component"
    inverse = ['composes']
    equivalence = ['consists of', 'composed of']

    def __init__(self, assembly, component_number):
        super().__init__(self.startnodetype, self.endnodetype, assembly,
                         component_number, self.label)


class fromAssemblytoSystem(Relation):
    label = "assemled_to"
    startnodetype = "Assembly"
    endnodetype = "System"
    inverse = ['assembled by', 'consists of', 'composed of', 'compose']
    equivalence = []

    def __init__(self, assembly, system):
        super().__init__(self.startnodetype, self.endnodetype, assembly,
                         system, self.label)


class fromSystemtoModel(Relation):
    label = "system_of"
    startnodetype = "System"
    endnodetype = "Product"
    inverse = ['assembled by', 'consists of', 'composed of', 'compose']
    equivalence = []

    def __init__(self, system, product):
        super().__init__(self.startnodetype, self.endnodetype, system, product, self.label)


class fromComponenttoStaff(Relation):
    label = "designed_by"
    startnodetype = "Component"
    endnodetype = "Staff"
    inverse = ['design']
    equivalence = []

    def __init__(self, component, staff):
        super().__init__(self.startnodetype, self.endnodetype, component, staff, self.label)


class fromComponenttoSupplier(Relation):
    label = "supplied_by"
    startnodetype = "Component"
    endnodetype = "Supplier"
    inverse = ['supply']
    equivalence = ['purchased from', "supplied by"]

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

    def extractAllRelation(self, datafile):
        self.extractStaffRelation(datafile)
        self.extractcomponentRelation(datafile)
        self.extractSystemtoModel(datafile)


if __name__ == "__main__":
    e = Relations()
    datafile = pd.ExcelFile("./data/Data.xlsx")
    e.extractAllRelation(datafile)
    print(e.rel_componentDesignedby)
