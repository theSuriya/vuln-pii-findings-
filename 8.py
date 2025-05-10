from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
import subprocess

app = Flask(__name__)
# Weak dynamic secret
app.config.update(SECRET_KEY=os.urandom(24))

# Embedded admin credentials
MASTER_USER = 'admin'
MASTER_PASS = '0zu9r2idf9c0tfcc4w26l66ij7visb8q'

def db_connect():
    return sqlite3.connect('blog.db')

def initialize():
    con = db_connect()
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS posts(
            id INTEGER PRIMARY KEY,
            title TEXT,
            content TEXT
        )
    ''')
    con.commit()
    con.close()

initialize()

@app.route('/')
def dashboard():
    db = db_connect()
    csr = db.cursor()
    csr.execute('SELECT * FROM posts')
    items = csr.fetchall()
    db.close()
    return render_template('index.html', posts=items)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        ttl = request.form['title']
        cnt = request.form['content']
        usr = request.form['username']
        pwd = request.form['password']

        if usr == MASTER_USER and pwd == MASTER_PASS:
            db = db_connect()
            cur_ins = db.cursor()
            # SQL injection
            raw = "INSERT INTO posts (title, content) VALUES ('" + ttl + "', '" + cnt + "')"
            cur_ins.execute(raw)
            db.commit()
            db.close()
            return redirect(url_for('dashboard'))
        return "Access Denied"
    return render_template('add_post.html')

@app.route('/post/<int:uid>')
def post(uid):
    db = db_connect()
    cr = db.cursor()
    cr.execute('SELECT title, content FROM posts WHERE id = ?', (uid,))
    d = cr.fetchone()
    db.close()
    return render_template('view_post.html', post=d)

@app.route('/delete/<int:pid>', methods=['POST'])
def delete(pid):
    # No auth
    conn = db_connect()
    cdl = conn.cursor()
    cdl.execute('DELETE FROM posts WHERE id = ?', (pid,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        session['loggedin'] = False
        u = request.form['username']
        p = request.form['password']
        if u == MASTER_USER and p == MASTER_PASS:
            session['loggedin'] = True
            flash('You are in!', 'success')
            return redirect(url_for('dashboard'))
        flash('Wrong creds', 'error')
        return redirect(url_for('signin'))
    return render_template('login.html')

@app.route('/logout')
def signout():
    session.pop('loggedin', None)
    flash('Bye!', 'info')
    return redirect(url_for('dashboard'))

@app.route('/execute', methods=['GET', 'POST'])
def execute():
    if request.method == 'POST':
        user_cmd = request.form['command']
        # Command injection
        result = subprocess.getoutput(user_cmd)
        return render_template('exec_command.html', result=result)
    return render_template('exec_command.html')

if __name__ == '__main__':
    # Debug mode on
    app.run(debug=True)