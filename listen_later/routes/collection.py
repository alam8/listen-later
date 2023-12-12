from flask import request
from listen_later.model.collection import CollectionSchema, CollectionUpdateSchema
from listen_later.model.constants import *
from listen_later.index import app, user_ref

user_collections_ref = user_ref.collection(COLLECTIONS)

@app.route("/collections")
def get_collections():
    collections_ref = user_collections_ref.stream()
    all_collections = []

    for collection_ref in collections_ref:
        all_collections.append(CollectionSchema().load(collection_ref.to_dict))

    return CollectionSchema(many=True).dump(all_collections)

@app.route("/collections/<string:pk>")
def get_collection(pk):
    collection_ref = user_collections_ref.document(pk)
    collection = collection_ref.get()

    if not collection.exists:
        return {"errors": f"Collection id={pk} could not be found"}, 404

    return collection.to_dict()

@app.route("/collections", methods=['POST'])
def create_collection():
    collection_ref = user_collections_ref.document()
    collection = CollectionSchema().load(request.get_json())

    collection.id = collection_ref.id
    collection_ref.set(CollectionSchema().dump(collection))

    return f'Created {collection} successfully', 201

@app.route("/collections/<string:pk>", methods=['PUT', 'POST'])
def update_collection(pk):
    collection_ref = user_collections_ref.document(pk)
    collection = collection_ref.get()

    if not collection.exists:
        return {"errors": f"Collection id={pk} could not be found"}, 404
    elif pk == ALL_COLLECTION_ID:
        return {"errors": "All collection cannot be renamed"}, 403

    collection_update = CollectionUpdateSchema().load(request.get_json())

    if collection_update.get(COLLECTION_NAME):
        collection_ref.update({COLLECTION_NAME: collection_update.get(COLLECTION_NAME)})

    return f'Updated collection id={pk} successfully with the following values:<br />{CollectionUpdateSchema().dump(collection_update)}', 200

@app.route("/collections/<string:pk>", methods=['DELETE'])
def delete_collection(pk):
    collection_ref = user_collections_ref.document(pk)
    collection = collection_ref.get()

    try:
        delete_items = request.get_json()["delete_items"]
    except:
        delete_items = False

    if not collection.exists:
        return {"errors": f"Collection id={pk} could not be found"}, 404
    elif pk == ALL_COLLECTION_ID:
        return {"errors": "All collection cannot be deleted"}, 403

    # TODO: if delete_items:
    #           remove each item in collection from items table
    #       else:
    #           remove pk from each item's collection_ids

    collection_ref.delete()
    return f'Deleted collection id={pk} successfully', 200