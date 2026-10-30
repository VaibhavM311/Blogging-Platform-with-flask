from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from app import db
from app.posts import posts_bp
from app.posts.forms import PostForm
from app.models.post import Post
from app.models.user import User
from app.models.comment import Comment
from app.models.category import Category, Tag
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm



def apply_taxonomy(post, category_name, tag_names):
    """Create/reuse category and tags, then associate them with a post."""
    from werkzeug.utils import secure_filename
    category_name = (category_name or '').strip()
    if category_name:
        slug = secure_filename(category_name.lower()).replace('_', '-')
        category = Category.query.filter_by(slug=slug).first()
        if not category:
            category = Category(name=category_name, slug=slug)
            db.session.add(category)
        post.category = category
    else:
        post.category = None
    post.tags = []
    for raw in (tag_names or '').split(','):
        name = raw.strip()
        if not name:
            continue
        slug = secure_filename(name.lower()).replace('_', '-')
        tag = Tag.query.filter_by(slug=slug).first()
        if not tag:
            tag = Tag(name=name, slug=slug)
            db.session.add(tag)
        if tag not in post.tags:
            post.tags.append(tag)

class CommentForm(FlaskForm):
    body = TextAreaField("Comment", validators=[DataRequired(), Length(min=2, max=2000)])
    submit = SubmitField("Post comment")

@posts_bp.route('/<int:post_id>/comments', methods=['POST'])
@login_required
def add_comment(post_id):
    post = db.get_or_404(Post, post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data.strip(), author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added.', 'success')
    else:
        flash('Please enter a comment between 2 and 2000 characters.', 'warning')
    return redirect(url_for('posts.post_detail', post_id=post.id) + '#comments')

@posts_bp.route('/comments/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = db.get_or_404(Comment, comment_id)
    if comment.author != current_user and comment.post.author != current_user:
        abort(403)
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.', 'info')
    return redirect(url_for('posts.post_detail', post_id=post_id) + '#comments')

@posts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """Create and publish a new blog post."""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data.strip(),
            content=form.content.data.strip(),
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been published successfully!', 'success')
        return redirect(url_for('posts.post_detail', post_id=post.id))

    return render_template('posts/create_post.html', title='Write New Post', form=form)

@posts_bp.route('/<int:post_id>')
def post_detail(post_id):
    """View an individual blog post."""
    post = db.get_or_404(Post, post_id)
    return render_template('posts/post_detail.html', title=post.title, post=post, comment_form=CommentForm(), Comment=Comment)

@posts_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """Edit an existing blog post (only authorized for original author)."""
    post = db.get_or_404(Post, post_id)

    # Permission check: prevent unauthorized edits
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data.strip()
        post.content = form.content.data.strip()
        db.session.commit()
        flash('Your post has been updated successfully!', 'success')
        return redirect(url_for('posts.post_detail', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category.name if post.category else ''
        form.tags.data = ', '.join(tag.name for tag in post.tags)

    return render_template('posts/edit_post.html', title='Edit Post', form=form, post=post)

@posts_bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete a blog post (only authorized for original author)."""
    post = db.get_or_404(Post, post_id)

    # Permission check: prevent unauthorized deletions
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'info')
    return redirect(url_for('main.index'))

@posts_bp.route('/user/<string:username>')
def user_posts(username):
    """Display all posts written by a specific user (paginated)."""
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(author=user).order_by(Post.created_at.desc()).paginate(
        page=page, per_page=5, error_out=False
    )
    return render_template('posts/user_posts.html', title=f"Posts by {user.username}", user=user, pagination=pagination)
