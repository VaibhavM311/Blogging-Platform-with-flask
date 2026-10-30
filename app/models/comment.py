from datetime import datetime, timezone
from app import db

class Comment(db.Model):
    """A comment made by an authenticated user on a blog post."""
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    author = db.relationship("User", backref=db.backref("comments", lazy="dynamic", cascade="all, delete-orphan"))
    post = db.relationship("Post", backref=db.backref("comments", lazy="dynamic", cascade="all, delete-orphan"))
    def __repr__(self):
        return f"<Comment {self.id} on post {self.post_id}>"
