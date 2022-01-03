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

graph = Graph(os.environ["TPBDD_NEO4J_SERVER"], auth=(os.environ["TPBDD_NEO4J_USER"], os.environ["TPBDD_NEO4J_PASSWORD"]))

BATCH_SIZE = 10000

print("Deleting existing nodes and relationships...")
graph.run("MATCH ()-[r]->() DELETE r")
graph.run("MATCH (n:Name) DETACH DELETE n")
graph.run("MATCH (n:Title) DETACH DELETE n")

with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    cursor = conn.cursor()

    # Titles
    exportedCount = 0
    cursor.execute("SELECT COUNT(1) FROM tTitles")
    totalCount = cursor.fetchval()
    cursor.execute("SELECT tconst, primaryTitle, startYear FROM tTitles")
    while True:
        importData = []
        rows = cursor.fetchmany(BATCH_SIZE)
        if not rows:
            break
        
        i = 0
        for row in rows:
            # Créer un objet Node avec comme label Title et les propriétés adéquates
            # A COMPLETER
            importData.append(n)
            i += 1

        try:
            create_nodes(graph.auto(), importData, labels={"Title"})
            exportedCount += len(rows)
            print(f"{exportedCount}/{totalCount} title records exported to Neo4j")
        except Exception as error:
            print(error)

    # Names
    # En vous basant sur ce qui a été fait dans la section précédente, exportez les données de la table tNames
    # A COMPLETER

    try:
        print("Indexing Title nodes...")
        graph.run("CREATE INDEX ON :Title(tconst)")
        print("Indexing Name nodes...")
        graph.run("CREATE INDEX ON :Name(nconst)")
    except Exception as error:
        print(error)


    # Relationships
    exportedCount = 0
    cursor.execute("SELECT COUNT(1) FROM tPrincipals")
    totalCount = cursor.fetchval()
    cursor.execute(f"SELECT nconst, category, tconst FROM tPrincipals")
    while True:
        importData = { "acted in": [], "directed": [], "produced": [], "composed": [] }
        rows = cursor.fetchmany(BATCH_SIZE)
        if not rows:
            break
        
        for row in rows:
            relTuple=(row[0], {}, row[2])
            importData[row[1]].append(relTuple)

        try:
            for cat in importData:
                # Utilisez la fonction create_relationships de py2neo pour créer les relations entre les noeuds Title et Name
                # (les tuples nécessaires ont déjà été créés ci-dessus dans la boucle for précédente)
                # https://py2neo.org/2021.1/bulk/index.html
                # ATTENTION: remplacez les espaces par des _ pour nommer les types de relation
                # A COMPLETER
                None # Remplacez None par votre code                
            exportedCount += len(rows)
            print(f"{exportedCount}/{totalCount} relationships exported to Neo4j")
        except Exception as error:
            print(error)