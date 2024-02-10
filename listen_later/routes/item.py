from flask import current_app, request
from google.cloud.firestore_v1.base_query import FieldFilter

from listen_later.app import db
from listen_later.constants import *
from listen_later.model.item import ItemSchema, ItemUpdateSchema
from listen_later.model.item_type import ItemType
from listen_later.routes import logic, responses
from listen_later.user import user_ref


def get_item_ref(item_id=None):
    return user_ref.collection(COLLECTIONS).document(ALL_COLLECTION_ID).collection(ITEMS).document(item_id)



@current_app.route("/items")
def get_items():
    return logic.get_items_from_collection(ALL_COLLECTION_ID)


@current_app.route("/items/<string:item_id>")
def get_item(item_id):
    return logic.get_item_from_collection(ALL_COLLECTION_ID, item_id)


@current_app.route("/items", methods=["POST"])
def create_item():
    item_ref = get_item_ref()
    try:
        item = ItemSchema().load(request.get_json())
    except (IndexError, ValueError):
        return {ERRORS: f"Invalid content link. Expected link format: https://open.spotify.com/CONTENT_TYPE/CONTENT_ID"}, 400

    item.id = item_ref.id
    item_ref.set(ItemSchema().dump(item))

    all_collection_ref = user_ref.collection(COLLECTIONS).document(ALL_COLLECTION_ID)
    # Don't display the all_collection when exposing item -> collections to the user.
    item_ref.collection(COLLECTIONS).document(ALL_COLLECTION_ID).set(
        {COLLECTION_NAME: all_collection_ref.get().to_dict().get(COLLECTION_NAME)}
    )

    return responses.obj_created(item)


@current_app.route("/items/<string:item_id>", methods=["PUT", "POST"])
def update_item(item_id):
    item_ref = get_item_ref(item_id)
    item = item_ref.get()

    if not item.exists:
        return responses.not_found_error(ITEM_TYPE, item_id)

    item_update = ItemUpdateSchema().load(request.get_json())

    # Each instance of the item needs to be updated.
    items_query = db.collection_group(ITEMS).where(
        filter=FieldFilter(ID, "==", item_id)
    ).stream()

    for queried_item_doc in items_query:
        if item_update.get(CONTENT_LINK):
            queried_item_doc.reference.update({CONTENT_LINK: item_update.get(CONTENT_LINK)})
        if item_update.get(RATING):
            queried_item_doc.reference.update({RATING: item_update.get(RATING)})
        if item_update.get(LISTENED):
            queried_item_doc.reference.update({LISTENED: item_update.get(LISTENED)})

    return responses.obj_updated(ITEM_TYPE, item_id, ItemUpdateSchema().dump(item_update))


@current_app.route("/items/<string:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item_ref = get_item_ref(item_id)
    item = item_ref.get()

    if not item.exists:
        return responses.not_found_error(ITEM_TYPE, item_id)

    # Delete each instance of this item from every collection/tag it belongs to.
    items_query = db.collection_group(ITEMS).where(
        filter=FieldFilter(ID, "==", item_id)
    ).stream()
    for queried_item_doc in items_query:
        queried_item_doc.reference.delete()

    item_ref.delete()
    return responses.obj_deleted(ITEM_TYPE, item_id)
