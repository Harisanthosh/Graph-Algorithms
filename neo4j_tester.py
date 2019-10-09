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

    def get_greetings(self):
        with self._driver.session() as session:
            gnodes = session.write_transaction(self._get_greetings)
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
    def _get_greetings(tx):
        rxx = tx.run("MATCH (n:Greeting)"
                     "RETURN n LIMIT 25")
        return rxx

cx = HelloWorldExample("bolt://localhost:7687","neo4j","123graph")
cx.print_greeting("Champion","Stipe Miocic","265lbs")
cx.get_greetings()



"""
For Establishing Relations
MATCH (n:Greeting {name:"Khabib"}) 
MATCH (t:Greeting {name:"Kamaru Usman"})
CREATE (n)-[r:MANAGED_BY {agent:"Ali abdelaziz"}]->(t)
RETURN n,r,t


For Delete
MATCH (p:Person) where ID(p)=1
OPTIONAL MATCH (p)-[r]-() //drops p's relations
DELETE r,p
"""