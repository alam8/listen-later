from listen_later.model.constants import *
from listen_later.index import app, db
from listen_later.routes import item, collection, tag
from google.cloud.firestore_v1.base_query import FieldFilter

@app.route("/collections/<string:collection_pk>/<string:item_pk>", methods=['PUT', 'POST'])
def add_item_to_collection(collection_pk, item_pk):
    # TODO: Fix error handling if collection/item not found
    collection_data = collection.get_collection(collection_pk)
    collection_ref = collection.user_collections_ref.document(collection_pk)

    # TODO: Fix collections sub-fbc of item not being copied correctly (maybe convert to map instead?)
    collection_ref.collection(ITEMS).document(item_pk).set(item.get_item(item_pk))

    items_query = db.collection_group(ITEMS).where(
        filter=FieldFilter("id", "==", item_pk)
    ).stream()

    for item_doc in items_query:
        item_doc.reference.collection(COLLECTIONS).document(collection_pk).set(collection_data)

    return f'Added Item(id={item_pk} to Collection(id={collection_pk}) successfully', 200

@app.route("/collections/<string:collection_pk>/<string:item_pk>", methods=['DELETE'])
def remove_item_from_collection(collection_pk, item_pk):
    pass

@app.route("/tags/<string:tag_pk>/<string:item_pk>", methods=['PUT', 'POST'])
def add_item_to_tag(tag_pk, item_pk):
    pass

@app.route("/tags/<string:tag_pk>/<string:item_pk>", methods=['DELETE'])
def remove_item_from_tag(tag_pk, item_pk):
    pass