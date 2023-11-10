from flask import Flask, jsonify, request

from listen_later.model.constants import ALL_COLLECTION_ID
from listen_later.model.item import ItemSchema
from listen_later.model.tag import TagSchema
from listen_later.model.collection import Collection
from listen_later.model.item_type import ItemType

app = Flask(__name__)

all_collection = Collection(ALL_COLLECTION_ID, 'All')
items = []
tags = []

@app.route("/items")
def get_items():
    return ItemSchema(many=True).dump(items)

@app.route("/items", methods=['POST'])
def add_item():
    item = ItemSchema().load(request.get_json())
    items.append(item)
    return '', 204

@app.route("/tags")
def get_tags():
    return TagSchema(many=True).dump(tags)

@app.route("/tags", methods=['POST'])
def add_tag():
    tag = TagSchema().load(request.get_json())
    tags.append(tag)
    return '', 204

if __name__ == "__main__":
    app.run()