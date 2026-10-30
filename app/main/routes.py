from flask import render_template, request, current_app
from app.main import main_bp
from app.models.post import Post
from app.models.category import Category, Tag
from app import db

@main_bp.route('/')
@main_bp.route('/home')
def index():
    """Homepage with paginated post feed."""
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=current_app.config.get('POSTS_PER_PAGE', 5), error_out=False
    )
    return render_template('main/index.html', title='Home', pagination=pagination)

@main_bp.route('/about')
def about():
    """About page."""
    return render_template('main/about.html', title='About Us')

@main_bp.route('/search')
def search():
    """Search posts by title/content and filter by category or tag."""
    q = request.args.get('q', '').strip()
    category_slug = request.args.get('category', '').strip()
    tag_slug = request.args.get('tag', '').strip()
    page = request.args.get('page', 1, type=int)
    query = Post.query
    if q:
        term = f"%{q}%"
        query = query.filter(db.or_(Post.title.ilike(term), Post.content.ilike(term)))
    if category_slug:
        query = query.join(Category).filter(Category.slug == category_slug)
    if tag_slug:
        query = query.join(Post.tags).filter(Tag.slug == tag_slug)
    pagination = query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=current_app.config.get('POSTS_PER_PAGE', 5), error_out=False
    )
    categories = Category.query.order_by(Category.name).all()
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('main/search.html', title='Search Results', q=q,
        pagination=pagination, categories=categories, tags=tags,
        selected_category=category_slug, selected_tag=tag_slug)
