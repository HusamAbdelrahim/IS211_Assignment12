import sqlite3
import os

def setup_db():
    # Get the path to the db
    db_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(db_dir, 'hw13.db')
    schema_path = os.path.join(db_dir, 'schema.sql')
    
    # create database and execute schema
    with sqlite3.connect(db_path) as db:
        with open(schema_path, 'r') as f:
            db.executescript(f.read())
        
        # insert sample data
        db.execute('''
            INSERT INTO students (first_name, last_name) 
            VALUES (?, ?)''', ['John', 'Smith'])
        
        db.execute('''
            INSERT INTO quizzes (subject, num_questions, quiz_date) 
            VALUES (?, ?, ?)''', ['Python Basics', 5, '2015-02-05'])
        
        # get the IDs of the inserted records
        student_id = db.execute('SELECT id FROM students WHERE first_name = ? AND last_name = ?', 
                              ['John', 'Smith']).fetchone()[0]
        quiz_id = db.execute('SELECT id FROM quizzes WHERE subject = ?', 
                           ['Python Basics']).fetchone()[0]
        
        # insert the quiz result
        db.execute('''
            INSERT INTO results (student_id, quiz_id, score) 
            VALUES (?, ?, ?)''', [student_id, quiz_id, 85])
        
        db.commit()

if __name__ == '__main__':
    setup_db()