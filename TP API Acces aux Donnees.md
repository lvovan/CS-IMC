# Conception et Déploiement d'API d'accès aux Données
Il est fortement conseillé de réaliser ce TP par groupe de deux étudiants.

Lors de cette dernière séance de travaux pratiques nous allons continuer à travailler sur la base de données IMDB du précédent TP. L'objectif sera cette fois-ci d'intégrer les requêtes, dont certaines nouvelles, dans des APIs déployées avec un CI/CD qui seront mises à disposition à des développeurs par le biais d'une plateforme d'API Management. Afin de découvrir l'utilisation d'outillage avancé, nous utiliserons aujourd'hui très peu le portail Azure - nous sacrifierons un peu de convivialité pour beaucoup d'efficacité!

## Préparatifs
- Ajoutez votre IP sur le firewall de la base de données du TP, comme documenté dans le [TP précédent](https://github.com/lvovan/CS-IMC-2021-2022/blob/main/TP%20Bdd%20Graphe%20et%20Relationnelle.md#pr%C3%A9requis---cr%C3%A9ation-et-connexion-aux-bases-de-donn%C3%A9es). - Il ne sera cette fois-ci pas obligatoire d'installer localement **pyodbc**, mais pouvoir tester votre code en local accélèrera considérablement votre développement.

## 1- Requêtes
Des données supplémentaires sont disponibles par rapport au TP précédent:
- Le ou les es genres (comédie, action...) associés aux films
- Les notations (*averageRating*) pour les films - mais uniquement dans la base SQL

Ecrire les requêtes en SQL ou Cypher, selon la requête et vos préférences
- Les genres pour lesquels au moins un film a une même personne qui a été la fois directeur et acteur (ex: si Alice a été acteur à la fois directeur dans une comédie, et que Bob a été à la fois acteur et directeur dans un film d'action alors il faut renvoyer [comédie, action])
- La note moyenne des films par genre

Pour les requêtes suivantes, utilisez *au moins* la base de données graphe (i.e. ne faites pas que du SQL!)
- Requêtez la base pour aider à déterminer si il y a une correlation entre la durée d'un film et son genre
- Même demande que précédemment, en ajoutant le rating

## 2- Création en Terraform des ressources APIs en serverless
Maintenant les requêtes conçues, créons des APIs qui permettront de les exécuter. Exposer les requêtes sous forme d'APIs permet de:
 - **Réduire et simplifier les prérequis pour les clients.** Avec une API en http, l'appelant n'aura besoin d'installer ni SDK, ni pilote/driver spécifique sur la machine effectuant l'appel
 - **Abstraire l'utilisation (endoint http) de l'implémentation (Python, SQL, Cypher)**, fournissant une flexibilité bien supérieure lors de futures mises à jour de l'API
 - **Effectuer des opérations fonctionnelles et techniques au niveau de la couche API** (ex: transformations, fusion de données, caching...) avant de solliciter la base de données

Nous implémenterons ces APIs en Python 3.9, hébergées en serverless ([FaaS](https://en.wikipedia.org/wiki/Function_as_a_service)) dans [Azure Function Apps](https://azure.microsoft.com/fr-fr/services/functions/) et déployées en CI/CD via [Github Actions](https://fr.github.com/features/actions).

### Infrastructure as Code avec Terraform
Nous utiliserons Terraform pour déployer automatiquement l'infrastructure à savoir:

    - L'[Azure Function App](https://azure.microsoft.com/fr-fr/services/functions/) qui gèrera le code Python, l'[App Service Plan](https://docs.microsoft.com/fr-fr/azure/app-service/overview-hosting-plans) associé qui s'occupe de son exécution et le [compte de stockage](https://docs.microsoft.com/fr-fr/azure/storage/common/storage-account-overview) qui persiste le code de la fonction.
     - Définit les paramètres de connexion pour que les Azure Functions sachent comment se connecter (SQL, Neo4j)
     - Notons que pour des raisons de simplification, nous n'utiliserons pas Terraform pour instancier les bases SQL et Neo4j

 1. Connectez-vous au portail Azure et démarrez [Azure Cloud Shell](https://docs.microsoft.com/fr-fr/azure/cloud-shell/overview) via l'icône en haut à droite de la page (PowerShell ou Bash fonctionneront aussi biens l'un que l'autre)
 2. Créez un dossier dans lequel vous allez travailler
 3. Initialisez Terraform pour une première utilisation: `terraform init`
 4. Téléchargez le template Terraform [api.tf](https://raw.githubusercontent.com/lvovan/CS-IMC-2021-2022/main/TP-API/api.tf), déjà préparé pour ce TP. Utilisez `curl` ou `wget` depuis le Cloud Shell.
 5. Editez le et modifiez les noms de toutes les ressources (`name`) pour les rendre uniques (ex: préfixez par vos noms). Vous pouvez utiliser l'éditeur inclus dans le Cloud Shell (bouton **{}**), ou encore **vim** ou **nano**.
 6. Pour la Function App et l'App Service Plan, compléter les propriétés `resource-group-name` et `location` pour vous assurer que ces deux ressources sont positionnées dans le groupe de ressource adéquat, et créées dans la même région Azure que ce dernier.
 7. Remplissez les paramètres manquants dans la section `app_settings`. Ces paramètres seront utilisées par les fonctions pour se connecter aux bases. ⚠️ Le fichier tf n'ira pas sur le source control git donc indiquer les paramètres (dont les mots de passe) en dur ne pose pas de problème immédiat de sécurité. Dans un projet d'entreprise ces paramètres utiliseraient des secrets dans le CI/CD comme nous le verrons dans la section 3.
 8. (optionnel) Pour un peu d'exotisme, vous pouvez modifier la location du groupe de ressource, la [liste est documentée](https://github.com/claranet/terraform-azurerm-regions/blob/master/REGIONS.md), utilisez la première colonne (*Region name*)
 9. Vérifiez que votre template est correct avec `terraform validate`, corrigez si nécessaire
 10. Créez votre plan d'exécution: `terraform plan -out main.plan`
 11. Exécutez le plan: `terraform apply main.plan`
 12. Vérifiez que toutes les ressources ont été créées telles que déclarées dans votre templatem y compris les app settings. Si ce n'est pas le cas, vous pouvez soit:

    - Corrigez votre template, puis ré-exécuter `plan` et `apply`
    - Ou tout détruire avec `destroy` et relancer - vous verrez que certains types de ressources ne peuvent être mises à jour et doivent être détruites pour ensuite être reconstruites avec la configuration désirées.

## 3- Déploiement automatisé avec Github Actions
1. Si vous ne disposez pas d'un compte Github, [créez-en un](https://github.com/signup)
2. Forkez le repository [https://github.com/lvovan/CS-IMC-2021-2022-TP-API](https://github.com/lvovan/CS-IMC-2021-2022-TP-API) en utilisant le bouton **Fork** situé en haut à droite de la page.
3. Modifions maintenant le workflow de déploiement
    - Editez le fichier de workflow dans **.github/workflows/main.yml**
    - Modifiez la valeur de la variable d'environnement `AZURE_FUNCTIONAPP_NAME` pour y mettre le nom de la Function App précédemment instanciée par votre template Terraform
    - Notez que la dernière ligne du workflow mentionne un secret nommé `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`. Le *publish profile* contient les informations, y compris les mots de passe, permettant de déployer du code dans votre function app. Vous pouvez le télécharger en utilisant la commande `az functionapp deployment list-publishing-profiles --name [nom_de_votre_fonction] --resource-group [nom_de_votre_groupe_de_ressource]` depuis le Cloud Shell.
    - Retournez dans votre repository Github et dans les paramètres de votre repository créez le secret nommé `AZURE_FUNCTIONAPP_PUBLISH_PROFILE` et avec comme valeur le contenu du *publish profile* obtenu précédemment
4. Retournez dans l'onglet **Actions** et vous devriez voir un déploiement se déclencher. Si ce n'est pas le cas, déclenchez le workflow manuellement.
5. Retournez dans le portail Azure pour voir votre Function App
6. Cliquez sur Functions: vous devriez voir 5 fonctions (**Query1..5**), cliquez sur **Query1** puis sur **Get function Url** pour obtenir l'adresse qui vous permettra de tester le bon fonctionnement de votre fonction.
7. Après avoir invoqué l'URL de *Query1*, vous devriez voir s'afficher quelques informations lues depuis les bases de données et un message confirmant la bonne exécution de la fonction. 

## 4- Implémentation des APIs
Nous allons spécifier et implémenter maintenant les requêtes travaillées dans la partie 1 et le TP précédent. Vous utiliserez pour cela les fonctions **Query2** à **Query5** déjà préparées pour vous dans le repository.

ℹ️ Pour éditer les fichiers directement depuis votre repository, changez simplement le domaine de l'URL dans votre navigateur en remplaçant **github.com** par **github.dev**

- Utilisez le code source de **Query1** pour apprendre comment requêter les deux types de bases de données en Python
- Le package *py2neo* est utilisé pour requêter le base Neo4j, vous verrez un exemple de requête et de récupération des résultats
- Idem pour *pyodbc* qui permet de requêter la base SQL

Pour les requêtes 2 à 4, implémentez les requêtes de votre choix entre celles du TP précédent et celles de la partie 1. N'implémentez pas toutes ces requêtes avec la même technologie de requêtage.

Pour la requête 5, spécifiez et implémentez une API qui renvoie la durée moyenne des films qui correspondent aux critères genre, acteur et directeur. L'interprétation de cette énoncé vous est laissée libre.

## 5- Mise à disposition via API Management
Vos APIs devraient maintenant être techniquement fonctionnelles. Exposez-les en tant que produits avec plusieurs niveaux (**tiers**) via Azure API Management, et envoyez-nous un lien vers votre produit.
