# Conception et Déploiement d'API d'accès aux Données
Il est fortement conseillé de réaliser ce TP par groupe de deux étudiants.

Lors de cette dernière séance de travaux pratiques nous allons continuer à travailler sur la base de données IMDB du précédent TP. L'objectif sera cette fois-ci d'intégrer les requêtes, dont certaines nouvelles, dans des APIs qui seront mises à disposition à des développeurs par le biais d'une plateforme d'API Management.

## Préparatifs
- Les prérequis pour accéder aux bases de données sont les mêmes que pour le TP précédent: [instructions](https://github.com/lvovan/CS-IMC-2021-2022/blob/main/TP%20Bdd%20Graphe%20et%20Relationnelle.md#pr%C3%A9requis---cr%C3%A9ation-et-connexion-aux-bases-de-donn%C3%A9es)
- Si vous ne disposez pas encore d'une instance Azure API Management, créez-en une dès maintenant depuis le [portail Azure](https://portal.azure.com).

## Requêtes **TODO Francesca**
Pour démontrer l'ajout des genres
- 1x Requête Neo4j
- 1x Requête SQL

Pour se sensibiliser à la combinaisons de données multi-sources
- 2x Idées de requêtes où il faudrait requêter Neo4j et SQL pour une performance/efficacité maximale. La colonne **tTitles.runtimeMinutes** ne sera disponible que dans la base de données SQL

## Implémentation des APIs en serverless
Maintenant les requêtes conçues, il faut les rendre accessibles par le biais d'API. Cette approche a les avantages suivants:
 - Réduire et simplifier les prérequis pour les clients potentiels. Avec une API en http, le client n'aura pas besoin d'installer de SDK ou de drivers
 - Abstraire l'utilisation de son implémentation, fournissant une flexibilité supérieure lors de futures mises à jour de l'API
 - Pouvoir procéder à des optimisations fonctionnelles et techniques au niveau de la couche API avant de solliciter la base de données

TODO - Luc

## Mise à disposition via API Management
Vos APIs devraient maintenant être techniquement fonctionnelles. Exposons-les de manière formelle et standardisée avec Azure API Management.