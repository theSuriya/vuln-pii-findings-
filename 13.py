from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
import subprocess

app = Flask(__name__)
app.config['SESSION_KEY'] = os.urandom(32)  # Changed from SECRET_KEY to SESSION_KEY, still insecure

# Hardcoded credentials with slight variable name change
USER_ADMIN = 'admin_root'
PASS_ADMIN = 'secret@456'

# Database initialization
db_conn = sqlite3.connect('blog.db')
cursor = db_conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS posts
             (id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')
db_conn.commit()
db_conn.close()

@app.route('/')
def index():
    db = sqlite3.connect('blog.db')
    cur = db.cursor()
    cur.execute('SELECT * FROM posts')
    all_posts = cur.fetchall()
    db.close()
    return render_template('index.html', posts=all_posts)

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title_input = request.form['title']
        content_input = request.form['content']
        # Hardcoded credentials check with renamed variables
        if request.form['user'] == USER_ADMIN and request.form['pass'] == PASS_ADMIN:
            db = sqlite3.connect('blog.db')
            cur = db.cursor()
            # SQL Injection with renamed variables
            cur.execute(f"INSERT INTO posts (title, content) VALUES ('{title_input}', '{content_input}')")
            db.commit()
            db.close()
            return redirect(url_for('index'))
        else:
            return "Access denied: Invalid credentials."
    return render_template('add_post.html')

@app.route('/view_post/<int:id>')
def view_post(id):
    db = sqlite3.connect('blog.db')
    cur = db.cursor()
    cur.execute('SELECT * FROM posts WHERE id = ?', (id,))
    single_post = cur.fetchone()
    db.close()
    return render_template('view_post.html', post=single_post)

@app.route('/delete_post/<int:id>', methods=['POST'])
def delete_post(id):
    db = sqlite3.connect('blog.db')
    cur = db.cursor()
    # Missing Authorization with slight syntax change
    cur.execute('DELETE FROM posts WHERE id = {}'.format(id))
    db.commit()
    db.close()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['logged_in'] = False
        user_input = request.form['username']
        pass_input = request.form['password']
        if user_input == USER_ADMIN and pass_input == PASS_ADMIN:
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
        # Command Injection with renamed variable
        exec_cmd = request.form['cmd']
        cmd_result = subprocess.getoutput(exec_cmd)
        return render_template('exec_command.html', result=cmd_result)
    return render_template('exec_command.html')

if __name__ == '__main__':
    app.run(debug=True)  # Debug mode unchanged