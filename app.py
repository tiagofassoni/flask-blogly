"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogly.db    '
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)

@app.route('/')
def home_page():
    """redirect to list of users (for now)"""
    return redirect('/users')

@app.route('/users')
def list_users():
    """list all userrs"""
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route('/users/new')
def add_user():
    """show form to add a new user"""
    return render_template('new_user.html')

@app.route("/users/new", methods=["POST"])
def handle_new_user_form():
    """process form data to add new user to databse"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user  = User(first_name=first_name, last_name=last_name, image_url=image_url or None)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show details about a single pet"""
    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """edit user details"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def handle_edit_user_form(user_id):
    """process form to edit user data"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """delete user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)

    db.session.commit()
    return redirect('/users')

@app.route("/users/<int:user_id>/posts/new")
def create_post(user_id):
    """show form to create a new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template("new_post.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def handle_new_post_form(user_id):
    """process form to add user's new post"""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title,
                    content=content,
                    user_id=user.id, 
                    tags=tags)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """show the details of a post"""
    post = Post.query.get_or_404(post_id)

    return render_template("post_details.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """show form to edit a post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("edit_post.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def handle_edit_post_form(post_id):
    """handle form submission for editing a post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")

@app.route("/posts/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    """deleted post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

@app.route("/tags")
def list_tags():
    """list all tags"""
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)

@app.route("/tags/<int:id>")
def show_tag_details(id):
    """show details about a tag"""
    tag = Tag.query.get_or_404(id)
    return render_template("tag_details.html", tag=tag)

@app.route("/tags/new")
def new_tag():
    """show form to add a new tag"""
    return render_template("new_tag.html")

@app.route("/tags/new", methods=["POST"])
def handle_new_tag_form():
    """process new tag form submission"""
    tag_name = request.form["tag_name"]
    
    new_tag = Tag(tag_name=tag_name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:id>/edit")
def edit_tag(id):
    "show form to edit tag details"
    tag = Tag.query.get_or_404(id)

    return render_template("edit_tag.html", tag=tag)

@app.route("/tags/<int:id>/edit", methods=["POST"])
def handle_edit_tag_form(id):
    """handle form submission to edit a tag"""

    tag = Tag.query.get_or_404(id)
    tag.tag_name = request.form["tag_name"]

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:id>", methods=["POST"])
def delete_tag(id):
    "delete a tag"
    tag = Tag.query.get_or_404(id)
    
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")

    
