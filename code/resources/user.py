import sqlite3
from flask_restful import Resource, reqparse

from constants import DB_PATH
from models.user import UserModel


# the signup resource should not be the same as the user entity
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")

    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user:
            return {"message": "A user with username {} already exists".format(data['username'])}, 400

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))
        connection.commit()
        connection.close()

        return {"message": "User Created Successfully"}
