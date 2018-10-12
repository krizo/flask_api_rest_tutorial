from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str, help="name can't be blank!")
    parser.add_argument('price', required=False, type=float)

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        select = "SELECT * FROM items where name=?"
        result = cursor.execute(select, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": row[0], "price": row[1]}
        return {"message": "item {} not found".format(name)}


    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items where name=?"
        result = cursor.execute(query, (name,))  # query arguments always as a tuple
        row = result.fetchone()
        connection.close()

        if row:
            return { 'item': {'name': row[0], 'price': row[1]}}


    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {"message": "An item with name {} already exists".format(name)}, 400

        payload = Item.parser.parse_args()
        item = {"name": name, "price": payload["price"]}

        insert = "INSERT INTO items VALUES(?, ?)"
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(insert, (item['name'], item['price']))

        connection.commit()
        connection.close()

        return item, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {"items": items}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = find_item(name)
        if item is None:
            item = {"name": data["name"], "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {"items": items}