import sqlite3
from sqlite3 import Error
import os


class sqlconnect:
    def __init__(self):
        print("init")

    # initiates connection to DB
    def create_connection(self):
        DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'chicagocrime.db')
        conn = None
        try:
            conn = sqlite3.connect(DEFAULT_PATH)
            print("Connected to DB successfully")
        except Error as e:
            print(e)
        return conn

    def queryIUCR(self, conn):
        with conn:
            sql = ("SELECT * crimes WHERE iucr LIKE ?", ('0486',))
            cur = conn.cursor()
            cur.execute(sql)
        return cur.lastrowid

def main():
    connecto = sqlconnect()
    conn = connecto.create_connection()
    with conn:
        team_id = connecto.queryIUCR(connecto)
        print(str(team_id))

if __name__ == '__main__':
    main()