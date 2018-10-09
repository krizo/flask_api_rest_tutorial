from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from section5.security import authenticate, identity
from section5.user import UserRegister
import os

app = Flask(__name__)
secret_key = os.environ.get('FLASK_TUTORIAL_SECRET')
app.secret_key = secret_key
api = Api(app)

# create endpoint /auth where you need send username and password:
jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)

items = []


def find_item(name):
    return next(filter(lambda x: x['name'] == name, items), None)


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str, help="name can't be blank!")
    parser.add_argument('price', required=False, type=float)

    @jwt_required()
    def get(self, name):
        item = find_item(name)
        return {"item": item}, 200 if item else 404

    @jwt_required()
    def post(self, name):
        if find_item(name) is not None:
            return {"message": "An item with name {} already exists".format(name)}, 400

        payload = Item.parser.parse_args()
        item = {"name": name, "price": payload["price"]}
        items.append(item)
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


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
