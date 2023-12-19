from flask import request

from listen_later.constants import *
from listen_later.index import flask_app, user_ref
from listen_later.model.collection import CollectionSchema, CollectionUpdateSchema
from listen_later.routes import responses

user_collections_ref = user_ref.collection(COLLECTIONS)


@flask_app.route("/collections")
def get_collections():
    collections_ref = user_collections_ref.stream()
    all_collections = []

    for collection_ref in collections_ref:
        all_collections.append(CollectionSchema().load(collection_ref.to_dict))

    return CollectionSchema(many=True).dump(all_collections)


def get_collection_ref(collection_id=None):
    return user_collections_ref.document(collection_id)


@flask_app.route("/collections/<string:collection_id>")
def get_collection(collection_id):
    collection = get_collection_ref(collection_id).get()

    if not collection.exists:
        return responses.not_found_error(COLLECTION_TYPE, collection_id)

    return collection.to_dict()


@flask_app.route("/collections", methods=["POST"])
def create_collection():
    collection_ref = get_collection_ref()
    collection = CollectionSchema().load(request.get_json())

    collection.id = collection_ref.id
    collection_ref.set(CollectionSchema().dump(collection))

    return responses.obj_created(collection)


@flask_app.route("/collections/<string:collection_id>", methods=["PUT", "POST"])
def update_collection(collection_id):
    collection_ref = get_collection_ref(collection_id)
    collection = collection_ref.get()

    if not collection.exists:
        return responses.not_found_error(COLLECTION_TYPE, collection_id)
    elif collection_id == ALL_COLLECTION_ID:
        return {ERRORS: f"{ALL_COLLECTION_ID} cannot be renamed."}, 403

    collection_update = CollectionUpdateSchema().load(request.get_json())

    if collection_update.get(COLLECTION_NAME):
        collection_ref.update({COLLECTION_NAME: collection_update.get(COLLECTION_NAME)})

    return responses.obj_updated(COLLECTION_TYPE, collection_id, CollectionUpdateSchema().dump(collection_update))


@flask_app.route("/collections/<string:collection_id>", methods=["DELETE"])
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

    # TODO: if delete_items:
    #           delete every item in this collection from all other collections
    #       else:
    #           remove only this collection from each instance of every item in
    #           this collection's sub-fbc of collections

    collection_ref.delete()
    return responses.obj_deleted(COLLECTION_TYPE, collection_id)
