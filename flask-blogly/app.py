"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User, Story, PostTag, Tag, default_picture
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
    stories = Story.query.order_by(Story.publish_time.desc()).limit(5).all()
    return render_template('home.html', stories=stories)

@app.route("/users")
def users():
    userlist = User.query.all()
    return render_template("users.html", userlist = userlist)

@app.route("/users/new", methods=['GET','POST'])
def new_users():
    if request.method == 'GET':
        return render_template('users_form.html')
    elif request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        prof_pic = request.form['img_url']
        
        if prof_pic == '':
            prof_pic = default_picture

        new_user = User(first_name=fname, last_name=lname, image_url=prof_pic)
        
        db.session.add(new_user)
        db.session.commit()

        return redirect("/users")

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
    return redirect('/users')

@app.route('/users/<user_id>/posts/new', methods=['GET','POST'])
def go_to_new_post(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)
        tags = Tag.query.all()
        return render_template('add_post.html', user=user, tags=tags)
    
    
    content = request.form['content']
    title = request.form['title']

    if content == '' or title == '':
        return redirect(f'/users/{user_id}/posts/new')

    tag_id = request.form.getlist('tags_html')
    
    new_story = Story(story_name=title, story_content=content, author_id=user_id)
    db.session.add(new_story)
    db.session.commit()

    #should probably fix to not run all these queries?
    for id in tag_id:
        new_post_tag = PostTag(post_id=new_story.id, tag_id=id)
        db.session.add(new_post_tag)

    
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

@app.route('/tags')
def get_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<tag_id>')
def tag_id(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('tag.html', tag=tag)

@app.route('/tags/<tag_id>/edit', methods=['GET','POST'])
def edit_tag(tag_id):
    if request.method == 'GET':
        tag = Tag.query.get(tag_id)
        request.method = 'POST'
        return render_template('tag.html', tag=tag, request=request)
    tag = Tag.query.get(tag_id)
    tag.name = request.form['tag']
    db.session.commit()
    return redirect(f'/tags/{tag_id}')

@app.route('/tags/new', methods=['GET','POST'])
def new_tags():
    if request.method == 'GET':
        return render_template('new_tag.html')
    
    tag = request.form['tag']
    if Tag.query.filter_by(name=tag).first():
        flash(f'The tag "{tag}" already exists', 'warning')
        return redirect('/tags/new')
    new_tag = Tag(name=tag)

    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<tag_id>/delete', methods=['GET','POST'])
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/stories')
def show_stories():
    stories = Story.query.all()
    return render_template('stories.html', stories=stories)