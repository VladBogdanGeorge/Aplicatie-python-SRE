import sys
import psycopg2
import os
from flask import Flask, request, jsonify

DB_NAME = os.environ.get('DB_NAME', 'bogdan')
DB_USER = os.environ.get('DB_USER', 'bogdan')
DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_PASS = os.environ.get('DB_PASSWORD', 'bogdanpass')

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
    )

def create_table_if_not_exists():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            nume VARCHAR(100),
            prenume VARCHAR(100)
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

def add_user(nume, prenume):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (nume, prenume) VALUES (%s, %s);', (nume, prenume))
    conn.commit()
    cur.close()
    conn.close()
    print("User adaugat.")

def delete_user(nume, prenume):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE nume=%s AND prenume=%s;', (nume, prenume))
    conn.commit()
    cur.close()
    conn.close()
    print("User sters.")

def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, nume, prenume FROM users;')
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

# Flask API
app_flask = Flask(__name__)

@app_flask.route('/users', methods=['GET'])
def api_get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, nume, prenume FROM users;')
    users = [{'id': row[0], 'nume': row[1], 'prenume': row[2]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(users)

@app_flask.route('/users', methods=['POST'])
def api_add_user():
    data = request.get_json()
    nume = data.get('nume')
    prenume = data.get('prenume')
    if not nume or not prenume:
        return jsonify({'error': 'Missing nume or prenume'}), 400
    add_user(nume, prenume)
    return jsonify({'message': 'User adaugat'}), 201

@app_flask.route('/users', methods=['DELETE'])
def api_delete_user():
    data = request.get_json()
    nume = data.get('nume')
    prenume = data.get('prenume')
    if not nume or not prenume:
        return jsonify({'error': 'Missing nume or prenume'}), 400
    delete_user(nume, prenume)
    return jsonify({'message': 'User sters'}), 200

@app_flask.route('/')
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, nume, prenume FROM users;')
    users = cur.fetchall()
    cur.close()
    conn.close()
    html = "<h1>Lista useri</h1><ul>"
    for user in users:
        html += f"<li>{user[1]} {user[2]}</li>"
    html += "</ul>"
    return html

if __name__ == "__main__":
    create_table_if_not_exists()
    if len(sys.argv) > 1:
        # CLI mode
        if len(sys.argv) == 4 and sys.argv[3].upper() == "ADD":
            add_user(sys.argv[1], sys.argv[2])
        elif len(sys.argv) == 4 and sys.argv[3].upper() == "DELETE":
            delete_user(sys.argv[1], sys.argv[2])
        elif len(sys.argv) == 2 and sys.argv[1].upper() == "GET":
            get_users()
        else:
            print("Usage: python app.py <nume> <prenume> ADD|DELETE\n       python app.py GET")
    else:
        # Web API mode
        app_flask.run(host="0.0.0.0", port=8000)
