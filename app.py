import os
import re
from flask import Flask, render_template, redirect, request, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
from sqlalchemy import Column, Integer, Text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ggadmin:admin@localhost/glibglab"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import User

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
        _username = request.form['username']
        _password = request.form['password']
        _password_confirm = request.form['password_confirm']
        _email = request.form['email']
        _fullname = request.form['fullname']
        _soi = request.form['soi']
        _agree = request.form['agree']
        if db.session.query(User).filter(User.username == _username).scalar() is None:
            if _password == _password_confirm:
                if _agree == ['agree1']:
                    new_user = User(_username, _password, _email, _fullname, _soi)
    return render_template('signup.html', error=error)

@app.route('/login')
def login():
    error = None
    return render_template('login.html', error=error)

@app.route('/reset')
def reset():
    error = None
    return render_template('forgotpassword.html', error=error)

@app.route('/teacher')
def teacher():
    error = None
    return render_template('TeacherView.html', error=error)

@app.route('/class')
def classview():
    error = None
    return render_template('ClassView.html', error=error)
    
@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()