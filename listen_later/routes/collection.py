from flask import request
from listen_later.model.collection import Collection, CollectionSchema, CollectionUpdateSchema
from listen_later.model.constants import *
from listen_later.index import app, db

# all_collection = Collection(ALL_COLLECTION_ID, 'All')
# collections = [all_collection]

@app.route("/collections")
def get_collections():
    docs = db.collection(COLLECTIONS).stream()
    collections = []

    for doc in docs:
        collections.append(CollectionSchema().load(doc.to_dict))

    return CollectionSchema(many=True).dump(collections)

@app.route("/collections/<string:pk>")
def get_collection(pk):
    doc_ref = db.collection("Collection").document(pk)
    collection = doc_ref.get()

    if not collection.exists:
        return {"errors": f"Collection id={pk} could not be found"}, 404

    return collection.to_dict()

@app.route("/collections", methods=['POST'])
def add_collection():
    doc_ref = db.collection(COLLECTIONS).document()
    collection = CollectionSchema().load(request.get_json())

    collection.id = doc_ref.id
    doc_ref.set(CollectionSchema().dump(collection))

    return f'Added {collection} successfully', 201

@app.route("/collections/<string:pk>", methods=['PUT', 'POST'])
def update_collection(pk):
    doc_ref = db.collection(COLLECTIONS).document(pk)
    collection = doc_ref.get()

    if not collection.exists:
        return {"errors": f"Collection id={pk} could not be found"}, 404
    elif pk == ALL_COLLECTION_ID:
        return {"errors": "'All' collection cannot be renamed"}, 403

    collection_update = CollectionUpdateSchema().load(request.get_json())

    if collection_update.get(COLLECTION_NAME):
        doc_ref.update({COLLECTION_NAME: collection_update.get(COLLECTION_NAME)})

    return f'Updated collection id={pk} successfully with the following values:<br />{CollectionUpdateSchema().dump(collection_update)}', 200

@app.route("/collections/<string:pk>", methods=['DELETE'])
def delete_collection(pk):
    doc_ref = db.collection("Collection").document(pk)
    collection = doc_ref.get()

    try:
        delete_items = request.get_json()["delete_items"]
    except:
        delete_items = False

    if not collection.exists:
        return {"errors": f"Collection id={pk} could not be found"}, 404
    elif pk == ALL_COLLECTION_ID:
        return {"errors": "'All' collection cannot be deleted"}, 403

    # TODO: if delete_items:
    #           remove each item in collection from items table
    #       else:
    #           remove pk from each item's collection_ids

    doc_ref.delete()
    return f'Deleted collection id={pk} successfully', 200