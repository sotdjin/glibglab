from app import db
from sqlalchemy.dialects.postgresql import JSON

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text, unique=False)
    email = db.Column(db.Text, unique=True)
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

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question_owner = db.Column(db.Text, unique=False)
    question_instructor = db.Column(db.Text, unique=False)
    question_course = db.Column(db.Text, unique=False)
    question = db.Column(db.Text, unique=False)
    read = db.Column(db.Boolean, unique=False, default=False)
    notes = db.Column(db.Text, unique=False, default="")
    
    def __init__(self, question_owner, question_instructor, question, read):
        self.question_owner = question_owner
        self.question_instructor = question_instructor
        self.question = question
        self.read = read
    
    def __repr__(self):
        return '<Question %r>' % self.id

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    course_instructor = db.Column(db.Text, unique=False)
    course_name = db.Column(db.Text, unique=False)
    course_color = db.Column(db.Text, unique=False)
    
    def __init__(self, course_instructor, course_name, course_color):
        self.course_instructor = course_instructor
        self.course_name = course_name
        self.course_color = course_color
        
    def __repr__(self):
        return '<Course %r>' % self.course_name