from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

DB_NAME = os.environ.get('POSTGRES_DB', 'bogdandb')
DB_USER = os.environ.get('POSTGRES_USER', 'bogdan')
DB_HOST = os.environ.get('POSTGRES_HOST', 'postgres')
DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'bogdanpass')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

@app.route('/get')
def get_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT version();')
    version = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify({'postgres_version': version[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)