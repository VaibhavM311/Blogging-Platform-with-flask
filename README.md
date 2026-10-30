# DevBlog &mdash; Blogging Platform with Flask

A modular, production-ready blogging web application built with Python, Flask, SQLAlchemy, Flask-Login, and Bootstrap 5.

---

## 🌟 Architecture Overview

The project uses the **Flask Application Factory Pattern** with **Blueprints**, separating features into dedicated, modular packages:

```text
Blogging_Platform/
├── app/
│   ├── __init__.py           # Application Factory (create_app) & extensions
│   ├── models/               # SQLAlchemy ORM Models
│   │   ├── __init__.py
│   │   ├── user.py           # User model, UserMixin & password hashing
│   │   └── post.py           # Post model, relational foreign keys & snippet property
│   ├── auth/                 # Authentication & Session Blueprint
│   │   ├── forms.py          # Registration, Login & Edit Profile WTForms
│   │   └── routes.py         # Login, Register, Logout, Profile routes
│   ├── posts/                # Blog Post CRUD Blueprint
│   │   ├── forms.py          # PostForm with validation
│   │   └── routes.py         # Create, read, edit, delete & user post routes
│   ├── main/                 # Main Blueprint (Index Feed, About)
│   │   └── routes.py
│   ├── errors/               # Custom Error Handlers (404, 403, 500)
│   │   └── handlers.py
│   └── templates/            # Jinja2 Templates (Bootstrap 5)
│       ├── auth/             # login.html, register.html, profile.html, edit_profile.html
│       ├── posts/            # create_post.html, edit_post.html, post_detail.html, user_posts.html
│       ├── errors/           # 404.html, 403.html, 500.html
│       ├── main/             # index.html, about.html
│       └── base.html         # Master responsive layout & navbar
├── migrations/               # Alembic database migrations
├── tests/                    # Automated Unit Tests (18 test cases)
│   ├── test_basics.py
│   ├── test_auth.py
│   └── test_posts.py
├── instance/                 # SQLite database storage (blog.db)
├── config.py                 # Multi-environment configurations
├── run.py                    # Entry-point runner
└── requirements.txt          # Python dependencies
```

---

## 📅 Weekly Milestones & Implementation Progress

### Week 1: Environment, Modular Blueprints & Database Migrations
- Virtual environment setup with dependencies (`requirements.txt`).
- Application Factory pattern (`create_app`) in `app/__init__.py`.
- Blueprints configuration: `main`, `auth`, `errors`.
- SQLite database configured via `Flask-SQLAlchemy` and Alembic migrations via `Flask-Migrate`.
- Master layout with Bootstrap 5 CDN and custom 404/500 error handlers.

### Week 2: User Models, Authentication & Session Management (Flask-Login)
- **User Model (`app/models/user.py`)**: Inherits from `db.Model` and `flask_login.UserMixin` with secure salted password hashing (`werkzeug.security`).
- **Session Management (`Flask-Login`)**:
  - Registered `@login_manager.user_loader` (`load_user`) to reload the user from the active session.
  - Route protection using `@login_required` decorator (unauthenticated requests safely redirect to login with a friendly notice).
  - Session persistence with "Remember Me" cookies.
  - Safe redirect protection against open redirect attacks using URL validation.
- **Forms & Validation (`Flask-WTF`)**:
  - `RegistrationForm`: username length, valid email syntax, matching passwords, duplicate username/email checks.
  - `LoginForm`: email & password validation, remember me checkbox.
  - `EditProfileForm`: dynamic duplicate validation ensuring updated username/email is not taken by another user.
- **User Profile Management**:
  - Protected `/auth/profile` route displaying account status, member since date, and bio.
  - Protected `/auth/edit-profile` route allowing users to customize their profile and author bio.
- **Automated Tests (`tests/test_auth.py`)**:
  - 100% test coverage for password hashing, registration, login/logout, route protection, and profile updates.

### Week 3: Post Management (CRUD), Author Relationships & Permissions
- **Post Model (`app/models/post.py`)**:
  - Relational mapping with `User` (`One-to-Many` via `author_id` foreign key and cascade deletion).
  - Content snippet helper property for feed previews.
  - Automated timestamps for creation and `updated_at` modification tracking.
- **Post Blueprint & CRUD Routes (`app/posts/routes.py`)**:
  - `GET /posts/create` & `POST /posts/create`: Protected post authoring with WTForms validation.
  - `GET /posts/<int:post_id>`: Dedicated article reading view.
  - `GET /posts/<int:post_id>/edit` & `POST /posts/<int:post_id>/edit`: Secure editing with strict author verification (`403 Forbidden` for non-authors).
  - `POST /posts/<int:post_id>/delete`: Secure deletion with Bootstrap confirmation modal.
  - `GET /posts/user/<string:username>`: Author portfolio page displaying all articles by a specific user.
- **Dynamic Homepage Feed**:
  - Real-time display of recent articles ordered newest-first with author badges, publication dates, and snippets.
- **Automated Tests (`tests/test_posts.py`)**:
  - Complete test coverage for post creation, reading, editing, deletion, unauthorized 403 blocks, 404 handling, and user filters.

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
*(All 18 tests passing with 100% success rate!)*
