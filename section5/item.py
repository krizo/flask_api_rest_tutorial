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

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

        return item, 201

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {"message": "An item with name {} already exists".format(name)}, 400

        payload = Item.parser.parse_args()
        item = {"name": name, "price": payload["price"]}
        try:
            self.insert(item)
        except:
            return {"message": "An error occured while inserting {} item".format(item)}, 500

        return item, 201

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items where name=?"

        cursor.execute(query, (name, ))

        connection.commit()
        connection.close()

        return {"message": "Item {} deleted".format(name)}


    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = { 'name': name, 'price': data['price']}

        if updated_item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occured on inserting the item {}".format(item)}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occured on inserting the item {}".format(item)}, 500
        return updated_item

class ItemList(Resource):

    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"

        rows = cursor.execute(query)
        items = [ { "name": row[0], "price": row[1] } for row in rows ]

        connection.commit()
        connection.close()

        return {"items": items}, 200
