from flask import Flask, render_template, redirect
from model import db, connect_db, Pet
from forms import AddPetForm

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "hello"


connect_db(app)

# db.drop_all()
# db.create_all()


@app.route('/')
def home():
    pets = Pet.query.all()
    return render_template('home.html', pets=pets)

@app.route('/add', methods=['GET','POST'])
def add_pet():
    form = AddPetForm()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        new_pet = Pet(name=name,species=species,photo_url=photo_url,age=age,notes=notes)
        db.session.add(new_pet)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('add_pet.html', form=form)
    
@app.route('/<pet_id>')
def go_to_pet(pet_id):
    pet = Pet.query.get(pet_id)
    return render_template('pet_profile.html', pet=pet)

@app.route('/edit/<pet_id>', methods=['GET','POST'])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = AddPetForm(obj=pet)
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.photo_url = form.photo_url.data
        pet.age = form.age.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        return redirect('/')
    else:
        return render_template('edit_pet.html', form=form, pet=pet)
