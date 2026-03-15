# 📚 Plumora API

Backend API pour une plateforme d’édition numérique permettant aux **auteurs** de soumettre des manuscrits, aux **éditeurs** de les évaluer et de publier les œuvres validées.

Le projet met en œuvre une architecture inspirée de **Clean Architecture** et **DDD (Domain Driven Design)**, avec des design patterns, des tests unitaires, une CI GitHub Actions, et une base de données conteneurisée avec Docker.

---

# 📖 Description fonctionnelle

Plumora simule une **plateforme éditoriale** où plusieurs acteurs interviennent.

## ✍️ Auteurs

Les auteurs peuvent :

- créer des manuscrits
- ajouter des chapitres
- créer des versions
- soumettre leur manuscrit à l’édition

## 📝 Éditeurs

Les éditeurs peuvent :

- prendre en charge les manuscrits soumis
- demander des corrections
- accepter ou rejeter les manuscrits

## 📚 Publication

Lorsqu’un manuscrit est accepté, il peut être publié sous forme de **livre dans le catalogue**.

## 🔔 Notifications

Les utilisateurs reçoivent des notifications lors d’événements importants :

- soumission
- changement de statut
- publication

---

# ⚙️ Description technique

Le projet est développé avec :

- **Python 3.13**
- **FastAPI**
- **SQLAlchemy Async**
- **MySQL**
- **Alembic**
- **Docker**
- **uv (gestionnaire Python)**
- **pytest**
- **GitHub Actions (CI)**

Le développement est réalisé sous **WSL (Windows Subsystem for Linux)**.

---

# 🏗 Architecture du projet

Le projet est conçu selon les principes de **Clean Architecture** et **Domain Driven Design (DDD)**.

app/
├── domain/
│ ├── entities/
│ ├── services/
│ ├── repositories/
│ └── ports/
│
├── application/
│ └── use_cases/
│
├── infrastructure/
│ ├── repositories/
│ ├── security/
│ └── database
│
└── presentation/
├── controllers
└── schemas


Cette structure permet :

- une séparation claire des responsabilités
- un domaine métier indépendant des frameworks
- une architecture maintenable et testable

---

#  Modélisation de l’architecture (C4 Model)

Le projet est modélisé à l’aide du **modèle C4**, qui permet de représenter l’architecture logicielle à plusieurs niveaux.

## 1️⃣ Diagramme de contexte (C4 - Level 1)

Ce diagramme montre les **acteurs principaux et leurs interactions avec le système Plumora**.

*(Ajouter l’image du diagramme C4 Contexte)*

![C4 Context Diagram](docs/c4-context.png)

---

## 2️⃣ Diagramme de conteneurs (C4 - Level 2)

Ce diagramme décrit les **principaux conteneurs techniques du système**, comme l’API, la base de données et les services.

*(Ajouter l’image du diagramme C4 Container)*

![C4 Container Diagram](docs/c4-container.png)

---

## 3️⃣ Diagramme de composants (C4 - Level 3)

Ce diagramme présente les **composants internes de l’API**, notamment les couches :

- domain
- application
- infrastructure
- presentation

*(Ajouter l’image du diagramme C4 Component)*

![C4 Component Diagram](docs/c4-component.png)

---

#  Domain Driven Design (DDD)

Le projet est structuré selon les principes du **Domain Driven Design**.

Le **domaine métier** est clairement identifié et modélisé à travers :

- **Bounded Contexts**
- **Entities**
- **Value Objects**
- **Domain Services**
- **Aggregates**

## Bounded Context

Un diagramme de **bounded context** a été réalisé afin de représenter les différentes parties du domaine métier.

*(Ajouter l’image du diagramme Bounded Context)*

![Bounded Context Diagram](docs/bounded-context.png)

---

## Modélisation du domaine

Un diagramme DDD permet de représenter les principaux éléments du domaine :

- Manuscript
- Chapter
- Version
- Book
- User
- Notification

*(Ajouter l’image du diagramme DDD)*

![DDD Diagram](docs/ddd-diagram.png)

---

#  Design Patterns utilisés

## 1️⃣ State Pattern

Utilisé pour gérer les **transitions d’état du manuscrit**.

Fichier :

domain/services/manuscript_state.py


Cela garantit que les transitions d’état sont **valides et contrôlées**.

---

## 2️⃣ Builder Pattern

Utilisé pour construire un **Book** à partir d’un manuscrit accepté.

Fichier :

domain/entities/book_builder.py


Le builder assemble :

- titre
- synopsis
- auteur
- slug
- contenu

---

## 3️⃣ Adapter Pattern

Utilisé pour la **gestion des notifications**.

Interface :

domain/ports/notification_port.py


---

# 🗄 Base de données

Le projet utilise **MySQL via Docker**.

Le conteneur est défini dans :

docker-compose.yml


### phpMyAdmin

Interface disponible sur :

http://localhost:8081


---

#  Installation du projet

## 1️⃣ Cloner le projet

```bash
git clone <repo>
cd Fil_rouge_architecture

2️⃣ Installer les dépendances

uv sync

3️⃣ Lancer la base de données

docker compose up -d

4️⃣ Appliquer les migrations

uv run alembic upgrade head

5️⃣ Lancer l’API

uv run uvicorn app.main:app --reload

 Accès à l'API

API :

http://127.0.0.1:8000

Documentation Swagger :

http://127.0.0.1:8000/docs

 Tests

Tests réalisés avec :

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