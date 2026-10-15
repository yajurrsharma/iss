import sqlite3


def init_db():
    con = sqlite3.connect('iss.db')
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS iss_data (email TEXT PRIMARY KEY, lat REAL, lon REAL)")
    con.commit()
    con.close()

def insert_user(email, lat, lon):
    con = sqlite3.connect('iss.db')
    cur = con.cursor()

    cur.execute("INSERT OR REPLACE INTO iss_data (email, lat, lon) values (?, ?, ?)", (email, lat, lon))
    con.commit()
    con.close()

def get_all():
    con = sqlite3.connect('iss.db')
    cur = con.cursor()

    cur.execute('SELECT * FROM iss_data')
    users = cur.fetchall()
    con.close()
    return users