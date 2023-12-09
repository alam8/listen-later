from flask import request
from listen_later.model.item import ItemSchema, ItemUpdateSchema
from listen_later.model.item_type import ItemType
from listen_later.model.constants import *
from listen_later.index import app, user_ref

@app.route("/items")
def get_items():
    items_ref = user_ref.collection(ITEMS).stream()
    all_items = []

    for item_ref in items_ref:
        all_items.append(ItemSchema().load(item_ref.to_dict()))

    return ItemSchema(many=True).dump(all_items)

@app.route("/items/<string:pk>")
def get_item(pk):
    item_ref = user_ref.collection(ITEMS).document(pk)
    item = item_ref.get()

    if not item.exists:
        return {"errors": f"Item id={pk} could not be found"}, 404

    return item.to_dict()

@app.route("/items", methods=['POST'])
def add_item():
    item_ref = user_ref.collection(ITEMS).document()
    item = ItemSchema().load(request.get_json())

    item.id = item_ref.id
    item_ref.set(ItemSchema().dump(item))

    all_collection_ref = user_ref.collection(COLLECTIONS).document(ALL_COLLECTION_ID)
    all_collection_ref.collection(ITEMS).document(item.id).set({"id": item_ref.id})
    item_ref.collection(COLLECTIONS).document(ALL_COLLECTION_ID).set({COLLECTION_NAME: all_collection_ref.get().to_dict().get(COLLECTION_NAME)})

    return f'Added {item} successfully', 201

@app.route("/items/<string:pk>", methods=['PUT', 'POST'])
def update_item(pk):
    item_ref = user_ref.collection(ITEMS).document(pk)
    item = item_ref.get()

    if not item.exists:
        return {"errors": f"Item id={pk} could not be found"}, 404

    item_update = ItemUpdateSchema().load(request.get_json())

    if item_update.get(CONTENT_LINK):
        item_ref.update({CONTENT_LINK: item_update.get(CONTENT_LINK)})
    if item_update.get(TAG_IDS):
        item_ref.update({TAG_IDS: item_update.get(TAG_IDS)})
    if item_update.get(COLLECTION_IDS):
        item_ref.update({COLLECTION_IDS: item_update.get(COLLECTION_IDS)})
    if item_update.get(RATING):
        item_ref.update({RATING: item_update.get(RATING)})
    if item_update.get(LISTENED):
        item_ref.update({LISTENED: item_update.get(LISTENED)})

    return f'Updated item id={pk} successfully with the following values:<br />{ItemUpdateSchema().dump(item_update)}', 200

@app.route("/items/<string:pk>", methods=['DELETE'])
def delete_item(pk):
    item_ref = user_ref.collection(ITEMS).document(pk)
    item = item_ref.get()

    if not item.exists:
        return {"errors": f"Item id={pk} could not be found"}, 404

    # TODO: Delete instance of item from every collection/tag it belongs to
    item_ref.delete()
    return f'Deleted item id={pk} successfully', 200