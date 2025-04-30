# Klaire Application

Cette application Django permet de gérer des adresses et d'obtenir des informations sur les risques associés.

## Prérequis

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Installation et utilisation

### 1. Cloner le dépôt

Clonez le dépôt sur votre machine locale :

```bash
git clone git@github.com:nicolas-carrez/test_kl.git
cd klaire
```

### 2. Construire et démarrer les conteneurs

Utilisez Docker Compose pour construire et démarrer les conteneurs :

```bash
docker-compose up --build
```

Cela va :
- Construire l'image Docker pour l'application Django.
- Démarrer les services définis dans `docker-compose.yml`.

### 3. Accéder à l'application

Une fois le conteneur démarré, vous pouvez communiquer avec l'application de la manière suivante :

#### Endpoint 1 : Ajouter une adresse

**Requête :**
```bash
curl -X POST http://127.0.0.1:8000/api/addresses/ -H "Content-Type: application/json" -d '{"q": "7 residence vaucouleur, 91940, Les Ulis"}'
```

**Réponse réussie (200) :**
```json
{
  "id": 1,
  "label": "7 Residence Vaucouleur, 91940 Les Ulis",
  "name": "7 Residence Vaucouleur",
  "postcode": "91940",
  "citycode": "91345",
  "latitude": 48.6829,
  "longitude": 2.1694
}
```

**Réponse en cas d'erreur (400) :**
```json
{
  "error": "Le champ 'q' est requis et doit être une chaîne non vide."
}
```

**Réponse en cas d'absence de résultats (404) :**
```json
{
  "error": "Adresse non trouvée. Aucun résultat ne correspond à votre recherche."
}
```

**Réponse en cas d'erreur serveur (500) :**
```json
{
  "error": "Erreur serveur : impossible de contacter l'API externe."
}
```

#### Endpoint 2 : Obtenir les risques associés à une adresse

**Requête :**
```bash
curl -X GET http://127.0.0.1:8000/api/addresses/{id}/risks/
```

**Réponse réussie (200) :**
```json
{
  "risks": {
    "flood": "low",
    "earthquake": "moderate",
    "pollution": "high"
  }
}
```

**Réponse en cas d'adresse inexistante (404) :**
```json
{
  "error": "Adresse non trouvée."
}
```

**Réponse en cas d'erreur serveur (500) :**
```json
{
  "error": "Erreur serveur : échec de la récupération des données de Géorisques."
}
```

### 4. Exécuter les tests

Pour exécuter les tests unitaires, utilisez la commande suivante :

```bash
docker-compose run web python manage.py test
```

### 5. Arrêter les conteneurs

Pour arrêter les conteneurs, utilisez :

```bash
docker-compose down
```

## Migrations de base de données

Avant de démarrer l'application pour la première fois, vous devez appliquer les migrations de base de données. Voici les étapes :

### 1. Créer les fichiers de migration

Si vous avez ajouté ou modifié des modèles, générez les fichiers de migration avec la commande suivante :

```bash
docker-compose run web python manage.py makemigrations
```

### 2. Appliquer les migrations

Appliquez les migrations à la base de données avec la commande suivante :

```bash
docker-compose run web python manage.py migrate
```

Cela mettra à jour la base de données PostgreSQL avec les schémas nécessaires.

### 3. Vérifier les migrations

Pour vérifier l'état des migrations, utilisez :

```bash
docker-compose run web python manage.py showmigrations
```

Cette commande affichera la liste des migrations et leur état (appliqué ou non).

## Structure des fichiers

- `docker-compose.yml` : Définit les services Docker (application Django et base de données PostgreSQL).
- `Dockerfile` : Définit l'image Docker pour l'application Django.
- `requirements.txt` : Liste des dépendances Python nécessaires.
- `klaire/` : Répertoire contenant le code source du serveur Django.
- `addresses/` : Répertoire contenant le code source de l'application addresses.

## Dépannage

- Si vous rencontrez des problèmes avec les dépendances Python, assurez-vous que le fichier `requirements.txt` est à jour.
- Si le conteneur ne démarre pas, vérifiez les logs avec :

```bash
docker-compose logs
```