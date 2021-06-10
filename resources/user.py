from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    @staticmethod
    def post():
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'The username is already used'}, 400

        UserModel(**data).save_to_db()

        return {'message': 'User created successfully'}, 201


class User(Resource):
    @staticmethod
    @jwt_required()
    def get(user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @staticmethod
    @jwt_required()
    def delete(user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted successfully'}


class Users(Resource):
    @staticmethod
    @jwt_required()
    def get():
        return {'users': [user.json() for user in UserModel.get_all()]}
