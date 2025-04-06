import sqlite3
from datetime import datetime, timedelta

DB_PATH = 'db.sqlite3'

def insert_test_data_hausa():
    """
    Inserts 5 test entries in Hausa language into the tts_history table.
    Creates the table if it doesn't exist.
    """
    
    hausa_test_data = [
        ("Ina kwana? Yaya lafiya?", "ina_kwana.mp3"),
        ("Barka da safiya!", "barka_safiya.mp3"),
        ("Me sunan ka?", "sunan_ka.mp3"),
        ("Na gode sosai", "nagode.mp3"),
        ("Zan iya taimaka?", "taimako.mp3")
    ]
    
    with sqlite3.connect(DB_PATH) as conn:
        # Create table if it doesn't exist
        conn.execute('''
        CREATE TABLE IF NOT EXISTS tts_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            audio_file TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Get current timestamp and create timestamps for the past 4 days
        now = datetime.now()
        timestamps = [now - timedelta(days=i) for i in range(5)]
        
        # Insert each Hausa entry with a different timestamp
        for i, (text, audio_file) in enumerate(hausa_test_data):
            conn.execute('''
            INSERT INTO tts_history (text, audio_file, timestamp)
            VALUES (?, ?, ?)
            ''', (text, audio_file, timestamps[i].strftime('%Y-%m-%d %H:%M:%S')))
        
        conn.commit()
        print("Successfully inserted 5 Hausa test entries into the database.")

# Example usage
insert_test_data_hausa()