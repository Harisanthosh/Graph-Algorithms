"""
 Program to load the entries from Oracle DB and display it in GUI
"""
from fastapi import FastAPI, File, Form, UploadFile
import csv, ast
import pandas as pd
import sys
import datetime
from neo4j import GraphDatabase
import nxneo4j


app = FastAPI(title="Graph Algorithms", description="Create and execute graph algorithms in neo4j")

config = {
    "node_label": "Paper",
    "relationship_type": None,
    "identifier_property": "name"
}


class GraphAlgorithms(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def print_greeting(self, message,name,weightclass):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message,name,weightclass)
            print(greeting)

    def create_graph(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_manager, message)
            print(greeting)
            return greeting

    def get_greetings(self):
        with self._driver.session() as session:
            gnodes = session.write_transaction(self._get_greetings)
            for item in gnodes:
                print(f'{item}')
            print(gnodes)
            return gnodes

    def get_closeness_centrality(self):
        with self._driver.session() as session:
            gnodes = session.write_transaction(self._get_centrality)
            lst = []
            for item in gnodes:
                print(f'{item}')
                lst.append(item)
            print(gnodes)
            return lst

    def get_page_rank(self):
        with self._driver.session() as session:
            G = nxneo4j.Graph(self._driver, config)
            sorted_pagerank = sorted(nxneo4j.centrality.pagerank(G).items(), key=lambda x: x[1], reverse=True)
            for name, score in sorted_pagerank[:10]:
                print(name, score)
            return sorted_pagerank

    @staticmethod
    def _create_and_return_greeting(tx, message,name,weightclass):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "SET a.name = $name "
                        "SET a.weightclass = $weightclass "
                        "RETURN a.message + ', from node ' + id(a)", message=message,name=name,weightclass=weightclass)
        return result.single()[0]

    @staticmethod
    def _create_manager(tx, message):
        result = tx.run(message)
        return result
        #return result.single()[0]

    @staticmethod
    def _get_greetings(tx):
        rxx = tx.run("MATCH (n:Node)"
                     "RETURN n LIMIT 25")
        return rxx

    # @staticmethod
    # def _get_centrality(tx):
    #     rxx = tx.run("CALL algo.closeness.stream('Node', 'LINK')"
    #                  "YIELD nodeId, centrality"
    #                  ""
    #                  "RETURN algo.asNode(nodeId).id AS node, centrality"
    #                  "ORDER BY centrality DESC"
    #                  "LIMIT 20;")
    #     return rxx

    @staticmethod
    def _get_centrality(tx):
        rxx = tx.run("CALL algo.closeness.stream('Node', 'LINK')"
                     "YIELD nodeId, centrality")
        return rxx

@app.post("/files/")
async def upload_result(
    fileb: UploadFile = File(...)
):
    return {
        # "file_size": len(fileb.file.read()),
        "fileb_content_type": fileb.content_type,
    }

# @app.delete("/files/{table}")
# def remove_table(table: str):
#     return {"Hello": table}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/createnodes/{graph_query}")
def create_graph(graph_query: str):
    cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "123graph")
    return cx.create_graph(graph_query)
    #return {"item_id": item_id, "q": q}

@app.get("/getnodes")
def get_nodes_from_graph():
    cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "123graph")
    return cx.get_greetings()


@app.get("/getcentrality")
def get_centrality_of_graph():
    cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "123graph")
    return cx.get_closeness_centrality()

@app.get("/getrank")
def get_rank_of_graph():
    cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "123graph")
    return cx.get_page_rank()