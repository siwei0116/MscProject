# Knowledge-Graph-for-Engineering

## Background
A Knowledge graph to manage information for an Engineering Enterprise

##  Functions of scipt files
### Entity.py
* Defines Node class and subclasses of different node types.
* Defines Entities class which stores all nodelists

### Relation.py
* Defines the Relation class and subclasses of different relation types
* Defines the Relations class to store all lists of relations

### part_connection.py
* To parse the connections between components
  * A component connection is defined as a tuple(connecion_typecode, component_number) ， eg.(4,C0010001)
  * The connection_typecode can be used to retrieve the connection code in the dictionary stored at ./data/part_connectiontype.json
  * The function returns a tuple as '(component1,connectiontype,component2)'

### buildgraph.py
* Defines a class to build a Neo4j Graph database from an entity.Entities object and a relation.Relations object,
  
### question_parse.py(In progress) and query.py
* Defines a function, which takes in a question(string) as an argument
* Extract keywords from the string, and match the keywords with a word dictionary.
* Categorize the question type based on the keywords list.
  * for example, if the keywords list contains 'Department of Powertrain', 'Role' and 'How many'
    * the function in query.py can output a Neo4j Cypher query `MATCH (:Department)<-(:works_in)-(s:Staff)-(:works_as)->(:Role) RETURN s,COUNT(s) ` which returns number of staffs and a list of the staff
  * The function should be able to match the synonyms, eg ("Powertrain Department" for "Department of powertrain" and "Job title" for "Role) 
    * The synonym for a node type or relationtype 'eg. Department' can be stored inside the specific Node class.
    * It's not realistic to store all synonymns for instances of nodes as properties eg.'Department of Powertrain' has a synonym 'Powertrain Department'. So some other methods of NLP need to be explored.
  * The function should distinguish whether the keyword stands for: 
    * a genral node type ,eg.'Department
    * a specific node instance, eg. 'Department of Powertrain
    * a predicate, eg. 'work_as
    * a word for question type, eg. "How many"， "is there any"
  * As Natural Language Questions is complex, not all questions can be identified. The project aims to identify some question types as a demostration.

### rescal.py   
* Copied from https://github.com/mnick/rescal.py which may be useful for the embedding.
* Some other sources found for graph neural networks and embeddings include https://github.com/deepmind/graph_nets and https://github.com/thunlp/OpenKE
  
### logic.py
* a script copied from a tutorial code of a lecture [' Edx COURSE CS50 Artificial Intelligence with Python' ](https://cs50.harvard.edu/ai/2020/)
* Can be used for inference of propositional logic
* As the knowledge graph uses 'first-order logic' or 'description logic', need to be adapted to be used in the knowledge graph

## The Neo4j Configuration
The community version of Neo4j database is used locally
### Download
* Downloaded at https://neo4j.com/download-center/#community
### Start locally
* use the command “neo4j console” to start the Neo4j. 
* The default port for the database is  http://localhost:7474/
The default user and passwrd (which is used in the buildgraph.py) are both 'neoj4' 
* (In the case of the script,the password has been changed to '123456', see line13 of buildgraph.py)
