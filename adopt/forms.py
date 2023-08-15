from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, RadioField, SelectField
from wtforms.validators import InputRequired, Email, Optional, URL, NumberRange

class AddPetForm(FlaskForm):
    """Form for adding pets to the database"""
    name = StringField('Name', validators=[InputRequired()])

    # species = RadioField('Species', choices = [('cat', 'Cat'), ('dog','Dog'), ('porcupine','Porcupine')])
    species = SelectField('Species', choices = [('cat', 'Cat'), ('dog','Dog'), ('porcupine','Porcupine')], validators=[InputRequired()])
    
    photo_url = StringField('Photo URL', validators=[Optional(), URL()])
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=0, max=30)])
    notes = StringField("Anything to add?", validators=[Optional()])

    available = BooleanField('This Pet Available for Adoption')