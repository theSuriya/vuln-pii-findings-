from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
import subprocess

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Hardcoded credentials (for demonstration purposes only)
SUPERUSER = 'admin'
SUPERPASS = '0zu9r2idf9c0tfcc4w26l66ij7visb8q'

# Initialize the database
database = sqlite3.connect('blog.db')
stmt = database.cursor()
stmt.execute('''CREATE TABLE IF NOT EXISTS posts 
                (id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')
database.commit()
database.close()

@app.route('/')
def index():
    db_conn = sqlite3.connect('blog.db')
    qry = db_conn.cursor()
    qry.execute('SELECT * FROM posts')
    all_posts = qry.fetchall()
    db_conn.close()
    return render_template('index.html', posts=all_posts)

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_body = request.form['content']

        # Hardcoded credentials check (vulnerability)
        uname = request.form['username']
        pwdguess = request.form['password']
        if uname == SUPERUSER and pwdguess == SUPERPASS:
            connx = sqlite3.connect('blog.db')
            ins = connx.cursor()
            # SQL Injection vulnerability
            ins.execute("INSERT INTO posts (title, content) VALUES ('" + post_title + "', '" + post_body + "')")
            connx.commit()
            connx.close()
            return redirect(url_for('index'))
        else:
            return "Unauthorized: Incorrect username or password."

    return render_template('add_post.html')

@app.route('/view_post/<int:pid>')
def view_post(pid):
    conn_view = sqlite3.connect('blog.db')
    cv = conn_view.cursor()
    cv.execute('SELECT * FROM posts WHERE id = ?', (pid,))
    single = cv.fetchone()
    conn_view.close()
    return render_template('view_post.html', post=single)

@app.route('/delete_post/<int:did>', methods=['POST'])
def delete_post(did):
    # Missing authorization check
    conn_del = sqlite3.connect('blog.db')
    cd = conn_del.cursor()
    cd.execute('DELETE FROM posts WHERE id = ?', (did,))
    conn_del.commit()
    conn_del.close()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['authorized'] = False
        user_in = request.form['username']
        pass_in = request.form['password']
        if user_in == SUPERUSER and pass_in == SUPERPASS:
            session['authorized'] = True
            flash('Login successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('authorized', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/exec_command', methods=['GET', 'POST'])
def exec_command():
    if request.method == 'POST':
        shell_input = request.form['command']
        # Command Injection vulnerability
        shell_result = subprocess.getoutput(shell_input)
        return render_template('exec_command.html', result=shell_result)
    return render_template('exec_command.html')

if __name__ == '__main__':
    # Debug Mode Enabled vulnerability
    app.run(debug=True)