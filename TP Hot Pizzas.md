# Travaux Pratiques Hot Pizzas
## *My customers deserve hot pizzas!!!*
![image](https://user-images.githubusercontent.com/20154628/145547104-43a2d9b7-1754-409b-8bbf-2060ee0f127e.png)  

![image](https://user-images.githubusercontent.com/20154628/145550769-ad5c56e9-bbc5-459f-9ed4-d00260ec4125.png)  

![image](https://user-images.githubusercontent.com/20154628/145551450-e5af6b3d-9412-407b-827c-3129783dbded.png)

![image](https://user-images.githubusercontent.com/20154628/145551474-327f4179-658d-4638-aac8-5b24d1415b0f.png)
  
## 1- Création de l'Injecteur d'évènements

1. Créer un service [Azure Event Hubs](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-features) ([instructions](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-create))
2. Créer une [Azure Logic Apps](https://docs.microsoft.com/en-us/azure/logic-apps/logic-apps-overview) en mode **Consommation** pour injecter des évènements dans l'Event Hubs créé précédemment ([instructions](https://docs.microsoft.com/en-us/azure/logic-apps/quickstart-create-first-logic-app-workflow))
3. Commencer le workflow Logic Apps avec un *Step* de type *Recurrence* (définir la fréquence)
4. Utiliser un Step de type *Send Event*
5. Utiliser la fonction random (*rand*) dans le JSON pour faire varier les valeurs...
<br />

Exemple d'évènement au format JSON:  
```
{  
     "DeviceId": "dev01",  
     "Speed": 40,  
     "Temperature": 70  
}
```
<br /><br />
On doit arriver à quelque chose comme ça :
<br />
![image](https://user-images.githubusercontent.com/20154628/145559457-300e909f-ac61-47af-9f91-a866d3191426.png)
<br />

## 2- Création du Consommateur d'évènements

1. Créer une autre Azure Logic Apps
2. Commencer le workflow par un Step de type trigger *When events are available in Event Hub*
3. Utiliser un Step de type *Parse JSON* pour "récupérer" les data dans des variables (Use sample payload to generate schema!)
4. Utiliser un Step de type *Condition* pour tester la température (<50 par exemple)
5. Utiliser un Step de type *Send an email* pour envoyer un message au client si la température n'est pas ok!
<br /><br />

On doit arriver à quelque chose comme ça :
<br />
![image](https://user-images.githubusercontent.com/20154628/145561491-daebde95-945d-4476-8139-d76c4f36e399.png)
<br />


