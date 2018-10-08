import sqlite3
import os

DATABASE_FILE = 'data.db'

try:
    os.remove(DATABASE_FILE)
except FileNotFoundError:
    pass

connection = sqlite3.connect(DATABASE_FILE)

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

users = [
    (1, 'kriz', 'asdf'),
    (2, 'emi', 'easy')
]

insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.executemany(insert_query, users)

query = "SELECT * FROM users"

[print(row) for row in cursor.execute(query)]

connection.commit()
connection.close()
