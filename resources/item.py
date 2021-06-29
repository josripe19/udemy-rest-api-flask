from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.item import ItemModel
from schemas.item import ItemSchema, itemInputSchema
from api import api
from libs.strings import gettext


item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):
    @staticmethod
    def get(name: str):
        item = ItemModel.find_item(name)

        if item:
            return item_schema.dump(item)
        return {'message': gettext("item_not_found")}, 404

    @staticmethod
    @api.expect(itemInputSchema)
    @api.doc(security='Bearer')
    @jwt_required()
    def post(name: str):
        if ItemModel.find_item(name):
            return {'message': gettext("item_name_exists").format(name)}, 400

        item_json = request.get_json()
        item_json['name'] = name
        item = item_schema.load(item_json)

        try:
            item.upsert()
        except:
            return {"message": gettext("item_error_inserting")}, 500

        return item_schema.dump(item), 201

    @staticmethod
    @api.doc(security='Bearer')
    @jwt_required()
    def delete(name: str):
        item = ItemModel.find_item(name)
        if item:
            item.delete()

        return {'message': gettext("item_deleted")}

    @staticmethod
    @api.expect(itemInputSchema)
    @api.doc(security='Bearer')
    @jwt_required()
    def put(name: str):
        item_json = request.get_json()
        item = ItemModel.find_item(name)

        if item:
            item.price = item_json['price']
        else:
            item_json['name'] = name
            item = item_schema.load(item_json)

        item.upsert()
        return item_schema.dump(item)


class Items(Resource):
    @staticmethod
    @api.doc(security='Bearer')
    @jwt_required(optional=True)
    def get():
        items = ItemModel.get_all()
        if get_jwt_identity():
            return {'items': item_list_schema.dump(items)}
        return {
            'items': [item.name for item in items],
            'message': 'More data available if you log in.'
        }
