# Travaux Pratiques Pipeline et Dataflow
Dans ce TP, nous allons implémenter les principe *bronze, silver, gold* dans le cadre de la fusion de données sur l'usage des vélos à Paris. Nous allons utiliser [Azure Data Factory](https://docs.microsoft.com/fr-fr/azure/data-factory/introduction) pour:

1. Configurer Azure Data Factory
2. Importer (copier) des données au format CSV depuis un espace de stockage [AWS S3 Bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingBucket.html) vers un stockage [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/#documentation)
3. Créer un data flow et référencer les deux jeux de données
4. Produire des données *silver* qui fusionnent les deux jeux de données
5. Produire des données *gold* qui agrègent les données créées dans la zone *silver*

Les fichiers que nous utilisons sont:
    - *comptage-velo-donnees-compteurs.csv* qui contient le nombre de passages par station de comptage (environ 1M d'enregistrements), initialement hébergé sur AWS
    - *comptage-velo-compteurs.csv* qui contient les informations des compteurs eux-mêmes (un peu moins de 300 enregistrements), hébergé sur Azure

## Création et configuration d'Azure Data Factory
1. Créez une instance Azure Data Factory via le portail Azure
2. Connectez-vous au studio associé à cette instance (lien dans l'onglet *Overview*, section *Getting started*). Si nécessaire, passez le studio en anglais (icône de l'engrenage en haut à droite)
3. A gauche, dans la section *Manage* créez deux *Linked services*
    - Choisissez *Amazon S3* et entrez les informations de connexion fournies en cours. Cliquez sur *Test connection* pour vous assurer que la connexion fonctionne.
    - Choisissez *Azure Blob Storage*, puis sélectionnez la souscription *Azure Internal - CentraleSupelec* et le compte de stockage *veloparisazure*. Cliquez sur *Test connection* pour vous assurer que la connexion fonctionne.

## Importation des données depuis AWS S3 et création des datasets
Maintenant que vous pouvez vous connecter aux espaces de stockage, copions le fichier *comptage-velo-donnees-compteurs.csv* qui contient les données comptages de S3 avec le Blob Storage.
1. Cliquez sur *Author* à gauche, puis créez un nouveau *Pipeline*
2. Dans la liste des *Activities*, dépliez *Move & transform* et glissez-déposez l'activité *Copy data* sur l'espace de travail juste à droite
3. Cliquez sur l'activité, le panneau du bas vous permet de la configurer.
4. Dans *Source* cliquez sur *New* et allez chercher le fichier *comptage-velo-donnees-compteurs.csv* en passant par le *Linked service* adéquat. Utilisez le bouton *Browse* (icône de dossier) pour vous y aider, nommez le *compteurs-aws*
5. Dans *Sink* (la destination de la copie), créez un nouveau dataset dans le *Linked Service* blob storage. Ce fichier sera également au format CSV.
    - Nommez le dataset *comptages_azure*
    - Dans *File path* mettez: **bronze/import-[votrenom]** et rien pour *File*
    - Décochez *First row as header*
    - Dans *Import schema* choisissez *None*
6. Pour chacun des datasets créés:
    - Dans l'onglet Connection, choisissez ";" (Semicolon) comme *Column delimiter*
    - Toujours dans l'onglet Connection, assurez-vous que *First row as header* est bien coché
    ![image](https://user-images.githubusercontent.com/22498922/146524247-7b5c9511-0a47-49cb-a278-c2de184b9cab.png)

8. Cliquez sur *Validate all* en haut de l'écran, il ne devrait pas y avoir d'erreur. S'il y en a, cliquez sur l'erreur et le portail vous pointera vers cette dernière
9. Cliquez sur *Publish all* pour sauvegarder
10. Lancez votre pipeline en cliquant sur *Add trigger* puis *Trigger now*. Vous pouvez observer votre run dans l'onglet *Monitor*
11. Depuis le portail Azure, allez dans l'espace de stockage *veloparisazure* et vous devriez retrouver votre fichier en utilisant le [Storage browser](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/43515dcd-cf02-45fd-bc30-f2c80dccc7dc/resourcegroups/datatransformation-rg/providers/Microsoft.Storage/storageAccounts/veloparisazure/storagebrowser)
12. Référençons maintenant les données des compteurs en créant un nouveau dataset pointant vers le fichier **bronze/ /comptage-velo-compteurs.csv** (utilisez le bouton *Browse*) et cochez *First row as header*

## Jointure des données
Nos données sont maintenant réunies dans notre Data Lake (le blob Storage). Effectuons la jointure!
1. Modifiez le dataset *comptages_azure* pour qu'il pointe vers le fichier importé (*File path*, utilisez le bouton *Browse* pour vous aider)
2. Pour le dataset *compteurs*:
    - Dans l'onglet Connection, choisissez ";" (Semicolon) comme *Column delimiter*
    - Toujours dans l'onglet Connection, assurez-vous que *First row as header* est bien coché
    - Dans l'onglet Schema, cliquez sur *Import schema* puis *From connection/store*
3. Validez puis publiez
4. Créez un nouveau Data flow
    - Avec deux sources de données, *comptages_azure* et *compteurs*
    - Effectue une jointure **left outer** sur le champs *Identifiant du compteur*
      ![image](https://user-images.githubusercontent.com/22498922/146525724-9640f1b0-e8f3-4f81-bfef-366dfd9bdd1a.png)

    - Ecrit la sortie (*Sink*) dans le container *output* du Blob Storage, au format CSV (ex: **silver/vovan/**)

    ![image](https://user-images.githubusercontent.com/22498922/146520673-14caaf82-128f-4b2c-8435-1b0d3cb4c8f5.png)

5. N'oubliez pas de valider et de publier!
6. Editez votre pipeline de copie et ajoutez maintenant le Data flow que vous venez de crée en  vous assurant que la copie a lieu **avant** le Data flow. Utilisez les rectangles verts pour connecter les boîtes entre elles.
    ![image](https://user-images.githubusercontent.com/22498922/146524341-0ef447fe-278b-4927-bdad-ae5d4f4f8643.png)

8. Validez, publiez et exécutez le pipeline.
9. Vérifiez que le fichier de sortie est bien unique et associe à chaque passage, un identifiant technique de compteur

## Pour l'or!
Avec ce que vous avez appris
1. Modifiez votre dataflow pour prendre les données de **silver** et effectuer une moyenne des distances par rapport au centre de Paris (colonne *Distance centre de Paris*) par compteur.
2. Ecrire le résultat dans **gold**
