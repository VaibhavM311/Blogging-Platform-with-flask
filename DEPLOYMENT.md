# Deployment (Gunicorn and Docker)

## Gunicorn (Linux/macOS)
1. Install dependencies: `pip install -r requirements.txt`
2. Set a strong secret: `export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"`
3. Set production mode: `export FLASK_CONFIG=production`
4. Apply migrations: `flask --app run.py db upgrade`
5. Start: `gunicorn --bind 0.0.0.0:8000 --workers 2 --threads 4 run:app`

On Windows, use Docker Desktop or run Gunicorn in WSL/Linux; Gunicorn is not natively supported on Windows.

## Docker
1. Create a strong `SECRET_KEY` environment variable.
2. Run: `docker compose up --build`
3. Open `http://localhost:8000`.

The SQLite database is stored in the persistent `blog_data` Docker volume. For production at scale, use PostgreSQL and configure backups, HTTPS, secure cookies, and a managed secret.
