# Student Learning Management App

A full-stack Flask web app that helps students manage tasks, share blog posts, and organize notes.

## Project Structure
- app.py — Main Flask application and all routes
- students.db — SQLite database
- static/style.css — All app styling
- static/script.js — JavaScript for flash messages, delete confirmations, and image preview
- static/uploads/ — Stores uploaded note images
- templates/base.html — Base layout with navbar and footer
- templates/login.html — Login page
- templates/signup.html — Registration page
- templates/dashboard.html — Main dashboard
- templates/todo.html — To-Do list
- templates/blog.html — Blog posts
- templates/post.html — Single post with comments and likes
- templates/notes.html — Image upload and preview
- templates/profile.html — User activity stats

## Setup and Installation

### Prerequisites
- Python 3.10+
- pip

### 1. Clone the repository
cd ET721_project_student_app

### 2. Install dependencies
pip install flask werkzeug

### 3. Set up the database
Run sqlite3 students.db and create the required tables for users, tasks, posts, comments, images, and likes. Then exit with .quit

### 4. Run the app
python app.py

it'll give you a prompt, click on it and open it in your browser. The root path redirects to the login page. Create an account using the Sign Up page to get started.

## Stopping the Server
Press Ctrl+C in the terminal.

## Resetting the Database
Stop the server, delete students.db and optionally static/uploads/, then follow the database setup steps again.

## Tech Stack
- Backend: Flask, Python
- Frontend: HTML, CSS, JavaScript
- Database: SQLite



