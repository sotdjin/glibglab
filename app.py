#from __future__ import print_function
import os
import re
import sys
from flask import Flask, render_template, redirect, request, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
from sqlalchemy import Column, Integer, Text


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://ggadmin:admin@localhost/glibglab"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
        print _soi
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
                        return redirect(url_for('classview'))
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
    soi = 0
    if request.method == 'POST':
        if User.query.filter(User.username == request.form['username'], 
                             User.password == request.form['password']).count():
            found_user = User.query.filter(User.username == request.form['username']).first()
            soi = found_user.soi
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            session['soi'] = soi
            if session['soi'] == 'option1':
                return redirect(url_for('classview'))
            else:
                return redirect(url_for('teacher'))
        else:
            error = "Invalid credentials. Please try again."
    return render_template('login.html', error=error)

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    error = None
    if request.method == 'POST':
        if User.query.filter(User.email == request.form['email']).count():
            found_user = User.query.filter(User.email == request.form['email']).first()
            email_to_send_to = found_user.email
            #SEND EMAIL (somehow) TO USER WITH THAT EMAIL
            #forgotten_email(email_to_send_to)
            return redirect(url_for('index'))
        else:
            error = "User with that email doesn't exist"
    return render_template('forgotpassword.html', error=error)

@app.route('/teacher')
def teacher():
    error = None
    return render_template('TeacherView.html', error=error)

@app.route('/class')
def classview():
    error = None
    return render_template('ClassView.html', error=error)
    
@app.route('/notes')
def notesview():
    error = None
    return render_template('NotesView.html', error=error)
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

app.debug = True
app.secret_key = '\xd6;\xcc\xd8N\xf0\x11\x89k\x08\n~Eu\x01\x9c\x86\xc3\xae\x89 \xfa\x9a\x04'
if __name__ == '__main__':
    app.run()