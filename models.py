from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
DEFAULT_IMAGE_URL = "https://cdn.vectorstock.com/i/500p/53/42/user-member-avatar-face-profile-icon-vector-22965342.jpg"

def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)     
        db.create_all()  

"""Models for Blogly."""

class User(db.Model):
    """Site user"""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String,
                           nullable=False)
    
    last_name = db.Column(db.String,
                           nullable=False)
    
    image_url = db.Column(db.String,
                          nullable=False,
                          default=DEFAULT_IMAGE_URL)
    
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"{self.id} {self.first_name} {self.last_name} {self.image_url}"
    
    @property
    def full_name(self):
        """Return full name of user"""

        return f"{self.first_name} {self.last_name}"
    
    
    

class Post(db.Model):
    """Blog post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.Text,
                      nullable=False)
    
    content = db.Column(db.Text,
                        nullable=False)
    
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    
    @property
    def friendly_date(self):
        """Return nicely formatted date."""

        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")