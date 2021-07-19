import pandas as pd
import json
from py2neo import Node

# Node is a class from the library py2Neo
# A Node has a 'label' as the first argument, which will be defined as the 'nodetype'
# A node takes a dictionary(key-value pairs) to store properties


class Component(Node):  # Define a component node type
    identified_By = "Component_Number"  # The name of unique ID label for the node
    nodeType = "Component"
    # The equivalent expressions for the node
    equivalence = ["component", "part"]

    def __init__(self, componentNumber, name, cost, inventory, quantity, unit='EA'):
        self.nodeProperties = {}
        self.nodeProperties["Component_Number"] = componentNumber
        self.nodeProperties["Name"] = name
        self.nodeProperties["Cost"] = cost
        self.nodeProperties["Inventory"] = inventory
        self.nodeProperties["Quantity"] = inventory
        self.nodeProperties["Unit"] = unit
        super().__init__(self.nodeType, **self.nodeProperties)


class ComponentSystem(Node):  # Define a system node type
    identified_by = "Name"
    nodeType = "System"
    equivalence = ["system", "subsystem"]

    def __init__(self, name):
        self.nodeProperties = {}
        self.nodeProperties['Name'] = name
        super().__init__(self.nodeType, **self.nodeProperties)


class Staff(Node):  # Define a staff node type
    identified_by = "StaffID"
    nodeType = "Staff"
    equivalence = ["Employee"]

    def __init__(self, name, number):
        self.nodeProperties = {}
        self.nodeProperties["Name"] = name
        self.nodeProperties["StaffID"] = number
        super().__init__(self.nodeType, **self.nodeProperties)


class Supplier(Node):  # Define a supplier node type
    identified_by = "SupplierID"
    nodeType = "Supplier"
    equivalence = ["supplier", "company", "seller"]

    def __init__(self, name, number):
        self.nodeProperties = {}
        self.nodeProperties["Name"] = name
        self.nodeProperties["SupplierID"] = number
        super().__init__(self.nodeType, **self.nodeProperties)


class Workstation(Node):  # Define a workstation node type
    identified_by = "WorkstationID"
    nodeType = "Workstation"
    equivalence = ["workstation", "assembly position"]

    def __init__(self, workstation):
        self.nodeProperties = {}
        self.nodeProperties["WorkstationID"] = workstation
        super().__init__(self.nodeType, **self.nodeProperties)


class Assembly(Node):  # Define an assembly node type, an assembly is a cluster of components (the bom structure is component-assembly-system-product)
    identified_by = "Name"
    nodeType = "Assembly"
    equivalence = ["module", "assembly"]

    def __init__(self, assembly):
        self.nodeProperties = {}
        self.nodeProperties["Name"] = assembly
        super().__init__(self.nodeType, **self.nodeProperties)


class Department(Node):  # Define a department node type
    identified_by = "Name"
    nodeType = "Department"
    equivalence = ["department", "division"]

    def __init__(self, department):
        self.nodeProperties = {}
        self.nodeProperties["Name"] = department
        super().__init__(self.nodeType, **self.nodeProperties)


class Role(Node):  # Define a Role(eg. Design engineer) node type
    identified_by = "Name"
    nodeType = "Role"
    Equivalence = ['job', 'title', 'position', 'role']

    def __init__(self, role):
        self.nodeProperties = {}
        self.nodeProperties["Name"] = role
        super().__init__(self.nodeType, **self.nodeProperties)


class Product(Node):  # Define a Product(eg. Model A) node type
    identified_by = "Name"
    nodeType = "Product"
    Equivalence = ["model", "product"]

    def __init__(self, product, status):
        self.nodeProperties = {}
        self.nodeProperties["Name"] = product
        self.nodeProperties["Status"] = status
        super().__init__(self.nodeType, **self.nodeProperties)


