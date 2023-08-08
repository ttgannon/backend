from unittest import TestCase
from app import app
from models import db, User
from flask import url_for

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True # makes Flask errors be real errors, rather than HTML with error info

db.drop_all()
db.create_all()

class IntegrationTest(TestCase):
    """Tests for integration of users"""

    def setUp(self):
        user = User(first_name="Joe", last_name="Shmoe", image_url="ABC123")

        db.session.add(user)
        db.session.commit()

        self.id = id
    def tearDown(self):
        db.session.rollback()

    def test_home(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            self.assertIn("Joe Shmoe", html)
            self.assertEqual(resp.status_code, 200)

    def test_new_user(self):
        with app.test_client() as client:
            data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'img_url': 'https://example.com/john.jpg'
            }
            resp = client.post('/users/new', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("John Doe", html)
            self.assertIn("Joe Shmoe", html)

    def test_edit_user(self):
        with app.test_client() as client:
            data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'img_url': 'https://example.com/john.jpg'
            } 
            user_id = 2
            url = f'/users/{user_id}/edit'
            resp = client.post(url, data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("John Doe", html)
            


    def test_delete(self):
        with app.test_client() as client:
            user_id = 1
            url = f'/users/{user_id}/delete'
            resp = client.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200) 

    def test_user_posts(self):
        with app.test_client() as client:
            user_id = 2
            url = f'/users/{user_id}/posts/new'
            resp = client.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Add", html)

            data = {
                'content': 'story',
                'title': 'hello',
            } 
            resp = client.post(url, data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edit", html)
            self.assertIn("Delete", html)