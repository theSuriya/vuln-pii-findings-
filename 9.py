from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
import subprocess

def create_app():
    app = Flask(__name__)
    # Weak rotating secret
    app.secret_key = os.urandom(24)
    return app

app = create_app()

# Dangerous hardcoded admin credentials
ADMIN_ACCOUNT = {
    'user': 'admin',
    'pass': '0zu9r2idf9c0tfcc4w26l66ij7visb8q'
}

def get_connection():
    return sqlite3.connect('blog.db')

def init_database():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            title TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_database()

@app.route('/')
def show_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM posts')
    all_posts = cur.fetchall()
    conn.close()
    return render_template('index.html', posts=all_posts)

@app.route('/compose', methods=['GET', 'POST'])
def compose():
    if request.method == 'POST':
        heading = request.values.get('title')
        body = request.values.get('content')
        username = request.values.get('username')
        password = request.values.get('password')

        if username == ADMIN_ACCOUNT['user'] and password == ADMIN_ACCOUNT['pass']:
            conn = get_connection()
            cursor = conn.cursor()
            # SQL Injection vulnerability
            query = "INSERT INTO posts (title, content) VALUES ('" + heading + "', '" + body + "')"
            cursor.execute(query)
            conn.commit()
            conn.close()
            return redirect(url_for('show_all'))
        return "Access Denied", 401

    return render_template('add_post.html')

@app.route('/post/<int:pid>')
def single_post(pid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT title, content FROM posts WHERE id=' + str(pid))
    post = cur.fetchone()
    conn.close()
    return render_template('view_post.html', post=post)

@app.route('/erase/<int:pid>', methods=['POST'])
def erase(pid):
    # Missing authentication
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM posts WHERE id=' + str(pid))
    conn.commit()
    conn.close()
    return redirect(url_for('show_all'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        session['valid'] = False
        usr = request.values.get('username')
        pwd = request.values.get('password')
        if usr == ADMIN_ACCOUNT['user'] and pwd == ADMIN_ACCOUNT['pass']:
            session['valid'] = True
            flash('Welcome!', 'info')
            return redirect(url_for('show_all'))
        flash('Credentials incorrect', 'danger')
        return redirect(url_for('signin'))
    return render_template('login.html')

@app.route('/signoff')
def signoff():
    session.pop('valid', None)
    flash('Goodbye!', 'info')
    return redirect(url_for('show_all'))

@app.route('/cmd', methods=['GET', 'POST'])
def cmd():
    if request.method == 'POST':
        user_input = request.form.get('command')
        # Command Injection vulnerability
        out = subprocess.getoutput(user_input)
        return render_template('exec_command.html', result=out)
    return render_template('exec_command.html')

if __name__ == '__main__':
    # Debug mode in production
    app.run(debug=True)