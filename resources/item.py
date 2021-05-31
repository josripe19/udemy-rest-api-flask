import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT name, price FROM items"
        result = cursor.execute(query)
        items_result = result.fetchall()
        connection.close()

        return {'items': [{'name': item[0], 'price': item[1]} for item in items_result]}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
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

        new_item = ItemModel(name, data['price'])
        new_item.insert()

        return new_item.json(), 201

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_item(name)
        new_or_updated = ItemModel(name, data['price'])

        if item:
            new_or_updated.update()
        else:
            new_or_updated.insert()

        return new_or_updated.json()
