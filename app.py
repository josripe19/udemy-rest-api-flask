import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, Users, UserLogin, TokenRefresh
from resources.item import Items, Item
from resources.store import Stores, Store
from db import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db').replace('postgres', 'postgresql')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True  # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'secret'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


# app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
# app.config['JWT_VERIFY_EXPIRATION'] = False
# jwt = JWT(app, authenticate, identity)  # this generates a POST /auth endpoint
jwt = JWTManager(app)


# --------------  some possible callbacks  ------------------
# @jwt.invalid_token_loader
# @jwt.expired_token_loader
# @jwt.unauthorized_loader
# @jwt.revoked_token_loader
# @jwt.token_in_blocklist_loader
# @jwt.needs_fresh_token_loader


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Stores, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(Users, '/users')
api.add_resource(User, '/user/<int:user_id>')


@app.route('/')
def home():
    return "Hello World"


if __name__ == '__main__':
    db.init_app(app)
    app.run()
