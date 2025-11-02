# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Post
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')

# Database configuration (sqlite in project folder)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'koho_connect.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB (db object from models.py)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post', methods=['POST'])
def post():
    name = request.form.get('name')
    message = request.form.get('message')
    post_type = request.form.get('type')

    if not name or not message:
        flash('Please enter your name and message.')
        return redirect(url_for('index'))

    new_post = Post(name=name, message=message, type=post_type)
    db.session.add(new_post)
    db.session.commit()
    flash('Post submitted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
