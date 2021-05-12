from flask import render_template, flash, redirect, url_for, Blueprint,send_file
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from werkzeug.utils import secure_filename

from app.models import (User, Post, Comment)
from app.forms import (LoginForm, RegistrationForm, PostForm, CommentForm)
import pandas as pd
from datetime import datetime
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io
import json
import base64

posts = Blueprint('posts', __name__)

fig,ax = plt.subplots(figsize=(6,6))
ax=sns.set_style(style='darkgrid')

# x= [1,2,3]
# y= ["one", "two", "three"]

def current_time() -> str:
    return datetime.now().strftime("%B %d")

def get_b64_imgs_index():
        posts = Post.objects()    
        temp = []
        for post in posts:
            bytes_im = io.BytesIO(post.image.read())    
            image = base64.b64encode(bytes_im.getvalue()).decode()
            temp.append(image)
        return temp

@posts.route('/')
@posts.route('/index')
def index():
    users = User.objects()
    posts = Post.objects()      
    comments = Comment.objects()

    return render_template("index.html", title='Home', users=users, posts=posts, images=get_b64_imgs_index())
    

def get_b64_imgs_profile(username):
        user = User.objects(username=username).first()
        posts = Post.objects(author=user)    
        temp = []
        for post in posts:
            bytes_im = io.BytesIO(post.image.read())    
            image = base64.b64encode(bytes_im.getvalue()).decode()
            temp.append(image)
        return temp

@posts.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # handle the post form
    postform = PostForm()
    if postform.validate_on_submit():
        img = postform.image.data
        filename = secure_filename(img.filename)
        content_type = f'/images/{filename[-3:]}'

        newPost = Post(
            postid=f'post{len(Post.objects())}',
            author=current_user._get_current_object(),
            date=current_time(),
            caption=postform.caption.data
        )
        newPost.image.put(img.stream, content_type=content_type)
        
        newPost.save()

        flash('Successfully Posted')
        return redirect(url_for('posts.profile', username=username))
    
    # get all posts
    user = User.objects(username=username).first()
    posts = Post.objects(author=user)

    # list of lists of comments for posts
    comments = []
    for post in posts:
        comments.append( Comment.objects(postid=post.postid) )

    arr = []
    for i in posts:
        date = i.date
        if [date,0] not in arr:
            arr.append([i.date,0])

    for a in arr:
        for i in posts:
            if a[0] == i.date:
                a[1] += 1
    
    x = json.dumps([row[0] for row in arr])
    y = json.dumps([row[1] for row in arr])
    
    return render_template('profile.html', username=username, postform=postform, posts=posts, images=get_b64_imgs_profile(username), comments=comments,x=x,y=y)


def get_b64_img_post(postid):
    post = Post.objects(postid=postid).first()
    bytes_im = io.BytesIO(post.image.read())    
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image   


@posts.route("/post/<postid>", methods=["GET", "POST"])
def post(postid):
    post = Post.objects(postid=postid).first()
    commentform=CommentForm()
    if commentform.validate_on_submit():
        newComment = Comment(
            postid = postid,
            author = current_user._get_current_object(),
            date = current_time(),
            comment = commentform.comment.data
        )
        newComment.save()

        flash('Successfully Commented')
        return redirect(url_for('posts.post', postid=postid))

    comments = Comment.objects(postid=postid)

    return render_template('post.html', post=post, commentform=commentform, image=get_b64_img_post(postid), comments=comments)
