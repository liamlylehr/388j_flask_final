from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)
from flask_mongoengine import MongoEngine

from .models import (User, Post, Comment)


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


class SearchFrom(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    submit = SubmitField("Search")

class PostForm(FlaskForm):
    image = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images Only!')])    
    caption = TextAreaField(
        "caption", validators=[InputRequired(), Length(min=1, max=500)]
    )    
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    comment = TextAreaField(
        "comment", validators=[InputRequired(), Length(min=1, max=500)]
    )    
    submit = SubmitField('Comment')
