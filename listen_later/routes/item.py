from flask import request
from listen_later.model.item import ItemSchema, ItemUpdateSchema
from listen_later.model.item_type import ItemType
from listen_later.index import app

items = []

@app.route("/items")
def get_items():
    return ItemSchema(many=True).dump(items)

@app.route("/items/<int:pk>")
def get_item(pk):
    # TODO: query item w/ ORM
    item = None # db.collection("Item").document(pk)
    if not item:
        return {"errors": "Item could not be found"}, 404
    return ItemSchema.dump(item)

@app.route("/items", methods=['POST'])
def add_item():
    item = ItemSchema().load(request.get_json())
    items.append(item)
    return f'Added {item} successfully', 201

@app.route("/items/<int:pk>", methods=['PUT', 'POST'])
def update_item(pk):
    # TODO: query item w/ ORM
    item = None # db.collection("Item").document(pk)

    if not item:
        return {"errors": f"Item id={pk} could not be found"}, 404

    item_update = ItemUpdateSchema().load(request.get_json())

    if item_update.content_link:
        item.update({"content_link": item_update.content_link})
    if item_update.tag_ids:
        item.update({"tag_ids": item_update.tag_ids})
    if item_update.collection_ids:
        item.update({"collection_ids": item_update.collection_ids})
    if item_update.rating:
        item.update({"ratings": item_update.ratings})
    if item_update.listened:
        item.update({"listened": item_update.listened})

    return ItemUpdateSchema().dump(item_update)

@app.route("/items/<int:pk>", methods=['DELETE'])
def delete_item(pk):
    # TODO: query item w/ ORM
    item = None # db.collection("Item").document(pk)

    if not item:
        return {"errors": f"Item id={pk} could not be found"}, 404

    items.remove(item)
    return f'Deleted {item} successfully', 200