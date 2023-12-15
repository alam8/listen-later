from flask import request
from listen_later.model.item import ItemSchema, ItemUpdateSchema
from listen_later.model.item_type import ItemType
from listen_later.model.constants import *
from listen_later.index import app, user_ref, not_found_error

# TODO: test whether all_collection needs to be created upon user initialization or if Firebase will
#       automatically create it without issues
user_all_items_ref = user_ref.collection(COLLECTIONS).document(ALL_COLLECTION_ID).collection(ITEMS)

@app.route("/items")
def get_items():
    items_ref = user_all_items_ref.stream()
    all_items = []

    for item_ref in items_ref:
        all_items.append(ItemSchema().load(item_ref.to_dict()))

    return ItemSchema(many=True).dump(all_items)

def get_item_ref(pk=None):
    return user_all_items_ref.document(pk)

@app.route("/items/<string:pk>")
def get_item(pk):
    item_ref = get_item_ref(pk)
    item = item_ref.get()

    if not item.exists:
        return not_found_error(ITEM_TYPE, pk)

    return item.to_dict()

@app.route("/items", methods=['POST'])
def create_item():
    item_ref = get_item_ref()
    item = ItemSchema().load(request.get_json())

    item.id = item_ref.id
    item_ref.set(ItemSchema().dump(item))

    all_collection_ref = user_ref.collection(COLLECTIONS).document(ALL_COLLECTION_ID)
    # Note: Don't display the all_collection when exposing item -> collections to the user
    item_ref.collection(COLLECTIONS).document(ALL_COLLECTION_ID).set({COLLECTION_NAME: all_collection_ref.get().to_dict().get(COLLECTION_NAME)})

    return f'Created {item} successfully', 201

@app.route("/items/<string:pk>", methods=['PUT', 'POST'])
def update_item(pk):
    item_ref = get_item_ref(pk)
    item = item_ref.get()

    if not item.exists:
        return not_found_error(ITEM_TYPE, pk)

    item_update = ItemUpdateSchema().load(request.get_json())

    if item_update.get(CONTENT_LINK):
        item_ref.update({CONTENT_LINK: item_update.get(CONTENT_LINK)})
    if item_update.get(RATING):
        item_ref.update({RATING: item_update.get(RATING)})
    if item_update.get(LISTENED):
        item_ref.update({LISTENED: item_update.get(LISTENED)})

    return f'Updated item id={pk} successfully with the following values:<br />{ItemUpdateSchema().dump(item_update)}', 200

@app.route("/items/<string:pk>", methods=['DELETE'])
def delete_item(pk):
    item_ref = get_item_ref(pk)
    item = item_ref.get()

    if not item.exists:
        return not_found_error(ITEM_TYPE, pk)

    # TODO: delete instance of item from every collection/tag it belongs to

    item_ref.delete()
    return f'Deleted item id={pk} successfully', 200