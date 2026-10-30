from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    """User account model for authentication, authoring posts, and profile details."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    bio = db.Column(db.String(280), default='')
    profile_image = db.Column(db.String(120), default='default_avatar.png')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relational link: one user can author many posts (One-to-Many)
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hashes the user's password using Werkzeug's secure hashing."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Validates the password hash against the given plain text password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    """Callback function used by Flask-Login to reload user object from session ID."""
    return db.session.get(User, int(user_id))
