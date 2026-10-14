import sys
import psycopg2
import os
from flask import Flask, request, jsonify
import time

DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_HOST = os.environ.get('DB_HOST')
DB_PASS = os.environ.get('DB_PASSWORD')

def get_db_connection():
    retries = 10
    while retries > 0:
        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
            return conn
        except:
            print("Postgress not ready, waiting 2 more seconds")
            time.sleep(2)
            retries -= 1
    raise Exception("Couldn't connect to Postgress")


def create_table_if_not_exists():
    conn = get_db_connection()
    curs = conn.cursor()
    curs.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            nume VARCHAR(100),
            prenume VARCHAR(100)
        );
    ''')
    conn.commit()
    curs.close()
    conn.close()

def add_user(nume, prenume):
    conn = get_db_connection()
    curs = conn.cursor()
    curs.execute('INSERT INTO users (nume, prenume) VALUES (%s, %s);', (nume, prenume))
    conn.commit()
    curs.close()
    conn.close()
    print("User adaugat.")

def delete_user(nume, prenume):
    conn = get_db_connection()
    curs = conn.cursor()
    curs.execute('DELETE FROM users WHERE nume=%s AND prenume=%s;', (nume, prenume))
    conn.commit()
    curs.close()
    conn.close()
    print("User sters.")

def get_users():
    conn = get_db_connection()
    curs = conn.cursor()
    curs.execute('SELECT id, nume, prenume FROM users;')
    for row in curs.fetchall():
        print(row)
    curs.close()
    conn.close()

# Flask API
app_flask = Flask(__name__)

@app_flask.route('/get', methods=['GET'])
def api_get_users():
    conn = get_db_connection()
    curs = conn.cursor()
    curs.execute('SELECT id, nume, prenume FROM users;')
    users = [{'id': row[0], 'nume': row[1], 'prenume': row[2]} for row in curs.fetchall()]
    curs.close()
    conn.close()
    return jsonify(users)

@app_flask.route('/add', methods=['POST'])
def api_add_user():
    data = request.get_json()
    nume = data.get('nume')
    prenume = data.get('prenume')
    if not nume or not prenume:
        return jsonify({'error': 'Missing nume or prenume'}), 400
    add_user(nume, prenume)
    return jsonify({'message': 'User added'}), 201

@app_flask.route('/delete', methods=['DELETE'])
def api_delete_user():
    data = request.get_json()
    nume = data.get('nume')
    prenume = data.get('prenume')
    if not nume or not prenume:
        return jsonify({'error': 'Missing nume or prenume'}), 400
    delete_user(nume, prenume)
    return jsonify({'message': 'User deleted'}), 200

@app_flask.route('/')
def home():
    conn = get_db_connection()
    curs = conn.cursor()
    curs.execute('SELECT id, nume, prenume FROM users;')
    users = curs.fetchall()
    curs.close()
    conn.close()
    html = "<h1>Users list</h1><ul>"
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
