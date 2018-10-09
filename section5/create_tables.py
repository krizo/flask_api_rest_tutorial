import sqlite3
import os

DATABASE_FILE = 'data.db'

try:
    os.remove(DATABASE_FILE)
except FileNotFoundError:
    pass


connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

connection.commit()
connection.close()