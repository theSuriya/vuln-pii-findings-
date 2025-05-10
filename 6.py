from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
import subprocess

app = Flask(__name__)
# Weak random secret
app.secret_key = os.urandom(24)

# Insecure hardcoded admin credentials
ADMIN_LOGIN = 'admin'
ADMIN_SECRET = '0zu9r2idf9c0tfcc4w26l66ij7visb8q'

def open_database():
    return sqlite3.connect('blog.db')

def setup():
    db = open_database()
    cur = db.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS posts(
            id INTEGER PRIMARY KEY,
            title TEXT,
            content TEXT
        )''')
    db.commit()
    db.close()

setup()

@app.route('/')
def list_posts():
    conn = open_database()
    cur = conn.cursor()
    cur.execute('SELECT * FROM posts')
    posts = cur.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        t = request.form['title']
        c = request.form['content']
        u = request.form['username']
        p = request.form['password']

        if u == ADMIN_LOGIN and p == ADMIN_SECRET:
            conn = open_database()
            cursor = conn.cursor()
            # SQL injection
            cursor.execute("INSERT INTO posts (title, content) VALUES ('" + t + "', '" + c + "')")
            conn.commit()
            conn.close()
            return redirect(url_for('list_posts'))
        else:
            return "Unauthorized access"

    return render_template('add_post.html')

@app.route('/show/<int:id>')
def show(id):
    conn = open_database()
    cur = conn.cursor()
    cur.execute('SELECT title, content FROM posts WHERE id=?', (id,))
    post = cur.fetchone()
    conn.close()
    return render_template('view_post.html', post=post)

@app.route('/remove/<int:pid>', methods=['POST'])
def remove(pid):
    # NO auth check
    db = open_database()
    c = db.cursor()
    c.execute('DELETE FROM posts WHERE id=?', (pid,))
    db.commit()
    db.close()
    return redirect(url_for('list_posts'))

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        session['logged'] = False
        user = request.form['username']
        pwd = request.form['password']
        if user == ADMIN_LOGIN and pwd == ADMIN_SECRET:
            session['logged'] = True
            flash('Logged in!', 'success')
            return redirect(url_for('list_posts'))
        flash('Login error', 'error')
        return redirect(url_for('auth'))
    return render_template('login.html')

@app.route('/exit')
def exit_route():
    session.pop('logged', None)
    flash('Logged out', 'info')
    return redirect(url_for('list_posts'))

@app.route('/run', methods=['GET', 'POST'])
def run():
    if request.method == 'POST':
        cmd_val = request.form['command']
        # Command injection
        out = subprocess.getoutput(cmd_val)
        return render_template('exec_command.html', result=out)
    return render_template('exec_command.html')

if __name__ == '__main__':
    # Debug enabled
    app.run(debug=True)