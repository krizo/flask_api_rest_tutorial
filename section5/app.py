from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from section5.security import authenticate, identity
from section5.user import UserRegister
from section5.item import Item, ItemList
import os

app = Flask(__name__)
secret_key = os.environ.get('FLASK_TUTORIAL_SECRET')
app.secret_key = secret_key
api = Api(app)

# create endpoint /auth where you need send username and password:
jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
