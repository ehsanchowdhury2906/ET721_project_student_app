# Student Learning Management App

A full-stack Flask web app that helps students manage tasks, share blog posts, and organize notes.

## Features
- User login and registration
- To-Do list with categories and completion tracking
- Blog with comments
- Image upload for notes with preview and download
- Profile page with activity stats

## Project Files
- app.py — Main Flask application and all routes
- students.db — SQLite database
- static/style.css — All app styling
- static/script.js — JavaScript
- static/uploads/ — Stores uploaded note images
- templates/base.html — Base layout with navbar and footer
- templates/login.html — Login page
- templates/signup.html — Registration page
- templates/dashboard.html — Main dashboard
- templates/todo.html — To-Do list
- templates/blog.html — Blog posts
- templates/post.html — Single post with comments
- templates/notes.html — Image upload and preview
- templates/profile.html — User activity stats

## Setup
1. Install dependencies: pip install flask werkzeug
2. Run the app: python app.py
3. Go to http://127.0.0.1:5000

## Tech Stack
- Backend: Flask, Python
- Frontend: HTML, CSS
- Database: SQLite