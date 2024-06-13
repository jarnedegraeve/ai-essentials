from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a random value
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database file

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validate password complexity
        if len(password) < 8:
            flash('Password should be at least 8 characters long.', 'danger')
        elif not re.search(r'[A-Z]', password):
            flash('Password should contain at least one uppercase letter.', 'danger')
        elif not re.search(r'\d', password):
            flash('Password should contain at least one number.', 'danger')
        else:
            # Hash the password
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            
            try:
                new_user = User(username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                
                flash('Registration successful. Please login.', 'success')
                return redirect(url_for('login'))
            
            except IntegrityError:
                db.session.rollback()
                flash('Username already exists. Please choose a different one.', 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
