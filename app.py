from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "My Item",
                "price": 9.99
            }
        ]
    }
]


@app.route('/store', methods=['POST'])
def create_store():
    payload = request.get_data()
    new_store = {
        'name': payload['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


@app.route('/store/<string:name>')
def get_store(name):
    return jsonify(get_store_by_name(name))


@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    return jsonify(get_store_by_name(name).get('items'))


@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    payload = request.get_data()
    store = get_store_by_name(name)
    new_item = {
        "name": payload['name'],
        "price": payload['price']
    }
    if store is not None:
        store['items'].append(new_item)
    return jsonify(new_item)


def get_store_by_name(name):
    return next((store for store in stores if store['name'] == name), { "message": "No store found: {}".format(name)})


app.run(port=5000)
