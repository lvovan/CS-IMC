from py2neo import Graph
from py2neo.bulk import create_nodes, create_relationships
from py2neo.data import Node
import os
import pyodbc

server = os.environ["TPBDD_SERVER"]
database = os.environ["TPBDD_DB"]
username = os.environ["TPBDD_USERNAME"]
password = os.environ["TPBDD_PASSWORD"]
driver= '{ODBC Driver 17 for SQL Server}'

neo4j_server = os.environ["TPBDD_NEO4J_SERVER"]
neo4j_user = os.environ["TPBDD_NEO4J_USER"]
neo4j_password = os.environ["TPBDD_NEO4J_PASSWORD"]

if len(server)==0 or len(database)==0 or len(username)==0 or len(password)==0 or len(neo4j_server)==0 or len(neo4j_user)==0 or len(neo4j_password)==0:
	print("Au moins une des variables d'environnement n'a pas été initialisée.")
	exit(1)

try:
	print("Test de connexion avec py2neo...", end="", flush=True)
	graph = Graph(neo4j_server, auth=(neo4j_user, neo4j_password))
	graph.run("MATCH (n:Test) RETURN n")
	print("✔️")
	      
	print("Test de connexion avec pyodbc...", end="", flush=True)
	with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
		cursor = conn.cursor()
		cursor.execute("SELECT 1")
		print("✔️")
	
	print("La configuration est valide.")
	print("L'énoncé du TP est disponible sur: https://github.com/lvovan/CS-IMC/blob/main/TP%20Bdd%20Graphe%20et%20Relationnelle.md")
except Exception as error:
	print(error)
	print("Note: Si vous avez un timeout, réessayez dans quelques secondes pour donner à la base de données le temps de se 'réveiller'.")

print
