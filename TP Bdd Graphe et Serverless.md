# Travaux Pratiques Bases de Données Graphe et Serverless
Dans ce TP, nous allons travailler sur des jeux de données publics issus des [datasets IMDB](https://datasets.imdbws.com/)). Au démarrage du TP, ceux-ci sont disponibles dans une base de données relationelle [Azure SQL Database](https://docs.microsoft.com/fr-fr/azure/azure-sql/database/sql-database-paas-overview). Les objectifs du TP sont les suivants:

1. Se familiariser avec les différences de paradigme entre le requêtage relationnel et graphe
2. Transformer les données pour les exporter vers une base de données graphe Neo4j
3. Implémenter un ensemble de requêtes:
    - en SQL sur la base de donnée relationelle [Azure SQL Database](https://docs.microsoft.com/fr-fr/azure/azure-sql/database/sql-database-paas-overview)
    - en [Cypher](https://neo4j.com/developer/cypher/) sur la base de données graphe [Neo4j](https://neo4j.com/)
    - en [Apache Gremlin](https://tinkerpop.apache.org/docs/3.3.2/reference/#graph-traversal-steps) sur une base de données graphe répartie [Cosmos Db](https://docs.microsoft.com/en-us/azure/cosmos-db/graph/graph-introduction)
4. (optionnel) Encapsuler ces requêtes dans des API serverless (Azure Functions) et mesurer les performances

## Création et connexion aux bases de données
**⚠️Note:** Il est fortement conseillé de passer l'interface en **anglais** afin de suivre plus facilement les instructions du TP.

0. Si possible, installez [Azure Data Studio](https://docs.microsoft.com/fr-fr/sql/azure-data-studio/download-azure-data-studio?view=sql-server-ver15) pour faciliter la création de vos requêtes SQL. Si ce n'est pas possible, vous pourrez également effectuer les requêtes depuis votre navigateur.
1. Connectez-vous au [portail Azure](https://portal.azure.com), et ouvrez la page correspondant la base de données SQL `tpbdd-movies-sql`
2. Autorisez votre adresse IP dans le firewall du serveur SQL, ce qui vous permettra d'effectuer vos requêtes depuis votre ordinateur:

    1. Cliquez sur **Set server firewall**

        ![image](https://user-images.githubusercontent.com/22498922/147907059-5ec9d710-461c-4354-8527-182bc2d70c02.png)
    3. Puis sur **+ Add client IP**, ce qui ajoute votre IP à la liste existante

        ![image](https://user-images.githubusercontent.com/22498922/147907042-632dde1f-6e4b-4554-87f2-8866840ea8c0.png)
    5. Puis sur **Save** pour appliquer l'ajout

3. Connectez-vous à la base de données via l'onglet *Query editor)* à gauche, ou en récupérant les informations de connexion dans l'onglet **Connection strings** et en réutilisant ces informations dans Azure Data Studio.

## Exploration des données SQL
**Exercice 0**: Décrivez les tables et les attributs.

**Exercice 1**: Visualisez l'année de naissance de l'artiste `Jude Law`.

**Exercice 2**: Comptez le nombre d'artistes présents dans la base de donnee. 

**Exercice 3**: Trouvez les noms des artistes nés en `1960`, affichez ensuite leur nombre.

**Exercice 4**: Trouvez l'année de naissance la plus représentée parmi les acteurs (sauf 0!), et combien d'acteurs sont nés cette année là.

**Exercice 5**: Trouvez les artistes ayant joué dans plus d'un film

**Exercice 6**: Trouvez les artistes ayant eu plusieurs responsabilités au cours de leur carrière (acteur, directeur, producteur...).

**Exercice 7**: Trouver le nom du ou des film(s) ayant le plus d'acteurs (i.e. uniquement *acted in*).

**Exercice 8**: Montrez les artistes ayant eu plusieurs responsabilités dans un même film (ex: à la fois acteur et directeur, ou toute autre combinaison) et les titres de ces films.

# Neo4j
Neo4j est une base de données graphe. Les données sont représentées par des nœuds, des relations entre les nœuds et des propriétés:
1. Les nœuds et les relations contiennent des propriétés
2. Les *relations* connectent les nœuds
3. Les *propriétés* sont des paires clé-valeur pouvant être associées à des nœuds ou des relations
4. Les relations ont des *directions*: unidirectionnelles et bidirectionnelles

### Création d'une base de données Neo4j
Pour la suite du TP, nous aurons besoin de créer une base de données Neo4j en mode "bac à sable" (Sandbox). Pour cela:
1. Créez une base de données  [Neo4j Sandbox](https://neo4j.com/sandbox/). Utilisez les informations que vous souhaitez pour la création de compte.
2. Parmi les templates, créez une base vierge (*Blank sandbox*)
3. Dans le portail Neo4j (un lien vous a été envoyé par email), dépliez la ligne correspondant à votre sandbox puis allez dans l'onglet **Connection details** pour noter ces informations de connexion qui vous seront utiles ultérieurement.
![image](https://user-images.githubusercontent.com/22498922/147907013-ae0f0d32-7982-464b-969a-576646407c9c.png)

### Cypher 
Le langage de requêtage utilisé par Neo4j est [Cypher](https://neo4j.com/developer/cypher/). Vous trouverez sa [documentation officielle](https://neo4j.com/docs/cypher-refcard/current/) sur le site de Neo4j.

Cypher est basé sur des **patterns**. Un pattern décrit les données et permet d'interroger le graphe par le biais d'une syntaxe visuelle très similaire à la façon dont sont généralement illustrées sur papier les données dans un graphe.

On utilise des:
* Cercles `()` pour représenter les **nœuds**
* Flèches `-->` pour représenter les **relations**

**Patterns** :
1. nœud a : `(a)`
2. une relation entre deux nœuds : `(a)–>(b)` 
3. un chemin : `(a)–>(b)<–(c)`
4. un label (ou étiquette) : `(a:label)`

Les patterns sont utilisés pour le requêtage et visent à surtout réprésenter la structure des liens entre les nœuds, comme on peut le voir dans les exemples suivants:
1. `(a)–(b)`
2. `(a)-[r]- >(b) `
3. `(a)-[r:REL_TYPE]->(b) `
4. `(a)-[:REL_TYPE]->(b) `
5. `(a)-[*]->(b)`

#### Création de noeuds
Le statement `CREATE` nous permet de créer des noeuds selon la structure suivante :  
```
CREATE (nodePseudoVariable:nodeLabel { nodePropertyName: nodePropertyValue, .. })
```

Supposons que nous voulions créer deux noeuds: `Alice` et `Bob` de type `Person` avec la propriéte `name`, les requêtes seraient les suivantes: 
```
query = ("CREATE (Alice:Person { name: 'Alice' }) "
query = ("CREATE (Bob:Person { name: 'Bob' }) "
```

Nous pouvons aussi lier les noeuds par des relations, comme par exemple en indiquant que `Bob` et `Alice` se connaissent:

```
MATCH
  (a:Person),
  (b:Person)
WHERE a.name = 'Alice' AND b.name = 'Bob'
CREATE (a)-[r:RELTYPE]->(b)
RETURN type(r)
```

#### Création de relations
Le statement `MATCH` permet également de créer des relations entre des noeuds préalablement identifiés (*matchés*) en fonction de conditions:
```
MATCH (a:NodeLabel),(b:NodeLabel)
WHERE .....
CREATE (a)-[r:RELTYPE]->(b)
RETURN type(r)
```

Pour sélectionner tous les noeuds, utilisez la requête suivante:
```
MATCH ( n ) 
RETURN n
```

Autre exemple, pour sélectionner tous les noeuds disposant de la propriété `label`

```
MATCH (n:label) 
RETURN n
```

Pour affiner encore d'avantage, voici comment sélectionner tous les noeuds ayant une propriété `label` dont la valeur vaut `value` :


```
MATCH ( n )
WHERE n. label : 'value'
RETURN n
```

Pour supprimer des noeuds, utilisez le statement `DELETE`.

## Export des données vers un modèle graphe
**⚠️Note:** Il est fortement conseillé de réaliser cette partie du TP sur une machine Linux ou Mac.
1. Téléchargez les fichiers [export-neo4j.py](TP-Bdd-src/export-neo4j.py) dans un dossier local. Il contient le code (Python) nécessaire à l'exécution de l'export, mais pas la logique de transformation des données. Installez les dépendance (**pyodbc** et **py2neo**) avec les commandes suivantes:

```
        sudo apt install unixodbc-dev
        sudo -H pip3 install pyodbc
        pip3 install py2neo
```

Si des problèmes avec **pyodbc** subsistent, suivez [ces instructions](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15).

3. (recommandé) Créez un environnement virtuel Python dans votre dossier local
4. Installez **pyodbc**:  `sudo -H pip install pyodbc`
5. Installez les autres prérequis: `pip install -r requirements.txt`
6. Préparez un script qui initialise les variables d'environnement indiquées au début du fichier [export-neo4j](TP-Bdd-src/export-neo4j.py) (`TPBDD_SERVER`, `TPBDD_DB`, etc.) avec les informations de connexion récupérées dans la section précédente. Pour la variable `TPBDD_NEO4J_SERVER`, il s'agit de l'URL commençant par `bolt://` 
7. Complétez le programme aux endroits notés `A COMPLETER`. N'hésitez pas à déboguer en ajoutant des `print`, créer des programmes de test etc.
8. Effectuez l'export vers votre base Neo4j Sandbox

## Requêtes graphe (Cypher)
**Exercice 1**: Ajoutez une personne ayant votre prénom et votre nom dans le graphe. Verifiez qui le noeud a bien éte crée. 

**Exercice 2**: Ajoutez un film nommé `L'histoire de mon 20 au cours Infrastructure de donnees`

**Exercice 3**: Ajoutez la relation `ACTED_IN` qui modélise votre participation à ce film en tant qu'acteur/actrice

**Exercice 4**: Ajoutez deux de vos professeurs/enseignants comme réalisateurs/réalisatrices de ce film.

**Exercice 5**: Affichez le noeud représentant l'acteur nommé `Jude Law`, et visualisez son année de naissance.

**Exercice 6**: Visualisez l'ensemble des films.

**Exercice 7**: Trouvez les noms des artistes nés en `1960`, affichez ensuite leur nombre.

**Exercice 8**: Trouver l'ensemble des acteurs (sans entrées doublons) qui ont joué dans plus d'un film.

**Exercice 9**: Trouvez les artistes ayant eu plusieurs responsabilités au cours de leur carrière (acteur, directeur, producteur...).

**Exercice 10**: Montrez les artistes ayant eu plusieurs responsabilités dans un même film (ex: à la fois acteur et directeur, ou toute autre combinaison) et les titres de ces films.

**Exercice 11**: Trouver le nom du ou des film(s) ayant le plus d'acteurs.

## Requêtes graphe (Gremlin)
Une autre base de données graphe a été créée pour ce TP.  Elle utilise la technologie Cosmos DB et utilise un langage de requêtage différent: [Apache Gremlin](https://tinkerpop.apache.org/docs/3.3.2/reference/#graph-traversal-steps).

Vous pourrez trouver cette base, déjà préremplie, dans le portail Azure sous le nom `tpbdd-movies-cdb`. Vous pourrez y effectuer des requêtes en utilisant l'onglet **Data Explorer**.

**Exercices**: Effectuez toutes les requêtes de la section précédentes en utilisant ce langage de requêtage.

## (optionnel, points bonus) Encapsulation dans des APIs serverless
Implémentez quelques unes des requêtes du TP sous forme d'API Serverless avec Azure Function ou AWS Lambda. Mesurez les performances.
