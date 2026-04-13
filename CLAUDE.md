# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate

# Development
python manage.py runserver        # Start dev server at http://localhost:8000
python manage.py makemigrations   # Create migrations after model changes
python manage.py migrate          # Apply migrations

# **Testing**
python manage.py test                          # Run all tests
python manage.py test app_join                 # Run tests for a single app
python manage.py test app_join.tests.TestName  # Run a single test class

# Linting (djlint is available for Django templates)
djlint .
```

## Architecture

Two Django apps with REST API via Django REST Framework:

- **`app_join`** — Task management: `Task`, `Contact`, `SubTask` models. Tasks have a ManyToMany relation to Contacts (assignedTo) and a one-to-many to SubTasks (CASCADE delete). TaskSerializer nests SubTasks and Contacts in responses using custom `create()`/`update()` methods.

- **`app_user_auth`** — Authentication: `UserProfile` (OneToOne with Django's `User`) auto-created via `post_save` signal. Login is email-based (custom `EmailAuthTokenSerializer`). Registration auto-generates a username from `display_name`.

**URL namespace:** all endpoints under `/api/v1/`. Auth endpoints under `/api/v1/auth/`.

**Auth pattern:** DRF `TokenAuthentication`. Token returned on register (`POST /api/v1/auth/register/`) and login (`POST /api/v1/auth/login/`). Default permission class is `AllowAny` — per-view restrictions are commented out and need to be enabled for production.

**ViewSet pattern:** All CRUD endpoints use `viewsets.ModelViewSet` registered via `DefaultRouter`. Custom logic lives in serializers, not views.

## Key Settings

- Database: SQLite3 (`db.sqlite3`)
- `CORS_ALLOW_ALL_ORIGINS = True` — permissive for local frontend development (e.g., Live Server on port 5500)
- `DEBUG = True`, insecure `SECRET_KEY` — development only, not production-ready
- `REST_FRAMEWORK` default auth: `TokenAuthentication`; default permission: `AllowAny`
