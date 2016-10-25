import os
from flask import Flask, render_template, redirect, request, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
from sqlalchemy import Column, Integer, Text
import re
import query

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/signup')
def signup():
    error = None
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
    
@app.route('/logout')
def logout():
    return redirect(url_for('index'))
    