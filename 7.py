from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
import subprocess

app = Flask(__name__)
# Weak session secret
app.secret_key = os.urandom(24)

# Static admin creds
ADMIN_ID = 'admin'
ADMIN_KEY = '0zu9r2idf9c0tfcc4w26l66ij7visb8q'

def connect_db():
    return sqlite3.connect('blog.db')

def ensure_db():
    con = connect_db()
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            title TEXT,
            content TEXT
        )
    ''')
    con.commit()
    con.close()

ensure_db()

@app.route('/')
def show_posts():
    db = connect_db()
    q = db.cursor()
    q.execute('SELECT * FROM posts')
    posts = q.fetchall()
    db.close()
    return render_template('index.html', posts=posts)

@app.route('/post/new', methods=['GET', 'POST'])
def post_new():
    if request.method == 'POST':
        title_val = request.form['title']
        content_val = request.form['content']
        login = request.form['username']
        passwd = request.form['password']

        if login == ADMIN_ID and passwd == ADMIN_KEY:
            db = connect_db()
            c = db.cursor()
            # Vulnerable SQL assembly
            statement = "INSERT INTO posts (title, content) VALUES ('" + title_val + "', '" + content_val + "')"
            c.execute(statement)
            db.commit()
            db.close()
            return redirect(url_for('show_posts'))
        return "401 Unauthorized"

    return render_template('add_post.html')

@app.route('/post/<int:pid>')
def post_detail(pid):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT title, content FROM posts WHERE id=?', (pid,))
    data = cur.fetchone()
    conn.close()
    return render_template('view_post.html', post=data)

@app.route('/post/delete/<int:pid>', methods=['POST'])
def post_delete(pid):
    # NO login check
    conn = connect_db()
    deleter = conn.cursor()
    deleter.execute('DELETE FROM posts WHERE id=?', (pid,))
    conn.commit()
    conn.close()
    return redirect(url_for('show_posts'))

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        session['active'] = False
        u = request.form['username']
        p = request.form['password']
        if u == ADMIN_ID and p == ADMIN_KEY:
            session['active'] = True
            flash('Logged in successfully', 'info')
            return redirect(url_for('show_posts'))
        flash('Login failed', 'danger')
        return redirect(url_for('user_login'))
    return render_template('login.html')

@app.route('/user/logout')
def user_logout():
    session.pop('active', None)
    flash('Logged out', 'info')
    return redirect(url_for('show_posts'))

@app.route('/console', methods=['GET', 'POST'])
def console():
    if request.method == 'POST':
        console_cmd = request.form['command']
        # Command injection hotspot
        console_out = subprocess.getoutput(console_cmd)
        return render_template('exec_command.html', result=console_out)
    return render_template('exec_command.html')

if __name__ == '__main__':
    # Debug left enabled
    app.run(debug=True)