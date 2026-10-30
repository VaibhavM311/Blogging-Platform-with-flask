from flask import render_template, request
from app.main import main_bp
from app.models.post import Post

@main_bp.route('/')
@main_bp.route('/home')
def index():
    """Homepage with paginated post feed."""
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=5, error_out=False
    )
    return render_template('main/index.html', title='Home', pagination=pagination)

@main_bp.route('/about')
def about():
    """About page."""
    return render_template('main/about.html', title='About Us')

@main_bp.route('/search')
def search():
    """Full-text search across post title and content."""
    q = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    pagination = None
    if q:
        pagination = Post.query.filter(
            Post.title.ilike(f'%{q}%') | Post.content.ilike(f'%{q}%')
        ).order_by(Post.created_at.desc()).paginate(page=page, per_page=5, error_out=False)
    return render_template('main/search.html', title='Search Results', q=q, pagination=pagination)
