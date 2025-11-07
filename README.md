# Django_alex_network
Django Backend App
# Django Alex Network

This is a **Django 5.2 project** scaffolded for development with **SQLite**, **PostgreSQL**, and **Redis** support.  
It also includes **Django Debug Toolbar** for development and is ready for Codespaces or local development.

---

## Features

- Django 5.2 backend  
- SQLite (default, development)  
- PostgreSQL (Docker-ready, production/dev)  
- Redis caching support  
- Debug Toolbar for development  
- Ready for Django REST Framework and APIs  
- Environment variable-based configuration

---

## Prerequisites

- Python 3.11+  
- pip  
- Git  
- Docker (if using Postgres + Redis)  
- Codespaces recommended for quick setup  

---

## Quick Start (SQLite)

```bash
# Clone repo
git clone https://github.com/ermiHageez/Django_alex_network.git
cd Django_alex_network

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
Open in browser: http://127.0.0.1:8000/

Using PostgreSQL + Redis (Docker)
bash
Copy code
# Start Docker containers
docker compose up -d

# Update .env with PostgreSQL credentials
DATABASE_URL=postgres://alex:alex123@db:5432/alexdb
REDIS_URL=redis://redis:6379/1

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver
Debug Toolbar
Enabled in development mode (DEBUG=True):

Shows queries, cache, templates, and more

Access via browser at http://127.0.0.1:8000/ with toolbar on the side

Environment Variables
Copy .env.example to .env and edit as needed:

ini
Copy code
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://127.0.0.1:6379/1
Git Workflow
bash
Copy code
# Create branch
git checkout -b feature/<name>

# Commit changes
git add .
git commit -m "Describe changes"

# Push
git push origin feature/<name>
Next Steps
Create your first app (accounts or api)

Build models, serializers, and REST endpoints

Add Celery for background tasks with Redis

Set up production deployment with Postgres + Redis

References
Django 5.2 Docs

Django Debug Toolbar

django-environ

Django REST Framework

yaml
Copy code

---

If you want, I can **also add a ready-to-go Docker + Postgres + Redis development README section** with commands that work straight in Codespaces — it will make your repo fully plug-and-play.  

Do you want me to do that next?
