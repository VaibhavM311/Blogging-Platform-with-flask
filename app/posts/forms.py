from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    """Form for creating and editing blog posts."""
    title = StringField('Post Title', validators=[
        DataRequired(message='Please provide a title for your post.'),
        Length(min=3, max=150, message='Title must be between 3 and 150 characters.')
    ])
    content = TextAreaField('Content', validators=[
        DataRequired(message='Post content cannot be empty.'),
        Length(min=10, message='Content must be at least 10 characters long.')
    ])
    category = StringField('Category', validators=[Length(max=60)])
    tags = StringField('Tags (comma-separated)', validators=[Length(max=250)])
    submit = SubmitField('Publish Post')
