from flask import request
from listen_later.model.item import ItemSchema, ItemUpdateSchema
from listen_later.model.item_type import ItemType
from listen_later.index import app, db

@app.route("/items")
def get_items():
    docs = db.collection("items").stream()
    items = []

    for doc in docs:
        items.append(ItemSchema().load(doc.to_dict()))

    return ItemSchema(many=True).dump(items)

@app.route("/items/<string:pk>")
def get_item(pk):
    doc_ref = db.collection("items").document(pk)
    item = doc_ref.get()

    if not item.exists:
        return {"errors": f"Item id={pk} could not be found"}, 404

    return item.to_dict()

@app.route("/items", methods=['POST'])
def add_item():
    doc_ref = db.collection("items").document()
    item = ItemSchema().load(request.get_json())

    item.id = doc_ref.id
    doc_ref.set(ItemSchema().dump(item))

    return f'Added {item} successfully', 201

@app.route("/items/<string:pk>", methods=['PUT', 'POST'])
def update_item(pk):
    doc_ref = db.collection("items").document(pk)
    item = doc_ref.get()

    if not item.exists:
        return {"errors": f"Item id={pk} could not be found"}, 404

    item_update = ItemUpdateSchema().load(request.get_json())

    if item_update.get("content_link"):
        doc_ref.update({"content_link": item_update.get("content_link")})
    if item_update.get("tag_ids"):
        doc_ref.update({"tag_ids": item_update.get("tag_ids")})
    if item_update.get("collection_ids"):
        doc_ref.update({"collection_ids": item_update.get("collection_ids")})
    if item_update.get("rating"):
        doc_ref.update({"rating": item_update.get("rating")})
    if item_update.get("listened"):
        doc_ref.update({"listened": item_update.get("listened")})

    return f'Updated item id={pk} successfully with the following values:<br />{ItemUpdateSchema().dump(item_update)}', 200

@app.route("/items/<string:pk>", methods=['DELETE'])
def delete_item(pk):
    doc_ref = db.collection("items").document(pk)
    item = doc_ref.get()

    if not item.exists:
        return {"errors": f"Item id={pk} could not be found"}, 404

    doc_ref.delete()
    return f'Deleted item id={pk} successfully', 200