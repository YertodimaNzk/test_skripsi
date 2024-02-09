# app.py
from flask import Flask, render_template, request, Response, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from gtts import gTTS
import io



app = Flask(__name__)
app.secret_key = 'test123'  # Replace with a secure secret key

# Configure SQLite database
mysql_config = {
    "user": "root",
    "password": "",
    "host": "127.0.0.1",
    "port": "3306",
    "database": "test_skripsi",
}

# Configure MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{mysql_config['user']}:{mysql_config['password']}@{mysql_config['host']}:{mysql_config['port']}/{mysql_config['database']}?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable SQLAlchemy event system
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def process_signup():
    data = request.form
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if the username or email is already taken
    if User.query.filter_by(username=username).first():
        return 'Username already exists. Please choose a different username.'
    if User.query.filter_by(email=email).first():
        return 'Email already exists. Please use a different email address.'

    # Store the new user data in the database
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    # Redirect the user to the login page after successful signup
    return redirect(url_for('login'))

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password).first()

    if user:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        print("Invalid credentials.")
        return 'Invalid credentials.'

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))

    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    text_to_speak = data.get('text', '')

    # Use gTTS for text-to-speech
    tts = gTTS(text=text_to_speak, lang='id')

    # Stream the audio data directly to the client
    speech_stream = io.BytesIO()
    tts.write_to_fp(speech_stream)
    speech_stream.seek(0)

    return Response(speech_stream.read(), mimetype="audio/mp3")


if __name__ == '__main__':
    app.run(debug=True)
