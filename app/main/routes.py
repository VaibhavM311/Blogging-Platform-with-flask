from flask import render_template
from app.main import main_bp
from app.models.post import Post

@main_bp.route('/')
@main_bp.route('/home')
def index():
    """Homepage route displaying recent published articles."""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('main/index.html', title='Home', posts=posts)

@main_bp.route('/about')
def about():
    """About page introducing the blog platform."""
    return render_template('main/about.html', title='About Us')
