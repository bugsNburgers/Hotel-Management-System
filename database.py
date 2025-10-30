# database.py
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MySQL@123',
    'database': 'hotel_booking'
}


class Database:
    def __init__(self, cfg=DB_CONFIG):
        self.cfg = cfg

    def connect(self):
        return mysql.connector.connect(**self.cfg)

    def fetch(self, query, params=None):
        conn = None
        cur = None
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(query, params or ())
            return cur.fetchall()
        except Error as e:
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def execute(self, query, params=None, commit=True):
        conn = None
        cur = None
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(query, params or ())
            if commit:
                conn.commit()
            return cur.lastrowid
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def callproc(self, procname, args=()):
        """
        Call stored procedure. Returns list of result sets returned by the proc.
        """
        conn = None
        cur = None
        results = []
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.callproc(procname, args)
            # collect result sets
            for res in cur.stored_results():
                results.append(res.fetchall())
            conn.commit()
            return results
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
