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


    # Query Method for finding all items with a given IUCR record number
    def queryIUCR(self, conn, iucr_num):
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM crimes WHERE iucr LIKE {it}".format(it=iucr_num))
            ids = cursor.fetchall()
        return ids


def main():
    connecto = sqlconnect()
    conn = connecto.create_connection()
    with conn:
        crime_id = connecto.queryIUCR(conn, '0486')
        print(str(crime_id))

if __name__ == '__main__':
    main()