class Entities():  # Define a class whcih can store lists of all node types
    # A class which contains lists of all nodes to be created in the knowledge graph
    list_component = []
    list_componentsystem = []
    list_staff = []
    list_supplier = []
    list_workstation = []
    list_assembly = []
    list_department = []
    list_staffRole = []
    list_products = []

    # Transfer a node to a dictionary type (eg.{Label:"Component",Component_Number:"C0010001"})
    def nodeTodictionary(self, nodes):
        toDic = {}
        for k, v in nodes.items():
            toDic[k] = v
        return toDic

    # Transfer a node list to the dictionary(which contains a node as  dictionaries)
    def nodelistTOdictionary(self, nodelist):
        toDic = {}
        for node in nodelist:
            for k, v in node.items():
                if k in toDic and v not in toDic[k]:
                    toDic[k].append(v)
                else:
                    toDic[k] = [v]
        return toDic

    def NodeListtoJson(self):  # Export all nodes to json file
        toDic = {}
        toDic["Component"] = self.nodelistTOdictionary(
            self.list_component)
        toDic["Assembly"] = self.nodelistTOdictionary(self.list_assembly)
        toDic["System"] = self.nodelistTOdictionary(
            self.list_componentsystem)
        toDic["Department"] = self.nodelistTOdictionary(
            self.list_department)
        toDic["Products"] = self.nodelistTOdictionary(self.list_products)
        toDic["Staff"] = self.nodelistTOdictionary(self.list_staff)
        toDic["Role"] = self.nodelistTOdictionary(
            self.list_staffRole)
        toDic["Supplier"] = self.nodelistTOdictionary(self.list_supplier)
        toDic["Workstation"] = self.nodelistTOdictionary(
            self.list_workstation)
        with open("./data/nodeList.json", 'w') as f:
            json.dump(toDic, f)
        return toDic

    def addComponent(self, componentNumber, name, cost, inventory, quantity, unit):
        # add component as a Node object to the list_part list
        partNode = Component(componentNumber, name, cost,
                             inventory, quantity, unit)
        self.list_component.append(partNode)

    def addComponentSystem(self, name):
        # add system as a Node object to the list_part list
        componentSystemNode = ComponentSystem(name)
        self.list_componentsystem.append(componentSystemNode)

    def addStaff(self, name, staffID):
        # add staff as a Node object to the list_staff list
        staffNode = Staff(name, staffID)
        self.list_staff.append(staffNode)

    def addSupplier(self, name, supplierID):  # add a supplier node
        # add supplier as a Node object to the list_supplier list
        supplierNode = Supplier(name, supplierID)
        self.list_supplier.append(supplierNode)

    def addWorkstation(self, workstationID):
        # add workstation as a Node object to the workstation list
        workstationNode = Workstation(workstationID)
        self.list_workstation.append(workstationNode)

    def addAssembly(self, name):
        # add Assembly as a Node object to the Assembly list
        assemblyNode = Assembly(name)
        self.list_assembly.append(assemblyNode)

    def addDepartment(self, name):
        departmentNode = Department(name)
        self.list_department.append(departmentNode)

    def addStaffRole(self, name):
        # add job Role as a Node object to the job Role list
        staffroleNode = Role(name)
        self.list_staffRole.append(staffroleNode)

    def addProducts(self, name, status):
        productNode = Product(name, status)
        self.list_products.append(productNode)

    def extractComponentFromFile(self, datafile, systemName='Electric Motor Systems'):
        # extract all components information from a system part list, eg.Electric Motor System
        print(f"extracting all component info of {systemName}.....")
        bom = pd.read_excel(
            datafile, index_col=None, sheet_name=systemName)
        part_numbers = bom["Component Number"].tolist()
        part_names = bom["Component Name"].tolist()
        part_costs = bom["Cost"].tolist()
        part_quantities = bom['Qta'].tolist()
        part_units = bom['Unit'].tolist()
        part_inventory = bom['Inventory'].tolist()
        assembly_name = list(set(bom["Assembly"].tolist()))

        for i in range(len(part_numbers)):
            self.addComponent(
                part_numbers[i], part_names[i], part_costs[i], part_inventory[i], part_quantities[i], part_units[i])

        for v in assembly_name:
            self.addAssembly(v)

    def extractComponentsystemFromFile(self, datafile, sheetname='Component System'):
        # extract all components system  information (ID and name) from a file
        print("extracting all component system info.....")
        bom = pd.read_excel(
            datafile, index_col=None, sheet_name=sheetname)
        system_names = bom["Component System"].tolist()
        for i in range(len(system_names)):
            self.addComponentSystem(system_names[i])

    def extractStaffinofoFromFile(self, datafile, sheetname='Staff List'):
        # extract all Staff name and ID from the file
        print("extracting all staff info.....")
        staffinfo = pd.read_excel(
            datafile, index_col=None, sheet_name=sheetname)
        staffNumbers = staffinfo["Staff Number"].tolist()
        StaffNames = staffinfo["Name"].tolist()
        Departments = list(set(staffinfo["Department"].tolist()))
        Roles = list(set(staffinfo["Responsibility/Role"].tolist()))
        for i in range(len(staffNumbers)):
            self.addStaff(StaffNames[i], staffNumbers[i])
        for v in Departments:
            self.addDepartment(v)
        for v in Roles:
            self.addStaffRole(v)

    def extractSupplierFromFile(self, datafile, sheetname='Supplier List'):
        # extract all Supplier name and ID from the file
        print("extracting all supplier info.....")
        supplierinfo = pd.read_excel(
            datafile, index_col=None, sheet_name=sheetname)
        supplierNumber = supplierinfo["Supplier Code"].tolist()
        supplierName = supplierinfo["Supplier Name"].tolist()
        for i in range(len(supplierNumber)):
            self.addSupplier(supplierName[i], supplierNumber[i])

    def extractWorkstationFromFile(self, datafile, sheetname='Workstation List'):
        # extract all workstation name from the file
        print("extracting all workstation info.....")
        workstationinfo = pd.read_excel(
            datafile, index_col=None, sheet_name=sheetname)
        workstation = workstationinfo["Workstation"].tolist()
        for i in range(len(workstation)):
            self.addWorkstation(workstation[i])

    def extractProductsFromFile(self, datafile, sheetname="Product Family"):
        print("extracting product info....")
        productinfo = pd.read_excel(
            datafile, index_col=None, sheet_name=sheetname)
        product = productinfo["Product"].tolist()
        productStatus = productinfo["Status"].tolist()
        for i in range(len(product)):
            self.addProducts(product[i], productStatus[i])

    def extractAllNodes(self, datafile):
        self.extractComponentFromFile(datafile)
        self.extractComponentsystemFromFile(datafile)
        self.extractStaffinofoFromFile(datafile)
        self.extractSupplierFromFile(datafile)
        self.extractWorkstationFromFile(datafile)
        self.extractProductsFromFile(datafile)

    def allnodes(self):
        # Return all nodes of the object
        return self.list_assembly+self.list_component+self.list_componentsystem+self.list_department+self.list_staff+self.list_staffRole+self.list_supplier+self.list_workstation + self.list_products


if __name__ == "__main__":
    datafile = pd.ExcelFile("./data/Data.xlsx")
    e = Entities()
    e.extractAllNodes(datafile)
    print(e.allnodes())
