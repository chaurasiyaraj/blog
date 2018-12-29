from flask import Flask, redirect, url_for, request, render_template, make_response, session, abort, flash
from werkzeug import secure_filename
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key='Raj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'

db = SQLAlchemy()
db.init_app(app)
Migrate(app, db)


@app.route('/')
def home():
    #conn = sqlite3.connect('database.db')
    #print("Opened database successfully")
    return render_template('Blog/index.html')

@app.route('/admin')
def index():
    return render_template('Admin/login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Filter on the basis of email and password.
        user = db.session.query(User).filter_by(email=email, password=password).first()
        print (user)
        if hasattr(user, 'email'):
            session['logged_in'] = 1
            flash('You have logged In successfully')
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid Email/Password!'
    elif 'logged_in' in session:
        flash('You are already logged In')
        return redirect(url_for('dashboard'))
    return render_template('Admin/login.html', error=error)

@app.route('/dashboard')
def dashboard():
    return render_template('Admin/index.html')

@app.route('/categories')
def categories():
    categories={}
    return render_template('Admin/categories.html', categories=categories)

@app.route('/create_category', methods = ['POST', 'GET'])
def create_category():
    if request.method == 'POST':
        # Add a category
        name = request.form['name']
        description = request.form['description']
        status = request.form['status']
        category = Category(name=name, description=description, status=status)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('Admin/create_category.html')

@app.route('/edit_category', methods=['POST', 'GET'])
def edit_category():
    if request.method == 'POST':
        return redirect(url_for('categories'))
    return render_template('Admin/create_category.html', category=category)

@app.route('/posts')
def posts():
    posts={}
    return render_template('Admin/posts.html', posts=posts)

@app.route('/create_post', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        # Add a category
        name = request.form['name']
        description = request.form['description']
        status = request.form['status']
        category = Category(name=name, description=description, status=status)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('posts'))
    return render_template('Admin/create_post.html')

@app.route('/edit_post', methods=['POST', 'GET'])
def edit_post():
    if request.method == 'POST':
        return redirect(url_for('posts'))
    return render_template('Admin/create_post.html', post=post)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


class User(db.Model):
    """
    Model to save the User.
    """
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, nullable=False, primary_key=True)
    name = db.Column('name', db.String, nullable=False)
    email = db.Column('email', db.String, nullable=False)
    password = db.Column('password', db.String, nullable=False)
    role = db.Column('role', db.Integer, nullable=False)
    status = db.Column('status', db.String, nullable=False)

class Category(db.Model):
    """
    Model to save the Category.
    """
    __tablename__ = 'category'

    id = db.Column('id', db.Integer, nullable=False, primary_key=True)
    name = db.Column('name', db.String, nullable=False)
    email = db.Column('description', db.String, nullable=False)
    status = db.Column('status', db.Integer, nullable=False)

class Post(db.Model):
    """
    Model to save the Post.
    """
    __tablename__ = 'posts'

    id = db.Column('id', db.Integer, nullable=False, primary_key=True)
    name = db.Column('title', db.String, nullable=False)
    email = db.Column('body', db.String, nullable=False)
    category_id = db.Column('category_id', db.Integer, nullable=False)
    status = db.Column('status', db.Integer, nullable=False)
