from flask import render_template, session, Flask, redirect, flash
from models import connect_db, db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm


app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'abc123'
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)
db.create_all()

@app.route('/')
def home():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    username = session.get('username')
    
    if username is not None:
        flash("you're already logged in")
        return redirect(f'/users/{session["username"]}')

    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        flash("New account registered!")
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = session.get('username')
    
    if username is not None:
        flash("you're already logged in")
        return redirect(f'/users/{session["username"]}')
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            flash(f'Welcome back, {user.username}!')
            session['username'] = username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ['Invalid username/password']
    return render_template('login.html', form=form)
    

@app.route('/logout')
def logout():
    if session.get('username') == None:
        flash("You aren't logged in")
        return redirect('/login')
    session.pop('username')
    return redirect('/')

@app.route('/users/<username>')
def go_profile(username):
    if session.get('username') == None:
        flash('please log in')
        return redirect('/login')
    user = User.query.filter_by(username=username).first()
    return render_template('user.html', user=user)

@app.route('/user/<username>/feedback/add', methods=['GET','POST'])
def feedback(username):
    if  username not in session['username']:
        flash('please log in')
        return redirect('/login')
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = form.content.data
        title = form.title.data
        username = session['username']
        new_feedback = Feedback(title=title, content=feedback, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    return render_template('feedback.html', username=username, form=form)
    

@app.route('/feedback/<feedback_id>/update', methods=['GET','POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if feedback.username not in session['username']:
        flash('please log in')
        return redirect('/login')
    
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.content = form.content.data
        feedback.title = form.title.data
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    
    return render_template('edit_feedback.html', form = form, feedback = feedback)

@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    username = Feedback.query.filter_by(id=feedback_id).first()
    print(username)
    if username.username not in session['username']:
        flash('please log in')
        return redirect('/login')
    feedback = Feedback.query.get(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    user = User.query.filter_by(username=username.username).first()
    return render_template('/user.html', user=user)

@app.route('/users/<username>/delete', methods=['GET','POST'])
def delete_user(username):
    if username not in session['username']:
        flash('please log in')
        return redirect('/login')
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    form = UserForm()
    return redirect('/register')