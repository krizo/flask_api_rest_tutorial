from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
import sqlite3
from section6.models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str, help="name can't be blank!")
    parser.add_argument('price', required=False, type=float)

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name {} already exists".format(name)}, 400

        payload = Item.parser.parse_args()
        item = ItemModel(name, payload['price'])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while inserting {} item".format(item)}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item {} deleted".format(name)}


    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
             item = ItemModel(name, data['price'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()

class ItemList(Resource):

    @jwt_required()
    def get(self):

        return {"items": [ x.json() for x in ItemModel.query.all() ]}, 200
