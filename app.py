from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'db.sqlite3'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tts_history (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            text TEXT NOT NULL,
                            audio_file TEXT NOT NULL,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        )''')

def get_all_history():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT id, text FROM tts_history ORDER BY id DESC").fetchall()

@app.route('/')
def new_text():
    history = get_all_history()
    return render_template('new_text.html', history=history)

@app.route('/submit', methods=['POST'])
def submit_text():
    text = request.form['hausa_text']
    
    # Sanitize and shorten base name from text
    filename_base = text.strip().replace(' ', '_')[:20]
    
    # Add timestamp for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_base}_{timestamp}.mp3"
    
    # Full path
    audio_path = os.path.join('static', 'audio', filename)
    
    # Create dummy audio file
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    with open(audio_path, 'wb') as f:
        f.write(b'\0')

    # Save to DB
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO tts_history (text, audio_file) VALUES (?, ?)", (text, audio_path))
    
    return redirect(url_for('new_text'))


@app.route('/history/<int:item_id>')
def view_history(item_id):
    history = get_all_history()
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("SELECT text, audio_file, timestamp FROM tts_history WHERE id = ?", (item_id,)).fetchone()
    return render_template('history.html', item=row, history=history)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
