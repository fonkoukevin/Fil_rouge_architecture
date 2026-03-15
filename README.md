
---

# 🐳 Conteneurisation

Docker est utilisé pour :

- MySQL
- phpMyAdmin

L’application Python est exécutée localement via **uv**.

---

# 🚀 Installation du projet

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

🌐 Accès à l'API

API :

http://127.0.0.1:8000

Documentation Swagger :

http://127.0.0.1:8000/docs

🧪 Tests

Le projet contient des tests unitaires utilisant :

    pytest

    pytest-asyncio

    pytest-cov

Exécution

uv run pytest

Couverture

uv run pytest --cov=app

Couverture actuelle : 32%
🔄 Pipeline CI

Un pipeline GitHub Actions exécute automatiquement les tests.

Fichier :

.github/workflows/tests.yml

Déclenché sur :

    push

    pull_request

📡 Routes API
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