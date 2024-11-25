CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

CREATE TABLE quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    num_questions INTEGER NOT NULL,
    quiz_date DATE NOT NULL
);

CREATE TABLE results (
    student_id INTEGER,
    quiz_id INTEGER,
    score INTEGER CHECK(score >= 0 AND score <= 100),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id),
    PRIMARY KEY (student_id, quiz_id)
);