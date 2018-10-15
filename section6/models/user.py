import sqlite3
from flask_restful import Resource


class UserModel(Resource):
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users where username=?"
        result = cursor.execute(query, (username,))  # query arguments always as a tuple
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users where id=?"
        result = cursor.execute(query, (_id,))  # query arguments always as a tuple
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user