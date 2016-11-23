from app import db
from sqlalchemy.dialects.postgresql import JSON

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text, unique=False)
    email = db.Column(db.Text, unique=False)
    name = db.Column(db.Text, unique=False)
    soi = db.Column(db.Text, unique=False)
    
    def __init__(self, username, password, email, name, soi):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.soi = soi
    
    def __repr__(self):
        return '<User %r>' % self.username