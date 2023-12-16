from flask import request
from listen_later.model.collection import CollectionSchema, CollectionUpdateSchema
from listen_later.model.constants import *
from listen_later.index import app, user_ref, not_found_error

user_collections_ref = user_ref.collection(COLLECTIONS)

@app.route("/collections")
def get_collections():
    collections_ref = user_collections_ref.stream()
    all_collections = []

    for collection_ref in collections_ref:
        all_collections.append(CollectionSchema().load(collection_ref.to_dict))

    return CollectionSchema(many=True).dump(all_collections)

def get_collection_ref(id=None):
    return user_collections_ref.document(id)

@app.route("/collections/<string:id>")
def get_collection(id):
    collection = get_collection_ref(id).get()

    if not collection.exists:
        return not_found_error(COLLECTION_TYPE, id)

    return collection.to_dict()

@app.route("/collections", methods=["POST"])
def create_collection():
    collection_ref = get_collection_ref()
    collection = CollectionSchema().load(request.get_json())

    collection.id = collection_ref.id
    collection_ref.set(CollectionSchema().dump(collection))

    return f"Created {collection} successfully", 201

@app.route("/collections/<string:id>", methods=["PUT", "POST"])
def update_collection(id):
    collection_ref = get_collection_ref(id)
    collection = collection_ref.get()

    if not collection.exists:
        return not_found_error(COLLECTION_TYPE, id)
    elif id == ALL_COLLECTION_ID:
        return {"errors": "All collection cannot be renamed"}, 403

    collection_update = CollectionUpdateSchema().load(request.get_json())

    if collection_update.get(COLLECTION_NAME):
        collection_ref.update({COLLECTION_NAME: collection_update.get(COLLECTION_NAME)})

    return f"Updated collection id={id} successfully with the following values:<br />{CollectionUpdateSchema().dump(collection_update)}", 200

@app.route("/collections/<string:id>", methods=["DELETE"])
def delete_collection(id):
    collection_ref = get_collection_ref(id)
    collection = collection_ref.get()

    try:
        delete_items = request.get_json()["delete_items"]
    except:
        delete_items = False

    if not collection.exists:
        return not_found_error(COLLECTION_TYPE, id)
    elif id == ALL_COLLECTION_ID:
        return {"errors": "All collection cannot be deleted"}, 403

    # TODO: if delete_items:
    #           delete every item in this collection from all other collections
    #       else:
    #           remove only this collection from each instance of every item in
    #           this collection's sub-fbc of collections

    collection_ref.delete()
    return f"Deleted collection id={id} successfully", 200