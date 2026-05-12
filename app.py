import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "dev_secret_key"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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
        return redirect(url_for('todo'))
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
# BLOG ROUTING
# ------------------
@app.route('/blog')
def blog():
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
    posts = cursor.fetchall()
    conn.close()
    return render_template('blog.html', posts=posts)

@app.route('/blog/add', methods=['POST'])
def add_post():
    if 'username' not in session:
        return redirect(url_for('login'))
    title = request.form['title']
    content = request.form['content']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (username, title, content) VALUES (?,?,?)", (session['username'], title, content))
    conn.commit()
    conn.close()
    return redirect(url_for('blog'))

@app.route('/blog/post/<int:post_id>')
def view_post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    cursor.execute("SELECT * FROM comments WHERE post_id = ? ORDER BY created_at ASC", (post_id,))
    comments = cursor.fetchall()
    conn.close()
    return render_template('post.html', post=post, comments=comments)

@app.route('/blog/comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    comment = request.form['comment']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (post_id, username, comment) VALUES (?,?,?)", (post_id, session['username'], comment))
    conn.commit()
    conn.close()
    return redirect(url_for('view_post', post_id=post_id))

@app.route('/blog/delete/<int:post_id>')
def delete_post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    cursor.execute("DELETE FROM comments WHERE post_id = ?", (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('blog'))

# ------------------
# IMAGE UPLOAD ROUTING
# ------------------
@app.route('/notes')
def notes():
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM images WHERE username = ? ORDER BY uploaded_at DESC", (session['username'],))
    images = cursor.fetchall()
    conn.close()
    return render_template('notes.html', images=images)

@app.route('/notes/upload', methods=['POST'])
def upload_image():
    if 'username' not in session:
        return redirect(url_for('login'))
    if 'image' not in request.files:
        flash("No file selected!")
        return redirect(url_for('notes'))
    file = request.files['image']
    subject = request.form['subject']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO images (username, filename, subject) VALUES (?,?,?)", (session['username'], filename, subject))
        conn.commit()
        conn.close()
        flash("Image uploaded successfully!")
    else:
        flash("Invalid file type. Only png, jpg, jpeg, gif allowed.")
    return redirect(url_for('notes'))

@app.route('/notes/delete/<int:image_id>')
def delete_image(image_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM images WHERE id = ?", (image_id,))
    image = cursor.fetchone()
    if image:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], image['filename'])
        if os.path.exists(filepath):
            os.remove(filepath)
        cursor.execute("DELETE FROM images WHERE id = ?", (image_id,))
        conn.commit()
    conn.close()
    return redirect(url_for('notes'))

# ------------------
# RUN APP
# ------------------
if __name__ == '__main__':
    app.run(debug=True)