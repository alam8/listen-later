from flask import request
from listen_later.model.collection import Collection, CollectionSchema, CollectionUpdateSchema
from listen_later.model.constants import ALL_COLLECTION_ID
from listen_later.index import app

all_collection = Collection(ALL_COLLECTION_ID, 'All')
collections = [all_collection]

@app.route("/collections")
def get_collections():
    return CollectionSchema(many=True).dump(collections)

@app.route("/collections/<int:pk>")
def get_collection(pk):
    # TODO: query collection w/ ORM
    collection = None # db.collection("Collection").document(pk)
    if not collection:
        return {"errors": "Collection could not be found"}, 404
    return CollectionSchema.dump(collection)

@app.route("/collections", methods=['POST'])
def add_collection():
    collection = CollectionSchema().load(request.get_json())
    collections.append(collection)
    return f'Added {collection} successfully', 201

@app.route("/collections/<int:pk>", methods=['PUT', 'POST'])
def update_collection(pk):
    # TODO: query collection w/ ORM
    collection = None # db.collection("Collection").document(pk)

    if pk == ALL_COLLECTION_ID:
        return {"errors": "'All' collection cannot be renamed"}, 403
    elif not collection:
        return {"errors": f"Collection id={pk} could not be found"}, 404

    collection_update = CollectionUpdateSchema().load(request.get_json())

    if collection_update.name:
        collection.update({"name": collection_update.name})

    return CollectionUpdateSchema().dump(collection_update)

@app.route("/collections/<int:pk>", methods=['DELETE'])
def delete_collection(pk):
    # TODO: query collection w/ ORM
    collection = None # db.collection("Collection").document(pk)
    try:
        delete_items = request.get_json()["delete_items"]
    except:
        delete_items = False

    if pk == ALL_COLLECTION_ID:
        return {"errors": "'All' collection cannot be deleted"}, 403
    elif not collection:
        return {"errors": f"Collection id={pk} could not be found"}, 404

    # TODO: if delete_items:
    #           remove each item in collection from items table
    #       else:
    #           remove pk from each item's collection_ids

    collections.remove(collection)
    return f'Deleted {collection} successfully', 200