"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from datetime import datetime

default_picture = 'http://s3.amazonaws.com/pix.iemoji.com/images/emoji/apple/ios-12/256/smiling-face.png'
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
    image_url = db.Column(db.String, nullable = True, default = 'http://s3.amazonaws.com/pix.iemoji.com/images/emoji/apple/ios-12/256/smiling-face.png')
    
    stories = db.relationship('Story', backref='author', cascade='all, delete-orphan')
    


    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)


class Story(db.Model):
    """Story information"""
    __tablename__ = "stories"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    story_name = db.Column(db.String, nullable = False)
    story_content = db.Column(db.String, nullable = False)
    publish_time = db.Column(DateTime, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # author = db.relationship('User')

    tags = db.relationship('PostTag', backref='tags', cascade='all, delete-orphan')
    
    # author = db.relationship('User', backref='stories')

class Tag(db.Model):
    """Tags to add to stories for ease of sorting"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    posts_with_tag = db.relationship('PostTag', backref = 'posts')
    # stories_with_tag = db.relationship("Story")

class PostTag(db.Model):
    """Demonstrate relationship between posts and their tags"""

    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('stories.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    # posts_tags = db.relationship('Story', cascade='all, delete-orphan')

    
