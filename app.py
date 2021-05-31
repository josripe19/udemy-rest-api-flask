from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.user import UserRegister
from security import authenticate, identity
from resources.item import Items, Item
from db import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True  # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'secret'
api = Api(app)

app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
app.config['JWT_VERIFY_EXPIRATION'] = False
jwt = JWT(app, authenticate, identity)  # this generates a POST /auth endpoint

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')

db.init_app(app)
app.run()
