from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.item import ItemModel
from schemas.item import ItemSchema

ALREADY_EXISTS = "An item with name '{}' already exists."
ITEM_NOT_FOUND = "Item not found"
ITEM_DELETED = "Item deleted"
ERROR_INSERTING = "An error occurred while inserting the item."

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):
    @staticmethod
    def get(name: str):
        item = ItemModel.find_item(name)

        if item:
            return item_schema.dump(item)
        return {'message': ITEM_NOT_FOUND}, 404

    @staticmethod
    @jwt_required()
    def post(name: str):
        if ItemModel.find_item(name):
            return {'message': ALREADY_EXISTS.format(name)}, 400

        try:
            item_json = request.get_json()
            item_json['name'] = name
            item = item_schema.load(item_json)
        except ValidationError as err:
            return err.messages, 400

        try:
            item.upsert()
        except:
            return {"message": ERROR_INSERTING}, 500

        return item_schema.dump(item), 201

    @staticmethod
    @jwt_required()
    def delete(name: str):
        item = ItemModel.find_item(name)
        if item:
            item.delete()

        return {'message': ITEM_DELETED}

    @staticmethod
    @jwt_required()
    def put(name: str):
        item_json = request.get_json()
        item = ItemModel.find_item(name)

        if item:
            item.price = item_json['price']
        else:
            item_json['name'] = name
            try:
                item = item_schema.load(item_json)
            except ValidationError as err:
                return err.messages, 400

        item.upsert()
        return item_schema.dump(item)


class Items(Resource):
    @staticmethod
    @jwt_required(optional=True)
    def get():
        items = ItemModel.get_all()
        if get_jwt_identity():
            return {'items': item_list_schema.dump(items)}
        return {
            'items': [item.name for item in items],
            'message': 'More data available if you log in.'
        }
