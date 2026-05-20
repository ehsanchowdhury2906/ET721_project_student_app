# Student Learning Management App

A full-stack Flask web app that helps students manage tasks, share blog posts, and organize notes.

## Project Structure
ET721_project_student_app/
├── app.py                  Flask application: routes, DB
├── README.md               Current file
├── students.db             SQLite database
│
├── static/
│   ├── style.css           All page styles
│   ├── script.js           JavaScript for flash auto-dismiss, delete confirmations, and image preview
│   └── uploads/            Stored uploaded images
│
└── templates/
    ├── base.html           Shared layout with navbar and footer
    ├── login.html          Login form
    ├── signup.html         Registration form
    ├── dashboard.html      Dashboard with feature navigation
    ├── todo.html           Per-user to-do list with add/complete/delete
    ├── blog.html           Blog feed with add/delete
    ├── post.html           Single post with comments and likes
    ├── notes.html          Image upload with preview and download
    └── profile.html        User activity stats

## Setup and Installation

### Prerequisites
- Python 3.10+
- pip

### 1. Clone or download the project
cd ET721_project_student_app

### 2. Install dependencies
pip install flask werkzeug

### 3. Set up the database
sqlite3 students.db
Create the required tables for users, tasks, posts, comments, images, and likes, then exit with .quit

## Running the Application

Make sure you are in the project directory, then run:
python app.py

Flask will start the server at http://127.0.0.1:5000 — open that in your browser.
The app will redirect you to the login page. Sign up for an account to get started.

## Stopping the Server
Ctrl+C in the terminal running python app.py

## Resetting the Database
Stop the server, delete students.db and optionally static/uploads/, then follow the database setup steps again.

