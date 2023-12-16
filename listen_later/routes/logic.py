from listen_later.model.constants import *
from listen_later.index import app, db, not_found_error
from listen_later.routes import item, collection, tag
from google.cloud.firestore_v1.base_query import FieldFilter

# TODO: Look into refactoring so collection/tag functions can be merged together

@app.route("/collections/<string:collection_pk>/<string:item_pk>", methods=['PUT', 'POST'])
def add_item_to_collection(collection_pk, item_pk):
    collection_ref = collection.get_collection_ref(collection_pk)
    collection_doc = collection_ref.get()

    if not collection_doc.exists:
        return not_found_error(COLLECTION_TYPE, collection_pk)
    elif collection_pk == ALL_COLLECTION_ID:
        return {"errors": "Items cannot be added to All collection"}, 403
    
    item_ref = item.get_item_ref(item_pk)
    item_doc = item_ref.get()

    if not item_doc.exists:
        return not_found_error(ITEM_TYPE, item_pk)

    added_item_ref = collection_ref.collection(ITEMS).document(item_pk)
    added_item_ref.set(item_doc.to_dict())

    item_collections_ref = item_ref.collection(COLLECTIONS).stream()
    for item_collection_ref in item_collections_ref:
        added_item_ref.collection(COLLECTIONS).document(item_collection_ref.id).set(item_collection_ref.to_dict())

    items_query = db.collection_group(ITEMS).where(
        filter=FieldFilter("id", "==", item_pk)
    ).stream()
    for queried_item_doc in items_query:
        queried_item_doc.reference.collection(COLLECTIONS).document(collection_pk).set(collection_doc.to_dict())

    return f'Added Item(id={item_pk}) to Collection(id={collection_pk}) successfully', 200

@app.route("/collections/<string:collection_pk>/<string:item_pk>", methods=['DELETE'])
def remove_item_from_collection(collection_pk, item_pk):
    pass

@app.route("/tags/<string:tag_pk>/<string:item_pk>", methods=['PUT', 'POST'])
def add_item_to_tag(tag_pk, item_pk):
    tag_ref = tag.get_tag_ref(tag_pk)
    tag_doc = tag_ref.get()

    if not tag_doc.exists:
        return not_found_error(TAG_TYPE, tag_pk)

    item_ref = item.get_item_ref(item_pk)
    item_doc = item_ref.get()

    if not item_doc.exists:
        return not_found_error(ITEM_TYPE, item_pk)

    added_item_ref = tag_ref.collection(ITEMS).document(item_pk)
    added_item_ref.set(item_doc.to_dict())

    item_tags_ref = item_ref.collection(TAGS).stream()
    for item_tag_ref in item_tags_ref:
        added_item_ref.collection(TAGS).document(item_tag_ref.id).set(item_tag_ref.to_dict())

    items_query = db.collection_group(ITEMS).where(
        filter=FieldFilter("id", "==", item_pk)
    ).stream()
    for queried_item_doc in items_query:
        queried_item_doc.reference.collection(TAGS).document(tag_pk).set(tag_doc.to_dict())

    return f'Added Item(id={item_pk}) to Tag(id={tag_pk}) successfully', 200

@app.route("/tags/<string:tag_pk>/<string:item_pk>", methods=['DELETE'])
def remove_item_from_tag(tag_pk, item_pk):
    pass