import sqlite3

# Connect to the SQLite database (this will create the file if it doesn't exist)
conn = sqlite3.connect('workout_tracker.db')
cursor = conn.cursor()

# Define the schema for the 'exercises' and 'workouts' tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY,
        exercise_id INTEGER,
        date DATE,
        reps INTEGER,
        FOREIGN KEY (exercise_id) REFERENCES exercises (id)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database 'workout_tracker.db' and tables created successfully.")
