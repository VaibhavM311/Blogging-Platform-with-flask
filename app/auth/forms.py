from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models.user import User

class RegistrationForm(FlaskForm):
    """Form for new user registration."""
    username = StringField('Username', validators=[
        DataRequired(message='Username is required.'),
        Length(min=3, max=64, message='Username must be between 3 and 64 characters.')
    ])
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required.'),
        Email(check_deliverability=False, message='Please enter a valid email address.'),
        Length(max=120)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.'),
        Length(min=6, message='Password must be at least 6 characters long.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password.'),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        """Ensure username is unique."""
        user = User.query.filter_by(username=username.data.strip()).first()
        if user:
            raise ValidationError('That username is already taken. Please choose another.')

    def validate_email(self, email):
        """Ensure email is unique."""
        user = User.query.filter_by(email=email.data.strip().lower()).first()
        if user:
            raise ValidationError('An account with this email already exists.')

class LoginForm(FlaskForm):
    """Form for existing user login."""
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required.'),
        Email(check_deliverability=False, message='Please enter a valid email address.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.')
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EditProfileForm(FlaskForm):
    """Form for logged-in users to update their profile bio, username, and email."""
    username = StringField('Username', validators=[
        DataRequired(message='Username is required.'),
        Length(min=3, max=64, message='Username must be between 3 and 64 characters.')
    ])
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required.'),
        Email(check_deliverability=False, message='Please enter a valid email address.'),
        Length(max=120)
    ])
    bio = TextAreaField('About Me (Bio)', validators=[
        Length(max=280, message='Bio cannot exceed 280 characters.')
    ])
    submit = SubmitField('Save Changes')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data.strip() != self.original_username:
            user = User.query.filter_by(username=username.data.strip()).first()
            if user:
                raise ValidationError('That username is already in use by another account.')

    def validate_email(self, email):
        if email.data.strip().lower() != self.original_email:
            user = User.query.filter_by(email=email.data.strip().lower()).first()
            if user:
                raise ValidationError('An account with this email already exists.')
