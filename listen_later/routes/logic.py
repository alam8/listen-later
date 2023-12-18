from google.cloud.firestore_v1.base_query import FieldFilter

from listen_later.constants import *
from listen_later.index import db, flask_app
import listen_later.routes.collection as collection
import listen_later.routes.item as item
from listen_later.routes.responses import *
import listen_later.routes.tag as tag

def add_item_to_group(group_type, group_id, item_id):
    if group_type == COLLECTION_TYPE:
        group_ref = collection.get_collection_ref(group_id)
    elif group_type == TAG_TYPE:
        group_ref = tag.get_tag_ref(group_id)

    group_doc = group_ref.get()

    if not group_doc.exists:
        return not_found_error(group_type, group_id)
    elif group_type == COLLECTION_TYPE and group_id == ALL_COLLECTION_ID:
        return {ERRORS: f"{ITEM_TYPE} cannot be added to {ALL_COLLECTION_ID}"}, 403

    item_ref = item.get_item_ref(item_id)
    item_doc = item_ref.get()

    if not item_doc.exists:
        return not_found_error(ITEM_TYPE, item_id)
    elif item_ref.collection(group_type).document(group_id).get().exists:
        return {ERRORS: f"{ITEM_TYPE}({ID}={item_id}) already exists in {group_type}({ID}={group_id})"}, 403

    added_item_ref = group_ref.collection(ITEMS).document(item_id)
    added_item_ref.set(item_doc.to_dict())
    item_groups_ref = item_ref.collection(group_type).stream()
    for item_group_ref in item_groups_ref:
        added_item_ref.collection(group_type).document(item_group_ref.id).set(item_group_ref.to_dict())

    items_query = db.collection_group(ITEMS).where(
        filter=FieldFilter(ID, "==", item_id)
    ).stream()
    for queried_item_doc in items_query:
        queried_item_doc.reference.collection(group_type).document(group_id).set(group_doc.to_dict())

    return f"Added {ITEM_TYPE}({ID}={item_id}) to {group_type}({ID}={group_id}) successfully", 200

def remove_item_from_group(group_type, group_id, item_id):
    pass

@flask_app.route("/collections/<string:collection_id>/<string:item_id>", methods=["PUT", "POST"])
def add_item_to_collection(collection_id, item_id):
    return add_item_to_group(COLLECTION_TYPE, collection_id, item_id)

@flask_app.route("/tags/<string:tag_id>/<string:item_id>", methods=["PUT", "POST"])
def add_item_to_tag(tag_id, item_id):
    return add_item_to_group(TAG_TYPE, tag_id, item_id)

@flask_app.route("/collections/<string:collection_id>/<string:item_id>", methods=["DELETE"])
def remove_item_from_collection(collection_id, item_id):
    return remove_item_from_group(COLLECTION_TYPE, collection_id, item_id)

@flask_app.route("/tags/<string:tag_id>/<string:item_id>", methods=["DELETE"])
def remove_item_from_tag(tag_id, item_id):
    return remove_item_from_group(TAG_TYPE, tag_id, item_id)