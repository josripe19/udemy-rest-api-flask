from flask_restful import Resource
from flask_jwt_extended import jwt_required

from models.store import StoreModel
from schemas.store import StoreSchema

ALREADY_EXISTS = "A store with name {} already exists."
STORE_NOT_FOUND = "Store not found"
STORE_DELETED = "Store deleted"

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class Store(Resource):
    @staticmethod
    def get(name: str):
        store = StoreModel.find_item(name)

        if store:
            return store_schema.dump(store)
        return {'message': STORE_NOT_FOUND}, 404

    @staticmethod
    @jwt_required()
    def post(name: str):
        if StoreModel.find_item(name):
            return {'message': ALREADY_EXISTS.format(name)}, 400

        new_store = StoreModel(name=name)
        new_store.upsert()

        return store_schema.dump(new_store), 201

    @staticmethod
    @jwt_required()
    def delete(name: str):
        store = StoreModel.find_item(name)
        if store:
            store.delete()

        return {'message': STORE_DELETED}


class Stores(Resource):
    @staticmethod
    def get():
        return {'stores': store_list_schema.dump(StoreModel.query.all())}
