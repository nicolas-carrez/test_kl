Durée indicative : 2h30  

L’objectif de ce test est de monter une API Dockerisée capable de :
- Enregistrer une adresse
- Consulter les risques associés

> Note : Le temps est indicatif. La qualité du code (lisibilité, structure, gestion des erreurs) prime sur la quantité.
> 

---

## 1. Choix de la stack

Vous pouvez choisir entre :

- **NestJS (TypeScript)**
    - CLI & documentation : https://docs.nestjs.com/cli/overview
    - ORM SQLite (TypeORM) : https://typeorm.io/#/
- **Django (Python 3.12)**
    - Guide de démarrage : https://docs.djangoproject.com/fr/4.2/intro/tutorial01/
    - Base SQLite (réglage `DATABASES`) : https://docs.djangoproject.com/fr/4.2/ref/settings/#databases

Ressources : Vous pouvez utiliser ChatGPT ou toute autre ressource pour vous aider.

> Note : Le choix entre NestJS et Django est libre, sans pénalité.
> 

---

## 2. Endpoints  implémenter

### 2.1 `POST /api/addresses/`

### Payload

```json
{ "q": "chaîne de recherche d'adresse" }

```

### Validation

- Le champ `"q"` doit être une chaîne de caractères non vide.
- Si le payload est invalide, retourner HTTP 400 :
    
    ```json
    {
      "error": "Le champ 'q' est requis et doit être une chaîne non vide."
    }
    
    ```
    

### Comportement

1. Appeler l'API Adresse (BAN)
    - Exemple : `GET https://api-adresse.data.gouv.fr/search/?q=8+bd+du+port&limit=1`
2. Si au moins un résultat :
    - Persister en SQLite (table `addresses` avec champs :
        
        `id`, `label`, `housenumber`, `street`, `postcode`, `citycode`, `latitude`, `longitude`)
        
    - Retourner l'objet stocké (HTTP 200 + JSON)
3. Sinon : répondre HTTP 404 sans corps
4. En cas d'erreur lors de l'appel externe ou de la connexion DB : HTTP 500
    
    ```json
    {
      "error": "Erreur serveur : impossible de contacter l'API externe."
    }
    
    ```
    

### **Format de sortie attendu**

| Code HTTP | Corps de réponse |
| --- | --- |
| **200 OK** | `{
  "id": 1,
  "label": "8 bd du Port, 56170 Sarzeau",
  "housenumber": "8",
  "street": "bd du Port",
  "postcode": "56170",
  "citycode": "56242",
  "latitude": 47.58234,
  "longitude": -2.73745
}` |
| **400 Bad Request** | `{
  "error": "Le champ 'q' est requis et doit être une chaîne non vide."
}` |
| **404 Not Found** | `{
"error": "Adresse non trouvée. Aucun résultat ne correspond à votre recherche."
}` |
| **500 Internal Server Error** | `{
  "error": "Erreur serveur : impossible de contacter l'API externe."
}` |

---

### 2.2 `GET /api/addresses/{id}/risks/`

### Paramètre

- `id` de l'adresse en base

### Comportement

1. Lire l'enregistrement (`latitude`/`longitude` ou `citycode`)
2. Appeler l'API Géorisques
    - Exemple : `GET https://georisques.gouv.fr/api/v1/resultats_rapport_risque?latlon={lon},{lat}`
3. Retourner intégralement le JSON de réponse (HTTP 200)
4. Gestion des erreurs :
    - Si l'adresse n'existe pas → HTTP 404
        
        ```json
        {
          "error": "Adresse non trouvée."
        }
        
        ```
        
    - Si erreur appel externe → HTTP 500
        
        ```json
        {
          "error": "Erreur serveur : échec de la récupération des données de Géorisques."
        }
        
        ```
        

### **Format de sortie attendu**

| Code HTTP | Corps de réponse |
| --- | --- |
| **200 OK** | `json<br>{ …JSON complet de Géorisques… }` |
| **404 Not Found** | `json<br>{<br>  "error": "Adresse non trouvée."<br>}` |
| **500 Internal Server Error** | `json<br>{<br>  "error": "Erreur serveur : échec de la récupération des données de Géorisques."<br>}` |

---

## 3. Docker & orchestration

- Conteneur unique exposant le port **8000**
- Base SQLite en volume pour persister les données
- Fichier `docker-compose.yml` permettant le `build` et le `up` en une seule commande

---

## 4. Documentation et démarrage

Dans un `README.md`, indiquez :

1. **Commandes nécéssaire au lancement du docker compose**
    
    ```bash
    docker compose build
    docker compose up
    
    ```
    
2. **Variables d'environnement**
    - NestJS/TypeORM :
        
        ```
        TYPEORM_CONNECTION=sqlite
        TYPEORM_DATABASE=/data/db.sqlite
        
        ```
        
    - Django :
        
        ```
        DATABASE_URL=sqlite:////data/db.sqlite
        
        ```
        
3. **URL des endpoints** et exemples de requêtes/réponses (voir section Formats de sortie).

---

## 5. Bonnes pratiques

- **Tests unitaires :** Au moins un test simple (Jest ou pytest)
- **Sécurité (facultatif) :** Gestion des clés API, timeouts, etc.

---

## 6. Format de rendu – dépôt Git clonable

Le livrable attendu est un **dépôt Git public** (GitHub, GitLab ou autre) contenant :

- Le code source de l'application
- Le fichier `docker-compose.yml`
- Un `README.md` clair avec :
    - Instructions de lancement du projet
    - Description des endpoints et formats de réponse
    - Variables d'environnement nécessaires
- Optionnel : un fichier `.env.example` pour faciliter le démarrage
- Les tests unitaires (dans un dossier `tests/` ou `__tests__/`)
- Toute documentation additionnelle utile à la compréhension

> ⚠️ Merci de vérifier que le dépôt est clonable sans authentification et que toutes les instructions de démarrage fonctionnent directement.
> 

Une fois terminé, merci d'envoyer **le lien vers le dépôt Git** à l'adresse suivante : contact@klaire.cc

Bonne mise en œuvre,

L'équipe technique Klaire
