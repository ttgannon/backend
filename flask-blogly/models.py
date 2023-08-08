"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User information."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    image_url = db.Column(db.String, nullable = True, default = None)

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)


class Story(db.Model):
    """Story information"""
    __tablename__ = "stories"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    story_name = db.Column(db.String, nullable = False)
    story_content = db.Column(db.String, nullable = False)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    author = db.relationship('User')
    # author = db.relationship('User', backref='stories')