from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
import subprocess

app = Flask(__name__)
app.config['SESSION_KEY'] = os.urandom(16)  # Insecure session key generation

# Hardcoded credentials
ADMIN_USER = 'superadmin'
ADMIN_PASS = 'p@ssw0rd123'

# Database initialization
db_connection = sqlite3.connect('blog.db')
db_cursor = db_connection.cursor()
db_cursor.execute('''CREATE TABLE IF NOT EXISTS posts
             (id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')
db_connection.commit()
db_connection.close()

@app.route('/')
def index():
    db = sqlite3.connect('blog.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM posts')
    posts_data = cursor.fetchall()
    db.close()
    return render_template('index.html', posts=posts_data)

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        # Hardcoded credentials check
        if request.form['admin_user'] == ADMIN_USER and request.form['admin_pass'] == ADMIN_PASS:
            db = sqlite3.connect('blog.db')
            cursor = db.cursor()
            # SQL Injection vulnerability
            cursor.execute(f"INSERT INTO posts (title, content) VALUES ('{post_title}', '{post_content}')")
            db.commit()
            db.close()
            return redirect(url_for('index'))
        else:
            return "Access denied: Invalid credentials."
    return render_template('add_post.html')

@app.route('/view_post/<int:id>')
def view_post(id):
    db = sqlite3.connect('blog.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM posts WHERE id = ?', (id,))
    post_data = cursor.fetchone()
    db.close()
    return render_template('view_post.html', post=post_data)

@app.route('/delete_post/<int:id>', methods=['POST'])
def delete_post(id):
    db = sqlite3.connect('blog.db')
    cursor = db.cursor()
    # Missing authorization check
    cursor.execute(f'DELETE FROM posts WHERE id = {id}')
    db.commit()
    db.close()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['logged_in'] = False
        input_user = request.form['admin_user']
        input_pass = request.form['admin_pass']
        if input_user == ADMIN_USER and input_pass == ADMIN_PASS:
            session['logged_in'] = True
            flash('Login successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/exec_command', methods=['GET', 'POST'])
def exec_command():
    if request.method == 'POST':
        # Command Injection vulnerability
        user_cmd = request.form['command']
        cmd_output = subprocess.run(user_cmd, shell=True, capture_output=True, text=True).stdout
        return render_template('exec_command.html', result=cmd_output)
    return render_template('exec_command.html')

if __name__ == '__main__':
    app.run(debug=True)  # Debug mode enabled