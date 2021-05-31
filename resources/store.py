from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_item(name)

        if store:
            return store.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_item(name):
            return {'message': f"A store with name {name} already exists."}, 400

        new_store = StoreModel(name)
        new_store.upsert()

        return new_store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_item(name)
        if store:
            store.delete()

        return {'message': 'Store deleted'}


class Stores(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
