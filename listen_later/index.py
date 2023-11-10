from flask import Flask, jsonify, request

from listen_later.model.item import Item, ItemSchema
from listen_later.model.item_type import ItemType

app = Flask(__name__)

items = []

@app.route("/items")
def get_items():
    return jsonify(items)

@app.route("/items", methods=['POST'])
def add_item():
    item = ItemSchema().load(request.get_json())
    items.append(item.make_item())
    return '', 204

if __name__ == "__main__":
    app.run()