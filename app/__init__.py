import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config

# Initialize extensions (unbound to any specific app instance)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Configure Flask-Login defaults
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

def create_app(config_name='default'):
    """Application Factory function that constructs and configures the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Ensure the instance directory exists for SQLite database storage
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize extensions with the application instance
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register Blueprints
    from app.main.routes import main_bp
    from app.auth.routes import auth_bp
    from app.posts.routes import posts_bp
    from app.errors.handlers import errors_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(errors_bp)

    # Import models to ensure user_loader and database schemas are registered
    from app import models

    return app
