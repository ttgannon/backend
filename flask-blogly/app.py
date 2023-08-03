"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
    return app

app = create_app()

# to allow interactivity with terminal
app.app_context().push()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "thisismysecretkeydontguessitplease123789"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)


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
    return render_template('user_prof.html', user=user)

@app.route('/users/<user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.get_by_id(user_id)
    if not user:
        return "User not found", 404
    
    if request.method == 'GET':
        return render_template('users_form.html', user=user)
    
    fname = request.form['first_name']
    lname = request.form['last_name']
    prof_pic = request.form['img_url'] 

    user.first_name = fname
    user.last_name = lname
    user.image_url = prof_pic

    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/users/<user_id>/delete')
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

