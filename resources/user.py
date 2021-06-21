from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_restful import Resource
from flask import request
from datetime import timedelta

from models.user import UserModel
from schemas.user import UserSchema
from resources.security import admin_required


USER_CREATED = "User created successfully"
INVALID_CREDENTIALS = "Invalid credentials"
USER_NOT_FOUND = "User not found"
USER_DELETED = "User deleted"

user_schema = UserSchema()


class UserRegister(Resource):
    @staticmethod
    def post():
        user = user_schema.load(request.get_json())

        if UserModel.find_by_username(user.username):
            return {'message': 'The username is already used'}, 400

        user.encrypt_password()
        user.save_to_db()

        return {'message': USER_CREATED}, 201


class UserLogin(Resource):
    @staticmethod
    def post():
        user_data = user_schema.load(request.get_json())

        user = UserModel.find_by_username(user_data.username)
        if user and user.check_password(user_data.password):
            additional_claims = {
                'username': user.username,
                'admin': user.admin
            }
            access_token = create_access_token(
                identity=user.id,
                fresh=True,
                additional_claims=additional_claims,
                expires_delta=timedelta(hours=2))
            refresh_token = create_refresh_token(user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        return {'message': INVALID_CREDENTIALS}, 401


class User(Resource):
    @staticmethod
    @jwt_required()
    @admin_required
    def get(user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        return user_schema.dump(user)

    @staticmethod
    @jwt_required(fresh=True)
    @admin_required
    def delete(user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        user.delete_from_db()
        return {'message': USER_DELETED}


class Users(Resource):
    @staticmethod
    @jwt_required()
    @admin_required
    def get():
        return {'users': [user_schema.dump(user) for user in UserModel.get_all()]}


class TokenRefresh(Resource):
    @staticmethod
    @jwt_required(refresh=True)
    def post():
        current_user = UserModel.find_by_id(get_jwt_identity())
        if current_user:
            additional_claims = {
                'username': current_user.username,
                'admin': current_user.admin
            }
            access_token = create_access_token(identity=current_user.id,
                                               fresh=False,
                                               additional_claims=additional_claims,
                                               expires_delta=timedelta(hours=2))
            return {'access_token': access_token}, 200
