import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS persoane (nume TEXT, prenume TEXT)')
    conn.commit()
    conn.close()

def add_persoana(nume, prenume):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO persoane VALUES (?, ?)', (nume, prenume))
    conn.commit()
    conn.close()

def delete_persoana(nume, prenume):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM persoane WHERE nume=? AND prenume=?', (nume, prenume))
    conn.commit()
    conn.close()

def get_persoane():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM persoane')
    persoane = c.fetchall()
    conn.close()
    return persoane