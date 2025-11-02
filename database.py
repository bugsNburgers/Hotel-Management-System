# database.py
from mysql.connector import connect, Error
from db_config import DB

def get_conn():
    try:
        return connect(
            host=DB.get("host", "localhost"),
            user=DB.get("user", "root"),
            password=DB.get("password", ""),
            database=DB.get("database", "hotel_booking"),
            port=int(DB.get("port", 3306))
        )
    except Error as e:
        print("Database connection failed:", e)
        raise

def fetch_all(query, params=()):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

def fetch_one(query, params=()):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute(query, params)
    row = cur.fetchone()
    cur.close(); conn.close()
    return row

def execute(query, params=()):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    last_id = cur.lastrowid
    cur.close(); conn.close()
    return last_id

def call_proc(proc_name, params=()):
    conn = get_conn()
    cur = conn.cursor()
    cur.callproc(proc_name, params)
    results = []
    try:
        for res in cur.stored_results():
            results.append(res.fetchall())
    except Exception:
        pass
    conn.commit()
    cur.close(); conn.close()
    return results
