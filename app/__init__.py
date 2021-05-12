from flask import Flask
import os
from flask_mail import Mail, Message
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt

db = MongoEngine()
login_manager = LoginManager()
mail = Mail()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'ericliam388J@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ericliam388J$$'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)

    app.config["SECRET_KEY"] = "this-key-is-secret"
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )
    
    app.config["MONGO_URI"] ="mongodb://localhost:27017/perspect_db"

    

    db.init_app(app)
    login_manager.init_app(app)
    # login_manager.login_view = "login"

    bcrypt.init_app(app)


    from app.posts.routes import posts
    from app.users.routes import users

    app.register_blueprint(users)
    app.register_blueprint(posts)

    return app

# from app import routes
