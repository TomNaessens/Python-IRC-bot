import settings
import sqlite3

DB = settings.sql_DB

def set(query, args):
    rowid = -1

    try:
        conn = sqlite3.connect(DB)

        cursor = conn.cursor()
        cursor.execute(query, args)

        rowid = cursor.lastrowid

        conn.commit()

        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print "An error occurred:", e.args[0]

    return rowid

def get(query, args):
    rows = (-1, 'Error')

    try:
        count = 0

        conn = sqlite3.connect(DB)

        cursor = conn.cursor()

        if len(args) == 0:
            cursor.execute(query)
        else:
            cursor.execute(query, args)

        rows = cursor.fetchall()
        count = cursor.rowcount

        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print "An error occurred:", e.args[0]

    return rows, count
