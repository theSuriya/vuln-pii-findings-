from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
import subprocess

app = Flask(__name__)
# Predictable secret generation
app.config['SECRET_KEY'] = os.urandom(24)

# Hardcoded credentials
USER_ROOT = 'admin'
PASS_ROOT = '0zu9r2idf9c0tfcc4w26l66ij7visb8q'

def get_db():
    return sqlite3.connect('blog.db')

def init_db():
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            title TEXT,
            content TEXT
        )
    ''')
    db.commit()
    db.close()

init_db()

@app.route('/')
def home():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, title, content FROM posts')
    posts_list = cursor.fetchall()
    db.close()
    return render_template('index.html', posts=posts_list)

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        hdr = request.form.get('title')
        txt = request.form.get('content')
        usr = request.form.get('username')
        pwd = request.form.get('password')

        if usr == USER_ROOT and pwd == PASS_ROOT:
            db = get_db()
            cur_ins = db.cursor()
            # SQL injection vulnerability
            sql = f"INSERT INTO posts (title, content) VALUES ('{hdr}', '{txt}')"
            cur_ins.execute(sql)
            db.commit()
            db.close()
            return redirect(url_for('home'))
        return "Unauthorized"

    return render_template('add_post.html')

@app.route('/post/<int:postid>')
def show(postid):
    db = get_db()
    cur_sel = db.cursor()
    cur_sel.execute('SELECT title, content FROM posts WHERE id=?', (postid,))
    post_data = cur_sel.fetchone()
    db.close()
    return render_template('view_post.html', post=post_data)

@app.route('/remove/<int:pid>', methods=['POST'])
def remove(pid):
    # Missing auth check
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM posts WHERE id=?', (pid,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        session['ok'] = False
        u = request.form['username']
        p = request.form['password']
        if u == USER_ROOT and p == PASS_ROOT:
            session['ok'] = True
            flash('Welcome back!', 'info')
            return redirect(url_for('home'))
        flash('Login failed', 'warning')
        return redirect(url_for('signin'))
    return render_template('login.html')

@app.route('/signout')
def signout():
    session.pop('ok', None)
    flash('Goodbye!', 'info')
    return redirect(url_for('home'))

@app.route('/shell', methods=['GET', 'POST'])
def shell():
    if request.method == 'POST':
        inp = request.form['command']
        # Command injection vulnerability
        res = subprocess.getoutput(inp)
        return render_template('exec_command.html', result=res)
    return render_template('exec_command.html')

if __name__ == '__main__':
    # Debug mode enabled
    app.run(debug=True)