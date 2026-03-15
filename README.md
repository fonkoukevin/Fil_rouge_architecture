# Fil_rouge_architecture
Plumora API

Backend API pour une plateforme d’édition numérique permettant aux auteurs de soumettre des manuscrits, aux éditeurs de les évaluer et de publier les œuvres validées.

Le projet met en œuvre une architecture inspirée de Clean Architecture et DDD, avec des design patterns, des tests unitaires, une CI GitHub Actions, et une base de données conteneurisée avec Docker. 

Description fonctionnelle

Plumora simule une plateforme éditoriale où plusieurs acteurs interviennent :

Auteurs

créent des manuscrits

ajoutent des chapitres

créent des versions

soumettent leur manuscrit à l’édition

Éditeurs

prennent en charge les manuscrits soumis

demandent des corrections

acceptent ou rejettent les manuscrits

Publication

Lorsqu’un manuscrit est accepté, il peut être publié sous forme de livre dans le catalogue.

Notifications

Les utilisateurs reçoivent des notifications lors d’événements importants :

soumission

changement de statut

publication

Description technique

Le projet est développé avec :

Python 3.13

FastAPI

SQLAlchemy Async

MySQL

Alembic (migrations)

Docker

uv (gestionnaire Python)

pytest

GitHub Actions (CI)

Le développement est réalisé sous WSL (Windows Subsystem for Linux).

Architecture du projet

Le projet utilise une architecture inspirée de Clean Architecture / DDD (Domain Driven Design).

Structure principale :

app/
 ├── domain/
 │   ├── entities/
 │   ├── services/
 │   ├── repositories/
 │   └── ports/
 │
 ├── application/
 │   └── use_cases/
 │
 ├── infrastructure/
 │   ├── repositories/
 │   ├── security/
 │   └── database
 │
 └── presentation/
     ├── controllers
     └── schemas

Design Patterns utilisés

Le projet implémente plusieurs design patterns.

1️⃣ State Pattern

Utilisé pour gérer les transitions d’état du manuscrit.

Fichier:
domain/services/manuscript_state.py
Cela garantit que les transitions d’état sont valides et contrôlées.

2️⃣ Builder Pattern

Utilisé pour construire un Book à partir d’un manuscrit accepté.

Fichier :

domain/entities/book_builder.py

Le builder assemble les différentes informations :

titre

synopsis

auteur

slug

contenu

Cela permet de séparer la construction complexe d’un objet métier.

3️⃣ Adapter Pattern

Utilisé pour la gestion des notifications.

Interface :

domain/ports/notification_port.py

Base de données

Le projet utilise MySQL via Docker.

Le conteneur est défini dans docker-compose.yml

phpMyAdmin

Interface disponible sur :

http://localhost:8081

Conteneurisation

Le projet est semi-conteneurisé.

Docker est utilisé pour :

MySQL

phpMyAdmin

L’application Python est exécutée localement via uv.

Installation du projet

Cloner le projet :

git clone <repo>
cd Fil_rouge_architecture


Installer les dépendances :

uv sync

Lancer la base de données
docker compose up -d

Migrations
uv run alembic upgrade head

Lancer l’API
uv run uvicorn app.main:app --reload


API disponible sur :

http://127.0.0.1:8000


Documentation :

http://127.0.0.1:8000/docs

ests

Le projet contient des tests unitaires utilisant :

pytest
pytest-asyncio
pytest-cov


Exécution :

uv run pytest


Couverture :

uv run pytest --cov=app


Couverture actuelle : 32%

Pipeline CI

Un pipeline GitHub Actions exécute automatiquement les tests.

Fichier :

.github/workflows/tests.yml


Déclenché sur :
push
pull_request

Routes API
Auth
POST /auth/register
POST /auth/login
GET  /auth/me

Manuscrits
POST /manuscrits
GET  /manuscrits
PUT  /manuscrits/{id}

Workflow éditorial
POST /editorial/manuscrits/{id}/soumettre
POST /editorial/dossiers/{id}/start-review
POST /editorial/dossiers/{id}/request-changes
POST /editorial/dossiers/{id}/accept
POST /editorial/dossiers/{id}/reject

Publication
POST /publications
GET  /livres/{id}
GET  /catalogue

Notifications
GET  /notifications
POST /notifications/{id}/lu