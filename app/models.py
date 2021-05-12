from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username

class Post(db.Document):
    postid = db.StringField(required=True, unique=True)
    author = db.ReferenceField(User)
    image = db.ImageField()
    date = db.StringField(required=True)
    caption = db.StringField(required=True)

class Comment(db.Document):
    postid = db.StringField(required=True)
    # post = db.ReferenceField(Post)
    author = db.ReferenceField(User)
    comment = db.StringField(required=True)
    date = db.StringField(required=True)
