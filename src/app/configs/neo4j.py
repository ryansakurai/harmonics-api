"""
Singleton for the connection to Neo4j
"""
import os
import dotenv
from neo4j import GraphDatabase

dotenv.load_dotenv()

driver = GraphDatabase.driver(
    "neo4j+s://10ab7e50.databases.neo4j.io",
    auth = (
        os.getenv("NEO4J_USERNAME"),
        os.getenv("NEO4J_PASSWORD"),
    ),
)

driver.verify_connectivity()
