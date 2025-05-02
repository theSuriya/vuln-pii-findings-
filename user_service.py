from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_user(user_id):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, email, dob FROM users WHERE id=?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {'name': row[0], 'email': row[1], 'dob': row[2]}

@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = get_user(user_id)
    if not user:
        return jsonify({'error': 'Not found'}), 404
    # True positives:
    # user['email'] -> "alice.wonderland@example.com"
    # user['dob']   -> "1990-07-15"
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=True)