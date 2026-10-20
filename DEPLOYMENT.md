# Deployment readiness checklist

This project is a development prototype. Do not treat a passing CI run as proof that it is production-ready: the writing endpoint is unauthenticated, has no rate limiting, and uses a small rule-based checker rather than a complete grammar service.

## Required backend environment

Configure these values in the hosting provider's secret/environment settings; do not commit real values:

- `DJANGO_DEBUG=False`
- `DJANGO_SECRET_KEY`: a unique, randomly generated secret. Generate one with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`.
- `DJANGO_ALLOWED_HOSTS`: comma-separated exact API hostnames, without schemes or paths. Do not use `*`.
- `CORS_ALLOWED_ORIGINS`: comma-separated exact frontend origins including `https://`, for example `https://learn.example.com`.
- `DATABASE_URL`: a managed PostgreSQL connection string for a persistent production database.

When `DJANGO_DEBUG=False`, startup now fails if the development-only secret key or a wildcard/empty allowed-host configuration is used. Session and CSRF cookies are marked secure in this mode.

## HTTPS, database, and static files

- Terminate TLS at the hosting platform and enforce HTTPS for the public frontend and API.
- Verify that Django correctly recognizes HTTPS behind the provider's reverse proxy before enabling any redirect/proxy settings. Do not blindly enable proxy trust headers without confirming the provider's configuration.
- Apply schema changes with `python manage.py migrate` as a controlled deployment step.
- Configure static-file serving for Django admin if the admin is exposed; this project does not currently include a dedicated static-file serving layer.
- Keep database backups and verify that the configured database is persistent.

## Frontend environment

Set `NEXT_PUBLIC_API_BASE_URL` to the public API base URL at build time, without the trailing `/api/writing/analyze/` path. For example, `https://api.example.com`. Rebuild the frontend after changing this public variable.

## Before public launch

- [ ] CI passes for the exact commit being released: backend checks/tests, frontend lint, and frontend production build.
- [ ] Run `python manage.py check --deploy` with production environment variables and review every warning.
- [ ] Confirm HTTPS, CORS, allowed hosts, database persistence, migrations, and static files in the target hosting environment.
- [ ] Manually test health and writing-analysis endpoints, including invalid JSON, empty text, and the 2,000-character limit.
- [ ] Add rate limiting and abuse protection before exposing the unauthenticated writing endpoint publicly.
- [ ] Review privacy/data-retention requirements before accepting real learner writing; avoid logging submitted text.
- [ ] Confirm the product clearly describes the checker as a limited rule-based prototype.

No deployment has been performed by this checklist alone; hosting provider, domain, secrets, and production database must be configured explicitly.
