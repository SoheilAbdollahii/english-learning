# English Learning

A personal English-learning web application with writing feedback, reading and vocabulary practice, and evidence-informed personalized recommendations.

## Current implementation

- Django REST API with health and rule-based writing-analysis endpoints.
- Next.js + TypeScript bilingual (Persian/English) writing-practice interface.
- The writing checker currently recognizes only a few patterns; it is a prototype, not a full grammar checker or AI model.

## Requirements

- Python 3.11+ and Git
- Node.js 20.9+ and npm

## Run locally on macOS

### 1. Backend (Terminal 1)

```bash
git clone --branch feature/backend-foundation https://github.com/SoheilAbdollahii/english-learning.git
cd english-learning
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver
```

The API runs at http://127.0.0.1:8000. Health check: http://127.0.0.1:8000/api/health/

### 2. Frontend (Terminal 2)

From the repository root:

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

Open http://localhost:3000. Keep the backend terminal running while using the writing checker. The frontend uses `NEXT_PUBLIC_API_BASE_URL` to find the API; its local default is `http://127.0.0.1:8000`.

The default local database is SQLite. PostgreSQL can be configured with `DATABASE_URL` for later environments.

## Configuration and security

- Never commit real secrets. `.env` and `.env.local` must stay local and must not contain public credentials.
- The default Django secret key is for local development only and must be replaced before deployment.
- `DEBUG` must be disabled and `ALLOWED_HOSTS` configured for deployment.
- The writing endpoint accepts unauthenticated text and is a development prototype; do not send sensitive writing.
- The health endpoint is public and does not return user or database information.

## Quality gate

Deployment must wait until the project has been run and tested locally, the main user journeys have been manually verified, and important issues are resolved.
