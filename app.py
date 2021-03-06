#from __future__ import print_function
import os
import re
import sys
import json
from flask import Flask, render_template, redirect, request, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
from sqlalchemy import Column, Integer, Text

from flask.ext.heroku import Heroku


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://ggadmin:admin@localhost/glibglab"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)

from models import User, Course, Question

db.create_all()

api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(User, methods=['GET', 'POST', 'DELETE', 'PUT'])


@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        _username = request.form['reg_username']
        _password = request.form['reg_password']
        _password_confirm = request.form['reg_password_confirm']
        _email = request.form['reg_email']
        _fullname = request.form['reg_fullname']
        _soi = request.form.get('userType', None)
        _agree = request.form.get('reg_agree', 'agree2')
        if db.session.query(User).filter(User.username == _username).scalar() is None:
            if _password == _password_confirm:
                if _agree == 'agree1':
                    session['username'] = _username
                    session['password'] = _password
                    session['email'] = _email
                    session['soi'] = _soi
                    if session['soi'] == 'option1':
                        new_user = User(_username, _password, _email, _fullname, _soi)
                        db.session.add(new_user)
                        db.session.commit()
                        return redirect(url_for('student'))
                    elif session['soi'] == 'option2':
                        new_user = User(_username, _password, _email, _fullname, _soi)
                        db.session.add(new_user)
                        db.session.commit()
                        return redirect(url_for('teacher'))
                    else:
                        error = "Must choose a role."
                        return render_template('signup.html', error=error) 
                else:
                    error = "Must agree with terms."
                    return render_template('signup.html', error=error)
            else:
                error = "Passwords do not match."
                return render_template('signup.html', error=error)
        else:
            error = "Username is already taken."
            return render_template('signup.html', error=error)
    return render_template('signup.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if User.query.filter(User.username == request.form['lg_username'], 
                             User.password == request.form['lg_password']).count():
            found_user = User.query.filter(User.username == request.form['lg_username']).first()
            soi = found_user.soi
            fullname = found_user.name
            session['username'] = request.form['lg_username']
            session['password'] = request.form['lg_password']
            session['soi'] = soi
            session['name'] = fullname
            if session['soi'] == 'option1':
                return redirect(url_for('student'))
            else:
                return redirect(url_for('teacher'))
        else:
            error = "Invalid credentials. Please try again."
    return render_template('login.html', error=error)

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    error = None
    if request.method == 'POST':
        if User.query.filter(User.email == request.form['fp_email']).count():
            found_user = User.query.filter(User.email == request.form['fp_email']).first()
            email_to_send_to = found_user.email
            #SEND EMAIL (somehow) TO USER WITH THAT EMAIL
            #forgotten_email(email_to_send_to)
            return redirect(url_for('index'))
        else:
            error = "User with that email doesn't exist"
    return render_template('forgotpassword.html', error=error)

@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
    error = None
    current_courses = Course.query.filter(Course.course_instructor == session['username']).all()
    if request.method == 'POST':
        _coursename = request.form['course_name']
        _courseinstructor = session['username']
        found_user = User.query.filter(User.username == _courseinstructor).first()
        _instructorname = found_user.name
        if (Course.query.filter(Course.course_name == _coursename, Course.course_instructor == _courseinstructor).count()) == 0:
            new_course = Course(_courseinstructor, _instructorname, _coursename)
            db.session.add(new_course)
            db.session.commit()
            current_courses = Course.query.filter(Course.course_instructor == session['username']).all()
    return render_template('TeacherView.html', error=error, current_courses=current_courses)

@app.route('/teacherfeed', methods=['GET', 'POST'])
def teacherfeed():
    error = None
    questions = Question.query.filter(Question.question_instructor == session['username']).all()
    x = len(questions)
    if x >= 1:
        return render_template('TeacherFeed.html', error=error, questions=questions) 
    return render_template('TeacherFeed.html', error=error)
    
@app.route('/student', methods=['GET', 'POST'])
def student():
    error = None
    current_courses = Course.query.all()
    return render_template('StudentView.html', error=error, current_courses=current_courses)

@app.route('/questions', methods=['GET', 'POST'])
def notesview():
    error = None
    current_questions = Question.query.filter(Question.question_owner == session['username']).first()
    if request.method == 'POST':
        _question = request.form.get('question', None)
        if _question != None:
            new_question = Question(session['username'], 'testinstructor', _question, False)
            db.session.add(new_question)
            db.session.commit()
            current_questions = new_question
    return render_template('NotesView.html', error=error, current_questions=current_questions)
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

app.debug = True
app.secret_key = '\xd6;\xcc\xd8N\xf0\x11\x89k\x08\n~Eu\x01\x9c\x86\xc3\xae\x89 \xfa\x9a\x04'
if __name__ == '__main__':
    app.run()