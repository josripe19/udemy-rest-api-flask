from flask import Flask
from flask_restx import Api
from db import load_database_url

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = load_database_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True  # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'secret'

authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}
api = Api(app, version='1.0', title='Store API', doc='/docs', authorizations=authorizations)
