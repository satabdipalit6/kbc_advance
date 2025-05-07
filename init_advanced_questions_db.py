# init_advanced_questions_db.py

import sqlite3

conn = sqlite3.connect('questions.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS quiz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT,
    option4 TEXT,
    correct_answer TEXT,
    difficulty TEXT
)
''')

# Add questions (you should add 50+ with different difficulties)
questions_data = [
    ("What is the capital of France?", "Paris", "Berlin", "Rome", "Madrid", "Paris", "Easy"),
    ("Which planet is known as the Red Planet?", "Mars", "Earth", "Venus", "Jupiter", "Mars", "Easy"),
    ("What is the boiling point of water?", "90°C", "100°C", "80°C", "120°C", "100°C", "Easy"),
    ("Who developed the theory of relativity?", "Newton", "Tesla", "Einstein", "Darwin", "Einstein", "Medium"),
    ("What is the square root of 256?", "14", "16", "18", "20", "16", "Medium"),
    ("What is the capital of Australia?", "Sydney", "Melbourne", "Canberra", "Perth", "Canberra", "Hard"),
    ("What is the hardest natural substance?", "Gold", "Diamond", "Platinum", "Iron", "Diamond", "Hard")
    # Add more...
]

cursor.executemany("INSERT INTO quiz (question, option1, option2, option3, option4, correct_answer, difficulty) VALUES (?, ?, ?, ?, ?, ?, ?)", questions_data)

conn.commit()
conn.close()
