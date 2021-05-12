from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from werkzeug.utils import secure_filename

from app import bcrypt, mail

from app.models import (User, Post, Comment)
from app.forms import (LoginForm, RegistrationForm, PostForm, CommentForm)

from datetime import datetime

from flask_mail import Message
import plotly
import plotly.graph_objs as go
import os
import io
import json
import base64

users = Blueprint('users', __name__)

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if (user is not None and bcrypt.check_password_hash(user.password, form.password.data)):
           login_user(user)
           flash(f'{current_user.username} Successfully Logged In')
           return redirect(url_for('posts.profile', username=current_user.username))
        else:
            flash('Wrong Username or Password')

    return render_template("login.html", title='Login', form=form)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.index'))    
    
    form = RegistrationForm()
    if form.validate_on_submit():        
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')        
        user = User(username=form.username.data,email=form.email.data, password=hashed)        
        user.save()
        flash('Successfully Registered')
        return redirect(url_for('users.send_mail', name=form.username.data, email=form.email.data))
    
    return render_template('register.html', title='Register', form=form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('posts.index'))

@users.route('/send_mail/<name>/<email>')
def send_mail(name, email):
    msg = Message(subject='Thank you for Registering ' + name, body="We really appreciate you signing up " + name + "! Let us know if you have any questions.", sender='ericliam388J@gmail.com', recipients=[email])
    mail.send(msg)
    return redirect(url_for('users.login'))