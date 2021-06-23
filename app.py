from flask import jsonify
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from resources.user import UserRegister, User, Users, UserLogin, TokenRefresh
from resources.item import Items, Item
from resources.store import Stores, Store
from db import db
from ma import ma
from api import app, api


@app.route('/')
def home():
    return "Hello World"


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)  # needs app.config['PROPAGATE_EXCEPTIONS'] = True
def handle_marshmallow_validation(err):  # except ValidationError as err
    return jsonify(err.messages), 400


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

api.add_resource(Item, '/items/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(Store, '/stores/<string:name>')
api.add_resource(Stores, '/stores')
api.add_resource(UserRegister, '/auth/register')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(TokenRefresh, '/auth/refresh')
api.add_resource(Users, '/users')
api.add_resource(User, '/users/<int:user_id>')


if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(host='0.0.0.0')
