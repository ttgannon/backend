"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Story
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# to allow interactivity with terminal
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "thisismysecretkeydontguessitplease123789"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route("/")
def home_page():
    userlist = User.query.all()
    return render_template("users.html", userlist = userlist)

@app.route("/users/new", methods=['GET','POST'])
def users():
    if request.method == 'GET':
        return render_template('users_form.html')
    elif request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        prof_pic = request.form['img_url']
        
        new_user = User(first_name=fname, last_name=lname, image_url=prof_pic)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/")

@app.route('/users/<user_id>')
def user_page(user_id):
    user = User.get_by_id(user_id)
    posts = Story.query.filter_by(author_id=user_id)
    return render_template('user_prof.html', user=user, posts=posts)

@app.route('/users/<user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.get_by_id(user_id)
    if not user:
        return "User not found", 404
    
    if request.method == 'GET':
        return render_template('users_form.html', user=user)
    
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['img_url']

    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/users/<user_id>/delete', methods=['GET','POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

@app.route('/users/<user_id>/posts/new', methods=['GET','POST'])
def go_to_new_post(user_id):
    user = User.query.get(user_id)
    if request.method == 'GET':
        return render_template('add_post.html', user=user)
    
    
    content = request.form['content']
    title = request.form['title']
    
    new_story = Story(story_name=title, story_content=content, author=user)

    db.session.add(new_story)
    db.session.commit()
    
    return redirect(f'/users/{user_id}')


@app.route('/posts/<post_id>')
def show_post(post_id):
    post = Story.query.get(post_id)
    return render_template('post.html', post=post)

@app.route('/posts/<post_id>/delete', methods = ['GET', 'POST'])
def delete_post(post_id):
    post = Story.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.author_id}')

@app.route('/posts/<post_id>/edit', methods = ['GET','POST'])
def edit_post(post_id):
    if request.method == 'GET':
        post = Story.query.get(post_id)
        return render_template('add_post.html', post=post)
    
    post = Story.query.get(post_id)
    post.story_name = request.form['title']
    post.story_content = request.form['content']
    db.session.commit()

    return redirect(f'/posts/{post.id}')