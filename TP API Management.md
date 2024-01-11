# Travaux Pratiques API Management et Expérience Développeur
L'API Management permet, entre autres, de standardiser l'accès aux capacités SI de l'entreprise. En plus de cela, fournir une bonne expérience aux développeurs qui exploiteront votre API est également un point crucial: elle permet d'accélérer l'adoption tout en améliorant la productivité, et donc la rentabilité, des API mises à disposition.

Dans ce TP nous utiliserons [Azure API Management](https://azure.microsoft.com/fr-fr/services/api-management/) pour unifier l'accès à deux APIs: l'une hébergée sur Azure, l'autre sur AWS.

> ⚠️ Lancez dès maintenant la création d'une ressource **API Management en mode développeur** depuis le portail Azure, car la création peut prendre plusieurs minutes.

## 1. Test de l'API 'Fibonacci', hébergée en tant que serverless [Lambda](https://docs.aws.amazon.com/fr_fr/lambda/latest/dg/welcome.html) sur AWS
 - API calculant la [suite de Fibonacci](https://wvxyl5z85e.execute-api.eu-west-3.amazonaws.com/default/imc-fibo?value=20)

## 2. Implémentation votre propre API 'Lucas' serverless sur Azure
 - Implémentez une Azure Function implémentant le calcul de la [suite de Lucas](https://fr.wikipedia.org/wiki/Suite_de_Lucas), avec le langage de votre choix. Dans un premier temps, codez directement dans le navigateur.

## 3. Intégration à Azure API Management et transformation de la sortie
On souhaite créer une API de calcul unifiée en s'appuyant sur de l'API Management.
1. Intégrez-y les deux APIs testées précédemment. Observez que malgré le fait que les deux fonctions soient hébergées chez deux cloud providers distincts, qui plus est avec des technologies différentes, l'utilisation d'une couche d'API Management permet d'unifier leurs *endpoints*.
    1. Vous noterez que la fonction déjà hébergée dans Azure est plus facile à intégrer (il y a directement une option *Azure Function*): c'est un exemple de facilité d'intégration lorsque vous hébergez plusieurs ressources chez le même cloud provider
    2. Pour l'API hébergée chez AWS, vous utiliserez le connecteur *HTTP*
2. Certaines applications historiques ne supportant que le XML souhaitent utiliser les fonctions proposées. Utilisez la fonctionnalité *Test* pour requêter vos API en configurant l'entête `Accept` à `application/json` et `application/xml`. Observez que le résultat est toujours au format Json.
3. Configurez les policy de votre API Management afin de renvoyer du XML ou du Json en fonction de l'entête `Accept` utilisant la policy *Outbound* [json-to-xml](https://docs.microsoft.com/en-us/azure/api-management/api-management-transformation-policies#ConvertJSONtoXML) et testez.
4. Afin de pouvoir servir à la fois du XML ou du Json en fonction de l'appelant, reconfigurez la policy *Outbound* pour qu'elle renvoie le bon format de données en fonction du header http *accept*. Notez que cette policy permet à API Management d'automatiquement ajouter l'entête `content-type`, ce qui permet au client de connaître le format des données renvoyées par le service via un [MIME Type](https://developer.mozilla.org/en-US/docs/Glossary/MIME_type)
6. (Optionnel) Ajoutez une policy *inbound*, par exemple [Limit call rate by key](https://docs.microsoft.com/en-us/azure/api-management/api-management-access-restriction-policies#LimitCallRateByKey), qui limite le nombre d'appel par unité de temps.

## 4. Gestion des accès
Maintenant que les deux APIs sont réunies, créons un produit et ouvrons un compte développeur.
1. Ouvrez votre instance d'API Management
2. Dans *Users*, créez un utilisateur
3. Dans *Products*, créez un produit en lui associant les deux APIs Fibonacci et Lucas en n'oubliant pas de la publier en cochant l'élément adéquat.
4. Créez maintenant un abonnement en cliquant sur *Subscriptions*, associez-y le produit et l'utilisateur préalablement créés. 
5. Publiez le portail développeur (sans oublier d'activer CORS) et naviguez maintenant vers le portail développeur (je vous conseille d'utiliser le mode Privé/Incognito)
6. Autentifiez-vous avec l'utilisateur préalablement créé et testez vos APIs
7. (optionnel) Configurez deux niveaux d'abonnement, un niveau Standard avec uniquement l'API Fibonacci et un niveau Premium avec les API Fibonacci et Lucas.

## 5. (optionnel) Personnalisation du portail développeur
En vous connectant au portail développeur avec un compte administrateur de l'API Management, vous pourrez configurer l'apparence de ce dernier directement depuis votre navigateur.

## 6. (optionnel) Implémentez une API supplémentaire
Implémentez une nouvelle API, déployez là et intégrez la à API Management
