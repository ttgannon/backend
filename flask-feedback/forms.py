from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length

class UserForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])
    username = StringField("Username", validators=[InputRequired(), Length(max=30)])
    password = PasswordField("Password", validators=[InputRequired(), Length(max=30)])
    email = EmailField('Email Address', validators=[InputRequired()])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=30)])
    password = PasswordField("Password", validators=[InputRequired(), Length(max=30)])

class FeedbackForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    content = StringField('Feedback', validators=[InputRequired()])