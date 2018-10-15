import sqlite3
from flask_restful import Resource, reqparse


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
