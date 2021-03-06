from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True
                        )

    def get(self, name):
        item = ItemModel.find_item(name)

        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_item(name):
            return {'message': f"An item with name {name} already exists."}, 400

        data = Item.parser.parse_args()

        new_item = ItemModel(name, **data)
        new_item.upsert()

        return new_item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_item(name)
        if item:
            item.delete()

        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_item(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.upsert()
        return item.json()


class Items(Resource):
    @staticmethod
    @jwt_required(optional=True)
    def get():
        items = [item.json() for item in ItemModel.get_all()]
        if get_jwt_identity():
            return {'items': items}
        return {
            'items': [item['name'] for item in items],
            'message': 'More data available if you log in.'
        }
