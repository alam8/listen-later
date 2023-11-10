from flask import Flask, jsonify, request

from listen_later.model.constants import ALL_COLLECTION_ID
from listen_later.model.item import ItemSchema
from listen_later.model.tag import TagSchema
from listen_later.model.collection import Collection, CollectionSchema
from listen_later.model.item_type import ItemType

app = Flask(__name__)

all_collection = Collection(ALL_COLLECTION_ID, 'All')
items = []
collections = [all_collection]
tags = []


@app.route("/items")
def get_items():
    return ItemSchema(many=True).dump(items)

@app.route("/items", methods=['POST'])
def add_item():
    item = ItemSchema().load(request.get_json())
    items.append(item)
    return f'Added {item} successfully', 201


@app.route("/collections")
def get_collections():
    return CollectionSchema(many=True).dump(collections)

@app.route("/collections/<int:pk>")
def get_collection(pk):
    # TODO: query collection w/ ORM
    collection = None # Collection.get(Collection.id == pk)
    if not collection:
        return {"errors": "Collection could not be found"}, 404
    return CollectionSchema.dump(collection)

@app.route("/collections", methods=['POST'])
def create_collection():
    collection = CollectionSchema().load(request.get_json())
    collections.append(collection)
    return f'Added {collection} successfully', 201

@app.route("/collections/<int:pk>", methods=['PUT', 'POST'])
def update_collection(pk):
    # TODO: query collection w/ ORM
    collection = None # Collection.get(Collection.id == pk)
    try:
        new_name = request.get_json()["name"]
    except:
        return {"errors": "Name not provided"}, 400

    if pk == ALL_COLLECTION_ID:
        return {"errors": "'All' collection cannot be renamed"}, 403
    elif not collection:
        return {"errors": f"Collection id={pk} could not be found"}, 404

    update_name = collection.update(name=new_name)
    update_name.execute()
    return CollectionSchema().dump(collection)

@app.route("/collections/<int:pk>", methods=['DELETE'])
def delete_collection(pk):
    # TODO: query collection w/ ORM
    collection = None # Collection.get(Collection.id == pk)
    try:
        delete_items = request.get_json()["delete_items"]
    except:
        delete_items = False

    if pk == ALL_COLLECTION_ID:
        return {"errors": "'All' collection cannot be deleted"}, 403
    elif not collection:
        return {"errors": f"Collection id={pk} could not be found - {delete_items}"}, 404

    # TODO: if delete_items:
    #           remove each item in collection from items table
    #       else:
    #           remove pk from each item's collection_ids

    collections.remove(collection)
    return f'Deleted {collection} successfully', 200


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