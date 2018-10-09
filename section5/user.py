import sqlite3
from flask_restful import Resource, reqparse


class User(Resource):
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


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="Username can't be blank"
    )

    parser.add_argument('password',
        type=str,
        required=True,
        help="Password can't be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        username, password = data['username'], data['password']

        if User.find_by_username(username):
            return {"message": "User {} already exists".format(username)}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (username, password))

        connection.commit()
        connection.close()
        return {"message": "User {} created successfully".format(username)}, 201
