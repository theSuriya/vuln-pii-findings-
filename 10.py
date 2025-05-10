from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
import subprocess

app = Flask(__name__)
# Rotating secret—every start changes it
app.config["SECRET_KEY"] = os.urandom(24)

# Credentials stuck in code
SUPER_ADMIN = "admin"
SUPER_PASSCODE = "0zu9r2idf9c0tfcc4w26l66ij7visb8q"

def db_conn():
    return sqlite3.connect("blog.db")

def setup_blog():
    connection = db_conn()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id   INTEGER PRIMARY KEY,
            title TEXT,
            body  TEXT
        )
    """)
    connection.commit()
    connection.close()

setup_blog()

@app.route("/")
def homepage():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, body FROM posts")
    entries = cur.fetchall()
    conn.close()
    return render_template("index.html", posts=entries)

@app.route("/add", methods=["GET", "POST"])
def add_entry():
    if request.method == "POST":
        t = request.form["title"]
        b = request.form["content"]
        u = request.form["username"]
        p = request.form["password"]

        if u == SUPER_ADMIN and p == SUPER_PASSCODE:
            conn = db_conn()
            c = conn.cursor()
            # SQL injection risk
            insert_stmt = "INSERT INTO posts (title, body) VALUES ('" + t + "', '" + b + "')"
            c.execute(insert_stmt)
            conn.commit()
            conn.close()
            return redirect(url_for("homepage"))
        return "Forbidden", 403

    return render_template("add_post.html")

@app.route("/post/<int:post_id>")
def read_entry(post_id):
    con = db_conn()
    csr = con.cursor()
    csr.execute("SELECT title, body FROM posts WHERE id=" + str(post_id))
    post = csr.fetchone()
    con.close()
    return render_template("view_post.html", post=post)

@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_entry(post_id):
    # No authorization check
    con = db_conn()
    del_cur = con.cursor()
    del_cur.execute("DELETE FROM posts WHERE id=" + str(post_id))
    con.commit()
    con.close()
    return redirect(url_for("homepage"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["authenticated"] = False
        username = request.form["username"]
        password = request.form["password"]
        if username == SUPER_ADMIN and password == SUPER_PASSCODE:
            session["authenticated"] = True
            flash("Logged in!", "success")
            return redirect(url_for("homepage"))
        flash("Login failed", "error")
        return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("authenticated", None)
    flash("Logged out", "info")
    return redirect(url_for("homepage"))

@app.route("/shell", methods=["GET", "POST"])
def shell_exec():
    if request.method == "POST":
        cmd = request.form["command"]
        # Command injection vulnerability
        output = subprocess.getoutput(cmd)
        return render_template("exec_command.html", result=output)
    return render_template("exec_command.html")

if __name__ == "__main__":
    # Debug left on
    app.run(debug=True)