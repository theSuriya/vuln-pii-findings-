from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
import subprocess

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Hardcoded credentials (for demonstration purposes only)
ADMIN_USER = 'admin'
ADMIN_PASS = '0zu9r2idf9c0tfcc4w26l66ij7visb8q'

# Initialize the database
conn = sqlite3.connect('blog.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS posts 
               (id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')
conn.commit()
conn.close()

@app.route('/')
def index():
    db = sqlite3.connect('blog.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    db.close()
    return render_template('index.html', posts=posts)

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        heading = request.form['title']
        body = request.form['content']

        # Hardcoded credentials check (vulnerability)
        user_field = request.form['username']
        pass_field = request.form['password']
        if user_field == ADMIN_USER and pass_field == ADMIN_PASS:
            db = sqlite3.connect('blog.db')
            cur2 = db.cursor()
            # SQL Injection vulnerability
            cur2.execute("INSERT INTO posts (title, content) VALUES ('" + heading + "', '" + body + "')")
            db.commit()
            db.close()
            return redirect(url_for('index'))
        else:
            return "Unauthorized: Incorrect username or password."

    return render_template('add_post.html')

@app.route('/view_post/<int:post_id>')
def view_post(post_id):
    connection = sqlite3.connect('blog.db')
    cview = connection.cursor()
    cview.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    post = cview.fetchone()
    connection.close()
    return render_template('view_post.html', post=post)

@app.route('/delete_post/<int:delete_id>', methods=['POST'])
def delete_post(delete_id):
    # Missing authorization check
    conn2 = sqlite3.connect('blog.db')
    cdel = conn2.cursor()
    cdel.execute('DELETE FROM posts WHERE id = ?', (delete_id,))
    conn2.commit()
    conn2.close()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['logged'] = False
        usr = request.form['username']
        pwd = request.form['password']
        if usr == ADMIN_USER and pwd == ADMIN_PASS:
            session['logged'] = True
            flash('Login successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/exec_command', methods=['GET', 'POST'])
def exec_command():
    if request.method == 'POST':
        to_run = request.form['command']
        # Command Injection vulnerability
        output = subprocess.getoutput(to_run)
        return render_template('exec_command.html', result=output)
    return render_template('exec_command.html')

if __name__ == '__main__':
    # Debug Mode Enabled vulnerability
    app.run(debug=True)