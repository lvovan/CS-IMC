# TD Containers et CI/CD
Ce TD est volontairement peu documenté et n'est pas un tutoriel pas-à-pas comme le fut le TP. L'objectif ici est de vous guider afin que vous puissiez créer un web service containerisé en Python, déployable grâce à du CI/CD ("1-click") depuis GitHub.

Il est conseillé de travailler en binôme.

## 1. Création d'un repo github
1. Créer un repository GitHub pour votre TD
2. Cloner ce repo avec un dossier local de votre poste de travail

## 2. Création d'une application Flask
Vous allez maintenant créer une application Flask exposant un web service en Python.

1. Créer un environnement virtuel Python
2. Créer `requirements.txt` avec le contenu suivant
   ```
   Flask==2.2.2
   gunicorn
   Werkzeug==2.2.2
   Flask-RESTful
   ```
3. Créer `app.py` et y implémenter un web service en Flask
4. Tester votre service web en local
5. Poussez votre code sur votre repo

## 3. Containerisation
Vous allez maintenant containeriser votre application avec Docker.

Le fichier `Dockerfile` choisi vous permettra ensuite de déployer l'application sur [Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/overview), un service PaaS d'hébergement applicatif.

1. Containeriser l'application en s'appuyant sur [cette documentation](https://learn.microsoft.com/en-us/azure/developer/python/tutorial-containerize-simple-web-app?tabs=web-app-flask#add-dockerfile-and-dockerignore-files).
2. Tester l'application dockerisée en local
3. Poussez votre code sur votre repo

## 4. Création d'une ressource Container App

1. Depuis le [portail Azure](https://portal.azure.com), créer un resource group préfixé de vos noms (ex: `dupont-duponne-rg`)
2. Démarrer la console Azure (en haut à droite)
3. Cloner votre repo dans la console Azure ([Création d'un PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens))
4. Déployez l'application en suivant [ces instructions](https://learn.microsoft.com/en-us/azure/developer/python/tutorial-containerize-simple-web-app?tabs=web-app-flask#deploy-web-app-to-azure). Nommer votre ressource avec vos noms pour la rendre unique (ex: `jean-jeanne-aca`).
Il se peut qu'une erreur apparaisse concernant l'ACR (Azure Container Registry) - si cela arrive attendez deux ou trois minutes et recommencez
5. Tester votre application (vous n'aurez pas besoin d'ajouter `:5000` à l'URL)

## 5. Déploiement depuis GitHub
1. Retourner sur votre repo [GitHub](https://www.github.com)
2. Créer votre workflow à partir de cette [action](https://github.com/Azure/container-apps-deploy-action?tab=readme-ov-file#minimal---build-application-image-for-container-app) qui sera déclenchée lors d'un *push* et qui effectuera le build et le déploiement de l'application dans la Container App créée dans la section 4.
3. Modifier votre application pour qu'elle accepte un paramètre dans sa route (ex: `@app.route('/hello/<name>', methods=['GET'])`)
4. Bravo!
