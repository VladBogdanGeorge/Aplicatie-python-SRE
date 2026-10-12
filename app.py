from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_connection():
    return sqlite3.connect("people.db")

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS people (id INTEGER PRIMARY KEY, nume TEXT, prenume TEXT)''')
    conn.commit()
    conn.close()

@app.route('/add', methods=['POST'])
def add():
    nume = request.args.get('nume')
    prenume = request.args.get('prenume')
    if not nume or not prenume:
        return jsonify({"status": "error", "message": "nume si prenume sunt necesare"}), 400
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO people (nume, prenume) VALUES (?, ?)", (nume, prenume))
    conn.commit()
    conn.close()
    return jsonify({"status": "added"})

@app.route('/delete', methods=['POST'])
def delete():
    nume = request.args.get('nume')
    prenume = request.args.get('prenume')
    if not nume or not prenume:
        return jsonify({"status": "error", "message": "nume si prenume sunt necesare"}), 400
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM people WHERE nume=? AND prenume=?", (nume, prenume))
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"})

@app.route('/get', methods=['GET'])
def get():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT nume, prenume FROM people")
    results = c.fetchall()
    conn.close()
    return jsonify({"people": results})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000)