from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
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
    @jwt_required()
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
    @jwt_required()
    def get(self):
        return {"items": items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
