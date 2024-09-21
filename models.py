from flask_sqlalchemy import SQLAlchemy

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
    
    @property
    def full_name(self):
        """Return full name of user"""

        return f"{self.first_name} {self.last_name}"