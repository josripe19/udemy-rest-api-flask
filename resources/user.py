from hmac import compare_digest
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token
from flask_restful import Resource, reqparse

from models.user import UserModel
from resources.security import admin_required


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True)
_user_parser.add_argument('password', type=str, required=True)


class UserRegister(Resource):
    @staticmethod
    def post():
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'The username is already used'}, 400

        UserModel(**data).save_to_db()

        return {'message': 'User created successfully'}, 201


class UserLogin(Resource):
    @staticmethod
    def post():
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and compare_digest(user.password, data['password']):
            additional_claims = {
                'username': user.username,
                'admin': user.admin
            }
            access_token = create_access_token(identity=user.id, fresh=True, additional_claims=additional_claims)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid credentials'}, 401


class User(Resource):
    @staticmethod
    @jwt_required()
    @admin_required
    def get(user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @staticmethod
    @jwt_required()
    @admin_required
    def delete(user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted successfully'}


class Users(Resource):
    @staticmethod
    @jwt_required()
    @admin_required
    def get():
        return {'users': [user.json() for user in UserModel.get_all()]}
