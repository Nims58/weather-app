# WeatherApp

Django weather dashboard prepared for local development and Render deployment.

## Local setup

1. Create `.env` from `.env.example` and fill in your values.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run migrations and start the server:
   `python manage.py migrate`
   `python manage.py runserver`

## Render deployment

This repo includes `render.yaml` and `build.sh` for a Render Blueprint deployment.

Required Render environment variables:
- `SECRET_KEY` (generated automatically by `render.yaml`)
- `DATABASE_URL` (linked automatically to the Render Postgres database)
- `OPENWEATHERMAP_API_KEY` (set this manually in Render)

Optional environment variables:
- `OPENWEATHERMAP_DEFAULT_CITY`
- `OPENWEATHERMAP_DEFAULT_UNITS`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`

Render start command:
`python -m gunicorn WeatherApp.asgi:application -k uvicorn.workers.UvicornWorker`