# English Learning

A personal English-learning web application with writing feedback, reading and vocabulary practice, and evidence-informed personalized recommendations.

## Current implementation status

The repository is being built incrementally. The first backend foundation provides a Django REST API and a health endpoint. Learning features and the frontend are not implemented yet.

## Requirements

- Python 3.11+
- Git

## Run locally (macOS)

```bash
git clone https://github.com/SoheilAbdollahii/english-learning.git
cd english-learning
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py test
python manage.py runserver
```

Open http://127.0.0.1:8000/api/health/ and expect JSON with `"status": "ok"`.

The default local database is SQLite to make first-run setup simple. PostgreSQL can be configured with `DATABASE_URL` for later environments.

## Configuration and security

- Never commit real secrets. Keep them in an ignored `.env` file or deployment environment variables.
- The default secret key is for local development only and must be replaced before deployment.
- `DEBUG` must be disabled and `ALLOWED_HOSTS` configured for deployment.
- The health endpoint is public and does not return user or database information.

## Quality gate

Deployment must wait until the project has been run and tested on the user's Mac, core flows have been manually verified, and important issues are resolved.
