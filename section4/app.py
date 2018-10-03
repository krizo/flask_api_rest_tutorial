from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


def find_item(name):
    return next(filter(lambda x: x['name'] == name, items), None)


class Item(Resource):
    def get(self, name):
        item = find_item(name)
        return {"item": item}, 200 if item else 404

    def post(self, name):
        if find_item(name) is not None:
            return {"message": "An item with name {} already exists".format(name)}, 400
        payload = request.get_json()
        item = {"name": name, "price": payload["price"]}
        items.append(item)
        return item, 201


class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
