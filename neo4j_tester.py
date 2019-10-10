from neo4j import GraphDatabase

class HelloWorldExample(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def print_greeting(self, message,name,weightclass):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message,name,weightclass)
            print(greeting)

    def print_manager(self, message,name):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_manager, message,name)
            print(greeting)

    def get_greetings(self):
        with self._driver.session() as session:
            gnodes = session.write_transaction(self._get_greetings)
            for item in gnodes:
                print(f'{item}')
            print(gnodes)

    def get_degree_centrality(self):
        with self._driver.session() as session:
            gnodes = session.write_transaction(self._get_centrality)
            for item in gnodes:
                print(f'{item}')
            print(gnodes)

    @staticmethod
    def _create_and_return_greeting(tx, message,name,weightclass):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "SET a.name = $name "
                        "SET a.weightclass = $weightclass "
                        "RETURN a.message + ', from node ' + id(a)", message=message,name=name,weightclass=weightclass)
        return result.single()[0]

    @staticmethod
    def _create_manager(tx, message, name):
        result = tx.run("CREATE (a:Agent) "
                        "SET a.message = $message "
                        "SET a.name = $name "
                        "RETURN a.message + ', from node ' + id(a)", message=message, name=name)
        return result.single()[0]

    @staticmethod
    def _get_greetings(tx):
        rxx = tx.run("MATCH (n:Greeting)"
                     "RETURN n LIMIT 25")
        return rxx

    @staticmethod
    def _get_centrality(tx):
        rxx = tx.run("CALL algo.degree.stream(null, $relation, {direction: $direct})"
                     "YIELD nodeId, score", relation="MANAGED_BY", direct="incoming")
        return rxx

cx = HelloWorldExample("bolt://localhost:7687","neo4j","123graph")
#cx.print_greeting("Champion","Nate Diaz","165lbs")
#cx.print_manager("Manager","Audie Attar")
cx.get_greetings()
cx.get_degree_centrality()



"""
For Establishing Relations
MATCH (n:Greeting {name:"Khabib"}) 
MATCH (t:Greeting {name:"Kamaru Usman"})
CREATE (n)-[r:MANAGED_BY {agent:"Ali abdelaziz"}]->(t)
RETURN n,r,t

MATCH (n:Greeting {name:"John Jones"}) 
MATCH (t:Agent {name:"Ali Abdelaziz"})
CREATE (n)-[r:MANAGED_BY]->(t)
RETURN n,r,t

For Delete
MATCH (p:Person) where ID(p)=1
OPTIONAL MATCH (p)-[r]-() //drops p's relations
DELETE r,p

MATCH ()-[r:RELEASED]-() 
DELETE r

Degree Centrality Theorem
CALL algo.degree.stream("", "MANAGED_BY", {direction: "incoming"})
YIELD nodeId, score
RETURN algo.asNode(nodeId).name AS name, score AS clients
ORDER BY clients DESC
"""