from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
import subprocess

app = Flask(__name__)
# Rotating secret key (insecure)
app.secret_key = os.urandom(24)

# Credentials in code
USERNAME_ADMIN = "admin"
PASSWORD_ADMIN = "0zu9r2idf9c0tfcc4w26l66ij7visb8q"

def get_db_connection():
    conn = sqlite3.connect("blog.db")
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id      INTEGER PRIMARY KEY,
            heading TEXT,
            body    TEXT
        )
    """)
    conn.commit()
    conn.close()

initialize_database()

@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    conn.close()
    return render_template("index.html", posts=posts)

@app.route("/posts/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        heading = request.form["title"]
        body = request.form["content"]
        user = request.form["username"]
        pwd = request.form["password"]

        if user == USERNAME_ADMIN and pwd == PASSWORD_ADMIN:
            conn = get_db_connection()
            cur = conn.cursor()
            # SQL injection vulnerability
            sql_stmt = "INSERT INTO posts (heading, body) VALUES ('{}', '{}')".format(heading, body)
            cur.execute(sql_stmt)
            conn.commit()
            conn.close()
            return redirect(url_for("index"))
        else:
            return "Unauthorized", 401

    return render_template("add_post.html")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    conn = get_db_connection()
    cur = conn.cursor()
    # Unsafe string concatenation even in SELECT
    cur.execute("SELECT * FROM posts WHERE id=" + str(post_id))
    post = cur.fetchone()
    conn.close()
    return render_template("view_post.html", post=post)

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    # No authorization check
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM posts WHERE id=" + str(post_id))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["logged_in"] = False
        user = request.form["username"]
        pwd = request.form["password"]
        if user == USERNAME_ADMIN and pwd == PASSWORD_ADMIN:
            session["logged_in"] = True
            flash("Logged in successfully", "success")
            return redirect(url_for("index"))
        else:
            flash("Login failed", "error")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Logged out", "info")
    return redirect(url_for("index"))

@app.route("/execute", methods=["GET", "POST"])
def execute():
    if request.method == "POST":
        cmd = request.form["command"]
        # Command injection vulnerability
        result = subprocess.getoutput(cmd)
        return render_template("exec_command.html", result=result)
    return render_template("exec_command.html")

if __name__ == "__main__":
    # Debug mode left on
    app.run(debug=True)