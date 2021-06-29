from flask_restx import Resource
from flask_jwt_extended import jwt_required

from models.store import StoreModel
from schemas.store import StoreSchema
from libs.strings import gettext


store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class Store(Resource):
    @staticmethod
    def get(name: str):
        store = StoreModel.find_item(name)

        if store:
            return store_schema.dump(store)
        return {'message': gettext("store_not_found")}, 404

    @staticmethod
    @jwt_required()
    def post(name: str):
        if StoreModel.find_item(name):
            return {'message': gettext("store_name_exists").format(name)}, 400

        new_store = StoreModel(name=name)
        new_store.upsert()

        return store_schema.dump(new_store), 201

    @staticmethod
    @jwt_required()
    def delete(name: str):
        store = StoreModel.find_item(name)
        if store:
            store.delete()

        return {'message': gettext("store_deleted")}


class Stores(Resource):
    @staticmethod
    def get():
        return {'stores': store_list_schema.dump(StoreModel.query.all())}
