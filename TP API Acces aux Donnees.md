# Conception et Déploiement d'API d'accès aux Données
Il est fortement conseillé de réaliser ce TP par groupe de deux étudiants.

Lors de cette dernière séance de travaux pratiques nous allons continuer à travailler sur la base de données IMDB du précédent TP. L'objectif sera cette fois-ci d'intégrer les requêtes, dont certaines nouvelles, dans des APIs qui seront mises à disposition à des développeurs par le biais d'une plateforme d'API Management.

## Préparatifs
- Les prérequis pour accéder aux bases de données sont les mêmes que pour le TP précédent: [instructions](https://github.com/lvovan/CS-IMC-2021-2022/blob/main/TP%20Bdd%20Graphe%20et%20Relationnelle.md#pr%C3%A9requis---cr%C3%A9ation-et-connexion-aux-bases-de-donn%C3%A9es)
- Si vous ne disposez pas encore d'une instance Azure API Management, créez-en une dès maintenant depuis le [portail Azure](https://portal.azure.com).

## 1- Requêtes

Des données supplémentaires sont disponibles par rapport au TP précédent:
- Le ou les es genres (comédie, action...) associés aux films
- Les notations (*averageRating*) pour les films - mais uniquement dans la base SQL

Ecrire les requêtes 
-  le genre des films directed et avec la participation du meme artiste
- En SQL: la note moyenne des films par genre/artiste/directeur

Pour se sensibiliser à la combinaisons de données multi-sources
- 2x Idées de requêtes où il faudrait requêter Neo4j et SQL pour une performance/efficacité maximale. La colonne **tTitles.runtimeMinutes** ne sera disponible que dans la base de données SQL

## 2- Création en Terraform des ressources APIs en serverless
Maintenant les requêtes conçues, créons des APIs qui permettront de les exécuter. En effet, les APIs permettent de:
 - **Réduire et simplifier les prérequis pour les clients.** Avec une API en http, l'appelant n'aura besoin d'installer ni SDK, ni driver spécifique
 - **Abstraire l'utilisation (endoint http) de l'implémentation (python, SQL, Cypher)**, fournissant une flexibilité supérieure lors de futures mises à jour de l'API
 - **Effectuer des opérations fonctionnelles et techniques au niveau de la couche API** (ex: transformations, caching...) avant de solliciter la base de données

Nous implémenterons ces APIs sous la forme de code en Python, hébergées en serverless ([FaaS](https://en.wikipedia.org/wiki/Function_as_a_service)) dans [Azure Function Apps](https://azure.microsoft.com/fr-fr/services/functions/) et déployées en CI/CD via [Github Actions](https://fr.github.com/features/actions).

### Infrastructure as Code avec Terraform
Pour implémenter notre solution notre template Terraform aura besoin de préparer les éléments suivantes:
 - La base de données SQL qui contient les données relationnelles
 - L'[Azure Function App](https://azure.microsoft.com/fr-fr/services/functions/) qui gèrera le code Python, l'[App Service Plan](https://docs.microsoft.com/fr-fr/azure/app-service/overview-hosting-plans) associé qui s'occupe de son exécution et le [compte de stockage](https://docs.microsoft.com/fr-fr/azure/storage/common/storage-account-overview) qui le persiste.
 - Définir les paramètres de connexion pour que les Azure Functions sachent où se connecter (SQL, Neo4j)
 - Notons que pour des raisons de simplification, nous n'instancierons pas Neo4j via Terraform

 1. Connectez-vous au portail Azure et démarrez [Azure Cloud Shell](https://docs.microsoft.com/fr-fr/azure/cloud-shell/overview) via l'icône en haut à droite de la page (PowerShell ou Bash fonctionneront aussi biens l'un que l'autre)
 2. Créez un dossier dans lequel vous allez travailler
 3. Initialisez Terraform pour une première utilisation: `terraform init`
 4. Téléchargez le template Terraform **api.tf** préparé pour ce TP avec `curl https://raw.githubusercontent.com/lvovan/CS-IMC-2021-2022/main/TP-API/api.tf` 
 5. Editez le et modifiez les noms de toutes les ressources (`name`) pour les rendre unique, en intégrant par exemple vos noms
 6. Pour la Function App et l'App Service Plan, compléter les propriétés `resource-group-name` et `location` pour vous assurer que ces deux ressources sont positionnées dans le groupe de ressource adéquat, et créées dans la même région Azure que ce dernier.
 7. Remplissez les paramètres manquants dans la section `app_settings`. Ces paramètres seront utilisées par les fonctions pour se connecter aux bases.
 8. Vérifiez que votre template est correct avec `terraform validate`, corrigez si nécessaire
 8. Créez votre plan d'exécution: `terraform plan -out main.plan`
 9. Exécutez le plan: `terraform apply main.plan`
10. Vérifiez que toutes les ressources ont été créées telles que déclarées dans votre templatem y compris les app settings. Si ce n'est pas le cas, vous pouvez soit:
- Modifier votre template, exécuter `plan` et `apply`
- Ou tout détruire avec `destroy` et relancer - vous verrez que certains types de ressources ne peuvent être mises à jour et doivent être détruites pour ensuite être reconstruites avec la configuration désirées.

## 3- Déploiement automatisé avec Github Actions
1. Si vous ne disposez pas d'un compte Github, [créez-en un](https://github.com/signup)
2. Clonez le repository [https://github.com/lvovan/CS-IMC-2021-2022-TP-API](https://github.com/lvovan/CS-IMC-2021-2022-TP-API)
3. Modifions maintenant le workflow de déploiement
    - Editez le fichier de workflow dans **.github/workflows/main.yml**
    - Modifiez la valeur de la variable d'environnement `AZURE_FUNCTIONAPP_NAME` pour y mettre le nom de la Function App créée précédemment par votre template Terraform
    - Notez que la dernière ligne du workflow mentionne un secret nommé `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`. Le *publish profile* contient les informations permettant de déployer du code dans votre function app. Il est disponible dans le portail Azure, au haut de la page principale de votre fonction via le bouton **Get publish profile"**.
    - Téléchargez ce fichier, ouvrez le dans un éditeur de texte
    - Retournez dans votre repository Github et dans les paramètres de votre repository créez le secret nommé `AZURE_FUNCTIONAPP_PUBLISH_PROFILE` et collez le contenu du fichier *publish profile* en tant que valeur
4. Retournez dans l'onglet **Actions** et vous devriez voir un déploiement se déclencher. Si ce n'est pas le cas, déclenchez le workflow manuellement.
5. Retournez dans le portail Azure pour voir votre Function App
6. Cliquez sur Functions: vous devriez voir 5 fonctions (Query1..5), cliquez sur Query1 puis sur **Get function Url** pour obtenir l'adresse qui vous permettra de tester le bon fonctionnement de votre fonction

## 4- Implémentation des APIs
Nous allons spécifier et implémenter maintenant les requêtes travaillées dans la partie 1. Vous utiliserez pour cela les fonctions **Query2** à **Query5** déjà préparées. Utilisez le code source de **Query1** pour apprendre comment requêter les bases de données en Python.

## 5- Mise à disposition via API Management
Vos APIs devraient maintenant être techniquement fonctionnelles. Exposons-les en tant que produits avec plusieurs niveaux (**tiers**) via Azure API Management.