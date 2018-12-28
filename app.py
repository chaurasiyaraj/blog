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
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    return render_template('Blog/index.html')

@app.route('/admin')
def index():
    return render_template('Admin/login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        # Add an user
        user = User(email="om@gmail.com", password='abcd')
        db.session.add(user)
        db.session.commit()
        print("Added user: ")

        # Get all user
        users = db.session.query(User).all()
        for user in users:
            print(user.email)
            print(user.password)
            print("==============")

        # Filter on the basis of email.
        user = db.session.query(User).filter_by(email='om@gmail.com').first()
        print("Filtered on the basis of user email, and password is: {}".format(user.password))

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


class User(db.Model):
    """
    Model to save the User.
    """
    __tablename__ = 'user'

    id = db.Column('id', db.Integer, nullable=False, primary_key=True)
    email = db.Column('email', db.String, nullable=False)
    password = db.Column('password', db.String, nullable=False)
