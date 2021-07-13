from neo4j import GraphDatabase
import csv


class Mydata:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def createpart(self, partnumber):  # Create a isolated partnumber
        with self.driver.session() as session:
            info = session.write_transaction(self._createpart, partnumber)
            print(info+"has been created")

    @staticmethod
    def _createpart(tx, partnumber):
        result = tx.run("CREATE (p:Part {part_number: $partnumber}) "
                        "RETURN p.Part_number ", partnumber=partnumber)
        return result.single()[0]

    def linkpart(self, partnumber1, partnumber2, method):
        with self.driver.session() as session:
            session.write_transaction(
                self._linkpart, partnumber1, partnumber2, method)
            print("link has been created")

    @staticmethod
    def _linkpart(tx, partnumber1, partnumber2, method):
        query = ("MATCH (a:Part {part_number: $partnumber1}), (b:Part {part_number: $partnumber2}) "
                 "MERGE (a)-[c:connected_with {method:$method}]-(b)"
                 )
        result = tx.run(query, partnumber1=partnumber1,
                        partnumber2=partnumber2, method=method)
        return result

    def delete_all(self):  # Clear all data in the database
        with self.driver.session() as session:
            session.write_transaction(self._delete_all)
        print("all data cleared")

    @staticmethod
    def _delete_all(tx):
        query = ("MATCH (n)" "DETACH DELETE n")
        tx.run(query)

    def importBom(self):
        with self.driver.session() as session:
            session.write_transaction(self._importBom)
            print("import successful")

    @staticmethod
    def _importBom(tx):
        query = ('LOAD CSV WITH HEADERS FROM "file:///BOM.csv" AS row '
                 'WITH DISTINCT row.`Part Number` AS partnumber, row.`Part Name` AS partname, row.Supplier AS supplier,'
                 'row.System AS system,row.Inventory as inventory, row.`Contract Price` AS price, row.`Design Engineer` AS engineer '
                 'MERGE(p:Part {part_number: partnumber,part_name:partname,inventory:inventory})'
                 'CREATE(f:FinancialInfo {purchase_Price: price}) <-[:cost_info]-(p)'
                 'MERGE(s:System {system_name: system}) '
                 'MERGE(e:Staff{Staff_name:engineer}) '
                 'MERGE(o:Organization{Organization_name:supplier}) '
                 'MERGE (s)-[:contains]->(p) '
                 'MERGE(p)-[:Designed_by]->(e)'
                 'MERGE(p)-[:Supplied_by]->(o)'

                 )
        tx.run(query)


if __name__ == "__main__":
    url = "bolt://localhost:7687"
    usrname = "neo4j"
    paswd = "1234"
    mydata = Mydata(url, usrname, paswd)
    # mydata.importBom()
    # mydata.createpart("1234")
    # mydata.delete_all()
    mydata.linkpart("10001", "10011", "bolt")
    mydata.close()
