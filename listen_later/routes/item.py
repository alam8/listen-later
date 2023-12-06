from flask import request
from listen_later.model.item import ItemSchema, ItemUpdateSchema
from listen_later.model.item_type import ItemType
from listen_later.model.constants import *
from listen_later.index import app, db

@app.route("/items")
def get_items():
    docs = db.collection(ITEMS).stream()
    items = []

    for doc in docs:
        items.append(ItemSchema().load(doc.to_dict()))

    return ItemSchema(many=True).dump(items)

@app.route("/items/<string:pk>")
def get_item(pk):
    doc_ref = db.collection(ITEMS).document(pk)
    item = doc_ref.get()

    if not item.exists:
        return {"errors": f"Item id={pk} could not be found"}, 404

    return item.to_dict()

@app.route("/items", methods=['POST'])
def add_item():
    doc_ref = db.collection(ITEMS).document()
    item = ItemSchema().load(request.get_json())

    item.id = doc_ref.id
    doc_ref.set(ItemSchema().dump(item))

    return f'Added {item} successfully', 201

@app.route("/items/<string:pk>", methods=['PUT', 'POST'])
def update_item(pk):
    doc_ref = db.collection(ITEMS).document(pk)
    item = doc_ref.get()

    if not item.exists:
        return {"errors": f"Item id={pk} could not be found"}, 404

    item_update = ItemUpdateSchema().load(request.get_json())

    if item_update.get(CONTENT_LINK):
        doc_ref.update({CONTENT_LINK: item_update.get(CONTENT_LINK)})
    if item_update.get(TAG_IDS):
        doc_ref.update({TAG_IDS: item_update.get(TAG_IDS)})
    if item_update.get(COLLECTION_IDS):
        doc_ref.update({COLLECTION_IDS: item_update.get(COLLECTION_IDS)})
    if item_update.get(RATING):
        doc_ref.update({RATING: item_update.get(RATING)})
    if item_update.get(LISTENED):
        doc_ref.update({LISTENED: item_update.get(LISTENED)})

    return f'Updated item id={pk} successfully with the following values:<br />{ItemUpdateSchema().dump(item_update)}', 200

@app.route("/items/<string:pk>", methods=['DELETE'])
def delete_item(pk):
    doc_ref = db.collection(ITEMS).document(pk)
    item = doc_ref.get()

    if not item.exists:
        return {"errors": f"Item id={pk} could not be found"}, 404

    doc_ref.delete()
    return f'Deleted item id={pk} successfully', 200