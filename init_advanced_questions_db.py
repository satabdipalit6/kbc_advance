# init_advanced_questions_db.py

import pymysql

# Establish a connection to the MySQL database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='questions'
)
cursor = conn.cursor()

# Create the 'quiz' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS quiz (
        id INT AUTO_INCREMENT PRIMARY KEY,
        question TEXT,
        option1 TEXT,
        option2 TEXT,
        option3 TEXT,
        option4 TEXT,
        correct_answer TEXT,
        difficulty VARCHAR(10)
    )
''')

# List of questions to insert
questions_data = [
    ("What is the capital of France?", "Paris", "Berlin", "Rome", "Madrid", "Paris", "Easy"),
    ("Which planet is known as the Red Planet?", "Mars", "Earth", "Venus", "Jupiter", "Mars", "Easy"),
    ("What is the boiling point of water?", "90°C", "100°C", "80°C", "120°C", "100°C", "Easy"),
    ("Who developed the theory of relativity?", "Newton", "Tesla", "Einstein", "Darwin", "Einstein", "Medium"),
    ("What is the square root of 256?", "14", "16", "18", "20", "16", "Medium"),
    ("What is the capital of Australia?", "Sydney", "Melbourne", "Canberra", "Perth", "Canberra", "Hard"),
    ("What is the hardest natural substance?", "Gold", "Diamond", "Platinum", "Iron", "Diamond", "Hard")
    # Add more questions as needed
]

# SQL statement with correct placeholders
sql = '''
    INSERT INTO quiz (question, optionA, optionB, optionC, optionD, correctOption, difficulty)
    VALUES (%s, %s, %s, %s, %s, %s, %s)'''

# Execute the insertion of multiple records
cursor.executemany(sql, questions_data)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()
