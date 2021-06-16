from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.store import StoreModel

ALREADY_EXISTS = "A store with name {} already exists."
STORE_NOT_FOUND = "Store not found"
STORE_DELETED = "Store deleted"


class Store(Resource):
    def get(self, name: str):
        store = StoreModel.find_item(name)

        if store:
            return store.json()
        return {'message': STORE_NOT_FOUND}, 404

    @jwt_required()
    def post(self, name: str):
        if StoreModel.find_item(name):
            return {'message': ALREADY_EXISTS.format(name)}, 400

        new_store = StoreModel(name)
        new_store.upsert()

        return new_store.json(), 201

    @jwt_required()
    def delete(self, name: str):
        store = StoreModel.find_item(name)
        if store:
            store.delete()

        return {'message': STORE_DELETED}


class Stores(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
