from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from section6.security import authenticate, identity
from section6.resources.user import UserRegister
from section6.resources.item import Item, ItemList
from section6.resources.store import Store, StoreList
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
secret_key = os.environ.get('FLASK_TUTORIAL_SECRET')
app.secret_key = secret_key
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all( )

# create endpoint /auth where you need send username and password:
jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == "__main__":
    from section6.db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
