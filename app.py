import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "dev_secret_key"

# ------------------
# DATABASE CONNECTION
# ------------------
def get_db():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn

# ------------------
# LOADING PAGE
# ------------------
@app.route('/')
def home():
    return redirect(url_for('login'))

# ------------------
# LOGIN ROUTING
# ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password")
    return render_template("login.html")

# ------------------
# DASHBOARD ROUTING
# ------------------
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

# ------------------
# LOGOUT ROUTING
# ------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ------------------
# SIGNUP ROUTING
# ------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (username, email, password))
            conn.commit()
            flash("Account created successfully!")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Email already exists!")
        finally:
            conn.close()
    return render_template('signup.html')

# ------------------
# TO-DO ROUTING
# ------------------
@app.route('/todo')
def todo():
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE username = ?", (session['username'],))
    tasks = cursor.fetchall()
    conn.close()
    return render_template('todo.html', tasks=tasks)

@app.route('/todo/add', methods=['POST'])
def add_task():
    if 'username' not in session:
        return redirect(url_for('login'))
    task = request.form['task']
    category = request.form['category']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (username, task, category, completed) VALUES (?,?,?,0)", (session['username'], task, category))
    conn.commit()
    conn.close()
    return redirect(url_for('todo'))

@app.route('/todo/complete/<int:task_id>')
def complete_task(task_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('todo'))

@app.route('/todo/delete/<int:task_id>')
def delete_task(task_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('todo'))

# ------------------
# RUN APP
# ------------------
if __name__ == '__main__':
    app.run(debug=True)