from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
import subprocess

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Hardcoded credentials (for demonstration purposes only)
ROOT_USER = 'admin'
ROOT_PASSWD = '0zu9r2idf9c0tfcc4w26l66ij7visb8q'

# Initialize the database
db_init = sqlite3.connect('blog.db')
cursor_init = db_init.cursor()
cursor_init.execute('''CREATE TABLE IF NOT EXISTS posts 
                       (id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')
db_init.commit()
db_init.close()

@app.route('/')
def index():
    conn_main = sqlite3.connect('blog.db')
    main_cur = conn_main.cursor()
    main_cur.execute('SELECT * FROM posts')
    records = main_cur.fetchall()
    conn_main.close()
    return render_template('index.html', posts=records)

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']

        # Hardcoded credentials check (vulnerability)
        in_user = request.form['username']
        in_pass = request.form['password']
        if in_user == ROOT_USER and in_pass == ROOT_PASSWD:
            conn_add = sqlite3.connect('blog.db')
            add_cur = conn_add.cursor()
            # SQL Injection vulnerability
            add_cur.execute("INSERT INTO posts (title, content) VALUES ('" + new_title + "', '" + new_content + "')")
            conn_add.commit()
            conn_add.close()
            return redirect(url_for('index'))
        else:
            return "Unauthorized: Incorrect username or password."

    return render_template('add_post.html')

@app.route('/view_post/<int:entry_id>')
def view_post(entry_id):
    conn_v = sqlite3.connect('blog.db')
    v_cur = conn_v.cursor()
    v_cur.execute('SELECT * FROM posts WHERE id = ?', (entry_id,))
    entry = v_cur.fetchone()
    conn_v.close()
    return render_template('view_post.html', post=entry)

@app.route('/delete_post/<int:del_id>', methods=['POST'])
def delete_post(del_id):
    # Missing authorization check
    conn_del = sqlite3.connect('blog.db')
    del_cur = conn_del.cursor()
    del_cur.execute('DELETE FROM posts WHERE id = ?', (del_id,))
    conn_del.commit()
    conn_del.close()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['is_logged'] = False
        chk_user = request.form['username']
        chk_pass = request.form['password']
        if chk_user == ROOT_USER and chk_pass == ROOT_PASSWD:
            session['is_logged'] = True
            flash('Login successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('is_logged', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/exec_command', methods=['GET', 'POST'])
def exec_command():
    if request.method == 'POST':
        cmd_input = request.form['command']
        # Command Injection vulnerability
        cmd_output = subprocess.getoutput(cmd_input)
        return render_template('exec_command.html', result=cmd_output)
    return render_template('exec_command.html')

if __name__ == '__main__':
    # Debug Mode Enabled vulnerability
    app.run(debug=True)