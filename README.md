# DevBlog &mdash; Blogging Platform with Flask

A modular, production-ready blogging web application built with Python, Flask, SQLAlchemy, and Bootstrap 5.

---

## 🌟 Architecture Overview

The project uses the **Flask Application Factory Pattern** with **Blueprints**, separating features into dedicated, modular packages:

```
Blogging_Platform/
├── app/
│   ├── __init__.py           # Application Factory (create_app) & extensions
│   ├── models/               # SQLAlchemy ORM Models
│   │   ├── __init__.py
│   │   └── user.py           # User model & password hashing
│   ├── auth/                 # Authentication Blueprint
│   │   ├── forms.py          # Registration & Login WTForms
│   │   └── routes.py         # Login, Register, Logout routes
│   ├── main/                 # Main Blueprint (Index, About)
│   │   └── routes.py
│   ├── errors/               # Custom Error Handlers (404, 403, 500)
│   │   └── handlers.py
│   └── templates/            # Jinja2 Templates (Bootstrap 5)
├── migrations/               # Alembic database migrations
├── tests/                    # Automated Unit Tests
├── instance/                 # SQLite database storage (blog.db)
├── config.py                 # Multi-environment configurations
├── run.py                    # Entry-point runner
└── requirements.txt          # Python dependencies
```

---

## 🚀 Getting Started

### 1. Activate Virtual Environment (PowerShell)
```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Run Database Migrations
```powershell
flask db upgrade
```

### 3. Run the Development Server
```powershell
python run.py
```
Visit `http://127.0.0.1:5000` in your web browser.

### 4. Run Unit Tests
```powershell
python -m unittest discover tests
```
