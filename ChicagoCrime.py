import sqlite3
from sqlite3 import Error
import os
import tkinter as tk


class PythonGUI(tk.Frame):  # GUI Class
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("Chicago Crime Map")
        tk.Label(self, text="Click 'Start' to Begin").pack()
        tk.Button(self, text='Start', default='active', command=self.click_start).pack(side='left')
        tk.Button(self, text='Cancel', command=self.click_cancel).pack(side='right')

        # Listbox for user to select the items they are interested in
        listbox = tk.Listbox(master, selectmode=tk.MULTIPLE)
        listbox.pack(side='left')
        for item in ["ID", "Case #", "Date", "Block", "IUCR", "Primary Type", "Description", "Beat", "District", "Latitude", "Longitude"]:
            listbox.insert(tk.END, item)


    def click_start(self):
        print("The user clicked 'Start'")

    def click_cancel(self):
        print("The user clicked 'Cancel'")
        self.master.destroy()


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
    #connobject = sqlconnect()
    #conn = connobject.create_connection()
    #with conn:
    #    crime_id = connobject.queryIUCR(conn, '0486')
    #    print(str(crime_id))

    root = tk.Tk()
    app = PythonGUI(root)
    app.mainloop()

if __name__ == '__main__':
    main()