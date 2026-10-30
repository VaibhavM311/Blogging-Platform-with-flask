from datetime import datetime, timezone
from app import db

class Post(db.Model):
    """Post model representing a blog article created by a user."""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Foreign key linking post to the author user
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True, index=True)
    tags = db.relationship('Tag', secondary='post_tags', backref=db.backref('posts', lazy='dynamic'))

    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    @property
    def snippet(self):
        """Returns a trimmed summary of the post for feed previews."""
        plain = self.content.strip()
        if len(plain) > 180:
            return plain[:177] + '...'
        return plain

    def __repr__(self):
        return f'<Post {self.title[:30]}>'
