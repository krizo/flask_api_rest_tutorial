import sqlite3
from flask_restful import Resource, reqparse
from section6.models.user import UserModel


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

        if UserModel.find_by_username(username):
            return {"message": "User {} already exists".format(username)}, 400

        user =  UserModel(**data) #UserModel(username, password)
        user.save_to_db()

        return {"message": "User {} created successfully".format(username)}, 201
