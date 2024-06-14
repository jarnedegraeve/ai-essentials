from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
import re
import openai
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

endpoint = os.getenv("ENDPOINT")
api_key = os.getenv("API_KEY")
deployment = "aiesschatimplementatie"

client = openai.AzureOpenAI(
    base_url=f"{endpoint}/openai/deployments/{deployment}/extensions",
    api_key=api_key,
    api_version="2023-08-01-preview",
)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if len(password) < 8:
            flash('Password should be at least 8 characters long.', 'danger')
        elif not re.search(r'[A-Z]', password):
            flash('Password should contain at least one uppercase letter.', 'danger')
        elif not re.search(r'\d', password):
            flash('Password should contain at least one number.', 'danger')
        else:
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
    if 'chat_messages' not in session:
        session['chat_messages'] = []

    return render_template('dashboard.html', username=current_user.username, chat_messages=session['chat_messages'])

@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    message = request.form['message']
    
    # Send user message to the chatbot
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "Assistant is an intelligent chatbot designed to help users answer their erasmushogeschool brussel questions. Instructions: - Only answer questions related to erasmushogeschool Brussel. - If you're unsure of an answer, you can say 'I don't know' or 'I'm not sure' and recommend users to mail their question to help@ehb.be."},
            {"role": "user", "content": message},
        ],
        extra_body={
            "dataSources": [
                {
                    "type": "AzureCognitiveSearch",
                    "parameters": {
                        "endpoint": os.getenv("SEARCH_ENDPOINT"),
                        "key": os.getenv("SEARCH_KEY"),
                        "indexName": "aiessdatatobot-index"
                    }
                }
            ]
        }
    )

    # Extract the content of the bot response
    bot_response_content = response.choices[0].message.content

    # Store the user message and bot response in chat_messages
    chat_messages = session.get('chat_messages', [])
    chat_messages.append({"role": "user", "content": message})
    chat_messages.append({"role": "bot", "content": bot_response_content})
    session['chat_messages'] = chat_messages
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
