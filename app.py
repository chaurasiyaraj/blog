from flask import Flask, redirect, url_for, request, render_template, make_response, session, abort, flash
from werkzeug import secure_filename
#from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.secret_key='Raj'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'

@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    return render_template('Blog/index.html')

@app.route('/admin')
def index():
    return render_template('Admin/login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('Admin/login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('Admin/index.html')

@app.route('/categories')
def categories():
    categories={}
    return render_template('Admin/categories.html', categories=categories)

@app.route('/create_category')
def create_category():
    if request.method == 'POST':
        return redirect(url_for('categories'))
    return render_template('Admin/create_category.html')

@app.route('/edit_category')
def edit_category():
    if request.method == 'POST':
        return redirect(url_for('categories'))
    return render_template('Admin/create_category.html', category=category)

@app.route('/posts')
def posts():
    posts={}
    return render_template('Admin/posts.html', posts=posts)

@app.route('/create_post')
def create_post():
    if request.method == 'POST':
        return redirect(url_for('posts'))
    return render_template('Admin/create_post.html')

@app.route('/edit_post')
def edit_post():
    if request.method == 'POST':
        return redirect(url_for('posts'))
    return render_template('Admin/create_post.html', post=post)


@app.route('/logout')
def logout():
    return redirect(url_for('login'))