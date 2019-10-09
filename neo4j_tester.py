from neo4j import GraphDatabase

class HelloWorldExample(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def print_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    def get_greetings(self):
        with self._driver.session() as session:
            gnodes = session.write_transaction(self._get_greetings)
            for item in gnodes:
                print(f'{item}')
            print(gnodes)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

    @staticmethod
    def _get_greetings(tx):
        rxx = tx.run("MATCH (n:Greeting)"
                     "RETURN n LIMIT 25")
        return rxx

cx = HelloWorldExample("bolt://localhost:7687","neo4j","123graph")
cx.print_greeting("Champion")
cx.get_greetings()