from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'MYsuperSecretPa$$word2024'  

def get_db():
    db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database')

    db_path = os.path.join(db_dir, 'hw13.db')
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    return db

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    students = db.execute('SELECT * FROM students').fetchall()
    quizzes = db.execute('SELECT * FROM quizzes').fetchall()
    return render_template('dashboard.html', students=students, quizzes=quizzes)

@app.route('/student/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        try:
            db = get_db()
            db.execute('INSERT INTO students (first_name, last_name) VALUES (?, ?)',
                      [request.form['first_name'], request.form['last_name']])
            db.commit()
            return redirect(url_for('dashboard'))
        except:
            flash('Error adding student')
    return render_template('add_student.html')

@app.route('/quiz/add', methods=['GET', 'POST'])
@login_required
def add_quiz():
    if request.method == 'POST':
        try:
            db = get_db()
            db.execute('INSERT INTO quizzes (subject, num_questions, quiz_date) VALUES (?, ?, ?)',
                      [request.form['subject'], request.form['num_questions'], request.form['quiz_date']])
            db.commit()
            return redirect(url_for('dashboard'))
        except:
            flash('Error adding quiz')
    return render_template('add_quiz.html')

@app.route('/student/<int:id>')
@login_required
def student_results(id):
    db = get_db()
    results = db.execute('''
        SELECT r.score, q.subject, q.quiz_date 
        FROM results r 
        JOIN quizzes q ON r.quiz_id = q.id 
        WHERE r.student_id = ?''', [id]).fetchall()
    student = db.execute('SELECT * FROM students WHERE id = ?', [id]).fetchone()
    return render_template('student_results.html', results=results, student=student)

@app.route('/results/add', methods=['GET', 'POST'])
@login_required
def add_result():
    db = get_db()
    if request.method == 'POST':
        try:
            db.execute('INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)',
                      [request.form['student_id'], request.form['quiz_id'], request.form['score']])
            db.commit()
            return redirect(url_for('dashboard'))
        except:
            flash('Error adding result')
    
    students = db.execute('SELECT * FROM students').fetchall()
    quizzes = db.execute('SELECT * FROM quizzes').fetchall()
    return render_template('add_result.html', students=students, quizzes=quizzes)

if __name__ == '__main__':
    app.run(debug=True)