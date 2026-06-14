# Mimo Games — API REST

Application Spring Boot exposant une API REST CRUD sur un domaine de jeux vidéo
(jeux, studios, éditeurs). Les données sont persistées dans une base **MySQL**.

## Prérequis

- JDK 21
- Un serveur MySQL accessible sur `localhost:3306`

Par défaut, l'application se connecte avec l'utilisateur `root` et le mot de passe
`password`. La base `mimo_games` est créée automatiquement si elle n'existe pas, et
les tables sont (re)créées puis alimentées à chaque démarrage.

## Lancer l'application

```bash
./mvnw spring-boot:run
```

ou

```bash
./mvnw clean package
java -jar target/games-0.0.1-SNAPSHOT.jar
```

L'API est ensuite disponible sur http://localhost:8080.

## Configuration (si vos identifiants MySQL diffèrent)

Surchargez les valeurs par défaut via des variables d'environnement :

```bash
export MIMO_DB_URL="jdbc:mysql://localhost:3306/mimo_games?createDatabaseIfNotExist=true"
export MIMO_DB_USER="root"
export MIMO_DB_PASSWORD="password"
```

## Tests

Les tests unitaires ne nécessitent **aucune** base de données :

```bash
./mvnw test
```

## Exemples d'appels

```bash
# Lister tous les jeux
curl http://localhost:8080/games

# Rechercher les jeux d'un studio
curl "http://localhost:8080/games?studioName=Naughty Dog"

# Créer un jeu (le studio et l'éditeur doivent déjà exister)
curl -X POST http://localhost:8080/games \
  -H "Content-Type: application/json" \
  -d '{"code":"NEW-001","title":"Mon Jeu","studio":"Valve","publisherName":"Valve","genre":"Adventure"}'
```

Ressources exposées (CRUD complet) : `/games`, `/studios`, `/publishers`.
