from flask import current_app, request
from google.cloud.firestore_v1.base_query import FieldFilter

from listen_later.app import db
from listen_later.constants import *
from listen_later.model.collection import CollectionSchema, CollectionUpdateSchema
from listen_later.routes import responses
from listen_later.user import user_ref

user_collections_ref = user_ref.collection(COLLECTIONS)


def get_collection_ref(collection_id=None):
    return user_collections_ref.document(collection_id)



@current_app.route("/collections")
def get_collections():
    collections_ref = user_collections_ref.stream()
    all_collections = []

    for collection_ref in collections_ref:
        all_collections.append(CollectionSchema().load(collection_ref.to_dict()))

    return CollectionSchema(many=True).dump(all_collections)


@current_app.route("/collections/<string:collection_id>")
def get_collection(collection_id):
    collection = get_collection_ref(collection_id).get()

    if not collection.exists:
        return responses.not_found_error(COLLECTION_TYPE, collection_id)

    return collection.to_dict()


@current_app.route("/collections", methods=["POST"])
def create_collection():
    collection_ref = get_collection_ref()
    collection = CollectionSchema().load(request.get_json())

    collection.id = collection_ref.id
    collection_ref.set(CollectionSchema().dump(collection))

    return responses.obj_created(collection)


@current_app.route("/collections/<string:collection_id>", methods=["PUT", "POST"])
def update_collection(collection_id):
    collection_ref = get_collection_ref(collection_id)
    collection = collection_ref.get()

    if not collection.exists:
        return responses.not_found_error(COLLECTION_TYPE, collection_id)
    elif collection_id == ALL_COLLECTION_ID:
        return {ERRORS: f"{ALL_COLLECTION_ID} cannot be renamed."}, 403

    collection_update = CollectionUpdateSchema().load(request.get_json())

    # TODO: each instance of the collection needs to be updated
    if collection_update.get(COLLECTION_NAME):
        collection_ref.update({COLLECTION_NAME: collection_update.get(COLLECTION_NAME)})

    return responses.obj_updated(COLLECTION_TYPE, collection_id, CollectionUpdateSchema().dump(collection_update))


@current_app.route("/collections/<string:collection_id>", methods=["DELETE"])
def delete_collection(collection_id):
    collection_ref = get_collection_ref(collection_id)
    collection = collection_ref.get()

    try:
        delete_items = request.get_json()["delete_items"]
    except:
        delete_items = False

    if not collection.exists:
        return responses.not_found_error(COLLECTION_TYPE, collection_id)
    if collection_id == ALL_COLLECTION_ID:
        return {ERRORS: f"{ALL_COLLECTION_ID} cannot be deleted."}, 403

    # If delete_items, delete each instance of every item in this collection
    # from every collection/tag it belongs to.
    # Else, remove this collection from each instance of every item in this
    # collection's sub-fbc of collections.
    for item in collection_ref.collection(ITEMS).stream():
        items_query = db.collection_group(ITEMS).where(
            filter=FieldFilter(ID, "==", item.id)
        ).stream()
        for queried_item_doc in items_query:
            if delete_items:
                queried_item_doc.reference.delete()
            else:
                queried_item_doc.reference.collection(COLLECTIONS).document(collection_id).delete()

    collection_ref.delete()
    return responses.obj_deleted(COLLECTION_TYPE, collection_id)
