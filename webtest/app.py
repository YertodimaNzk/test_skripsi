# app.py
from flask import Flask, render_template, request, Response, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from gtts import gTTS
import io

app = Flask(__name__)
app.secret_key = 'test123'  # Ganti dengan secret key yang lebih aman

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
    return render_template('homepage.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
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
