from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from app import db
from app.posts import posts_bp
from app.posts.forms import PostForm
from app.models.post import Post
from app.models.user import User

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
    return render_template('posts/post_detail.html', title=post.title, post=post)

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
    """Display all posts written by a specific user."""
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.created_at.desc()).all()
    return render_template('posts/user_posts.html', title=f"Posts by {user.username}", user=user, posts=posts)
