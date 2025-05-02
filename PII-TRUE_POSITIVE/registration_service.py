from flask import Flask, jsonify, request
import sqlite3
import re

app = Flask(__name__)

def connect_db():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    full_name = data.get('full_name')
    email = data.get('email')
    ssn = data.get('ssn')
    phone = data.get('phone')
    dob = data.get('dob')

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({'error': 'Invalid email'}), 400

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO accounts (full_name, email, ssn, phone, dob) VALUES (?, ?, ?, ?, ?)',
        (full_name, email, ssn, phone, dob)
    )
    conn.commit()
    conn.close()
    return jsonify({'status': 'user created'}), 201

@app.route('/user/<int:account_id>')
def get_user(account_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT full_name, email, ssn, phone, dob FROM accounts WHERE id=?',
        (account_id,)
    )
    row = cursor.fetchone()
    conn.close()
    if not row:
        return jsonify({'error': 'Not found'}), 404

    return jsonify({
        'full_name': row['full_name'],
        'email': row['email'],
        'ssn': row['ssn'],
        'phone': row['phone'],
        'dob': row['dob']
    })

if __name__ == '__main__':
    app.run(debug=True)