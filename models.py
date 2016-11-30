from app import db
from sqlalchemy.dialects.postgresql import JSON

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text, unique=False)
    email = db.Column(db.Text, unique=True)
    name = db.Column(db.Text, unique=False)
    questions = db.relationship('Question', backref='users', lazy='dynamic')
    
    def __init__(self, username, password, email, name):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
    
    def __repr__(self):
        return '<User %r>' % self.username

class Instructor(db.Model):
    __tablename__ = 'instructors'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text, unique=False)
    email = db.Column(db.Text, unique=True)
    name = db.Column(db.Text, unique=False)
    questions = db.relationship('Question', backref='instructors', lazy='dynamic')
    
    def __init__(self, username, password, email, name):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        
    def __repr__(self):
        return '<Instructor %r>' % self.username

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question_owner = db.Column(db.Text, db.ForeignKey('users.username'))
    question_instructor = db.Column(db.Text, db.ForeignKey('instructors.username'))
    question = db.Column(db.Text, unique=False)
    read = db.Column(db.Boolean, unique=False, default=False)
    notes = db.Column(db.Text, unique=False, default="")
    
    def __init__(self, question_owner, question, read):
        self.question_owner = question_owner
        self.question = question
        self.read = read
    
    def __repr__(self):
        return '<Question %r>' % self.id