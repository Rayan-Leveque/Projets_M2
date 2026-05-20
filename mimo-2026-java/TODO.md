# TODO - Mimo Library

## Blockers (fix first)

1. **Spring Boot version invalide** — `pom.xml` utilise `<version>4.0.5</version>` qui n'existe pas. Dernier stable : `3.4.x` (ex: `3.4.0`) ou `3.3.5`.
2. **Maven Wrapper cassé** — le répertoire `.mvn/wrapper` est absent, `./mvnw` ne fonctionne pas. Soit le régénérer (`mvn wrapper:wrapper`), soit utiliser un Maven local.

## Etat actuel (déjà bien avancé)

| Exigence | Statut |
|----------|--------|
| API REST Spring Boot | OK |
| 3 tables avec FK (`authors`, `publishers`, `books`) | OK |
| CRUD complet (3 ressources) | OK |
| Recherches (by author, category, ISBN, publishers-by-author) | OK |
| Règles métier basiques (doublons, suppression protégée, cascade) | OK |
| Tests unitaires (Mockito) sur les 3 services | OK |
| Persistance DB (H2) | OK |

## Améliorations possibles (avant les bonus)

- [ ] **Validation des entrées** — ajouter `@Valid`, `jakarta.validation.constraints`, etc. sur les `WriteRequest` et le controller.
- [ ] **Exception handler global** — un `@ControllerAdvice` pour renvoyer des JSON d'erreur propres au lieu de 500 ou silences.
- [ ] **OpenAPI / Swagger** — `springdoc-openapi` pour documenter les endpoints auto.
- [ ] **ISBN validation** — regex ou vérification de format dans le service/controller.
- [ ] **Tests d'intégration** — `@SpringBootTest` avec la vraie base H2 pour tester la stack complète (repo + service + controller).

## Bonus à implémenter (par priorité)

1. **Autre base de données** (recommandé : PostgreSQL ou MySQL)
   - Remplacer H2 par Postgres en local (Docker)
   - Adapter `application.yml` (driver, dialect, `ddl-auto: validate`)
   - Conserver `schema.sql`/`data.sql` OU migrer vers Flyway/Liquibase

2. **Tests unitaires complémentaires**
   - Tests des controllers (`MockMvc`)
   - Tests des repositories (`@DataJpaTest`)

3. **Spring AI**
   - Endpoint `/ai/summarize` ou `/ai/recommend` qui appelle un LLM (OpenAI, Ollama local, etc.)
   - Ex: résumer la biographie d'un auteur ou recommander un livre par catégorie

4. **Kafka**
   - Producer : émettre un événement `BookCreated` / `AuthorCreated` lors du POST
   - Consumer : logger ou alimenter une statistique (ex: compteur de livres par catégorie)
   - Nécessite un `docker-compose.yml` avec Zookeeper + Kafka

## Suggestion d'ordre de travail

1. Corriger le `pom.xml` (version Spring Boot) et le Maven Wrapper.
2. Vérifier que le projet compile et que les tests passent (`mvn test`).
3. Ajouter PostgreSQL (Docker + config) pour le bonus base de données.
4. Ajouter les tests d'intégration / controller.
5. Spring AI (si clé API ou Ollama disponible).
6. Kafka (si temps restant).

---
*Document généré le 2026-05-12 — ne pas commiter tel quel si inutile.*
