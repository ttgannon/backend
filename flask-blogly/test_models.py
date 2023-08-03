from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False

with app.app_context():
    db.drop_all()
    db.create_all()


class UserModelTestCase(TestCase):
    """Tests model of users"""

    def setUp(self):
        User.query.delete()
    def tearDown(self):
        db.session.rollback()

    def test_get_by_id(self):
        user1 = User(first_name="Joe",
                    last_name="Smith",
                    image_url="https://www.google.com")
        user2 = User(first_name="JANE",
                    last_name="JOLLY",
                    image_url="https://www.google.com")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        users = User.get_by_id(1)
        self.assertEqual(users, user1)
        self.assertEqual(users.first_name, "Joe")
        
        users = User.get_by_id(2)
        self.assertEqual(users, user2)
        self.assertEqual(users.first_name, "JANE")


