from flask import current_app
from google.cloud.firestore_v1.base_query import FieldFilter

from listen_later.constants import *
from listen_later.app import db
from listen_later.model.item import ItemSchema
from listen_later.routes import collection, item, responses, tag


def set_group_vars(group_type, group_id):
    if group_type == COLLECTION_TYPE:
        group_ref = collection.get_collection_ref(group_id)
        fbc_name = COLLECTIONS
    elif group_type == TAG_TYPE:
        group_ref = tag.get_tag_ref(group_id)
        fbc_name = TAGS

    group_doc = group_ref.get()

    return (group_ref, group_doc, fbc_name)



def get_items_from_group(group_type, group_id):
    group_ref, group_doc, fbc_name = set_group_vars(group_type, group_id)

    if not group_doc.exists:
        return responses.not_found_error(group_type, group_id)

    items_ref = group_ref.collection(ITEMS).stream()
    items = []

    for item_ref in items_ref:
        items.append(ItemSchema().load(item_ref.to_dict()))

    return ItemSchema(many=True).dump(items)


def get_item_from_group(group_type, group_id, item_id):
    group_ref, group_doc, fbc_name = set_group_vars(group_type, group_id)

    if not group_doc.exists:
        return responses.not_found_error(group_type, group_id)

    item_ref = group_ref.collection(ITEMS).document(item_id)
    item_doc = item_ref.get()

    if not item_doc.exists:
        return responses.not_found_error(ITEM_TYPE, item_id)

    return item_doc.to_dict()


def add_item_to_group(group_type, group_id, item_id):
    group_ref, group_doc, fbc_name = set_group_vars(group_type, group_id)

    if not group_doc.exists:
        return responses.not_found_error(group_type, group_id)
    if group_type == COLLECTION_TYPE and group_id == ALL_COLLECTION_ID:
        return {ERRORS: f"{ITEM_TYPE}s cannot be added to the {ALL_COLLECTION_ID}."}, 403

    item_ref = item.get_item_ref(item_id)
    item_doc = item_ref.get()

    if not item_doc.exists:
        return responses.not_found_error(ITEM_TYPE, item_id)
    if item_ref.collection(fbc_name).document(group_id).get().exists:
        return {ERRORS: f"{ITEM_TYPE}({ID}={item_id}) already exists in {group_type}({ID}={group_id})."}, 403

    added_item_ref = group_ref.collection(ITEMS).document(item_id)
    added_item_ref.set(item_doc.to_dict())

    # Set the added item's existing collections and tags sub-fbcs since they aren't automatically copied.
    item_collections_ref = item_ref.collection(COLLECTIONS).stream()
    item_tags_ref = item_ref.collection(TAGS).stream()
    for item_collection_ref in item_collections_ref:
        added_item_ref.collection(COLLECTIONS).document(item_collection_ref.id).set(item_collection_ref.to_dict())
    for item_tag_ref in item_tags_ref:
        added_item_ref.collection(TAGS).document(item_tag_ref.id).set(item_tag_ref.to_dict())

    items_query = db.collection_group(ITEMS).where(
        filter=FieldFilter(ID, "==", item_id)
    ).stream()
    for queried_item_doc in items_query:
        queried_item_doc.reference.collection(fbc_name).document(group_id).set(group_doc.to_dict())

    return f"Added {ITEM_TYPE}({ID}={item_id}) to {group_type}({ID}={group_id}) successfully.", 200


def remove_item_from_group(group_type, group_id, item_id):
    group_ref, group_doc, fbc_name = set_group_vars(group_type, group_id)

    if not group_doc.exists:
        return responses.not_found_error(group_type, group_id)
    if group_type == COLLECTION_TYPE and group_id == ALL_COLLECTION_ID:
        return {ERRORS: f"{ITEM_TYPE}s cannot be removed from the {ALL_COLLECTION_ID}. Delete it instead."}, 403

    item_ref = item.get_item_ref(item_id)
    item_doc = item_ref.get()

    if not item_doc.exists:
        return responses.not_found_error(ITEM_TYPE, item_id)
    if not item_ref.collection(fbc_name).document(group_id).get().exists:
        return {ERRORS: f"{ITEM_TYPE}({ID}={item_id}) does not exist in {group_type}({ID}={group_id})."}, 403

    items_query = db.collection_group(ITEMS).where(
        filter=FieldFilter(ID, "==", item_id)
    ).stream()
    for queried_item_doc in items_query:
        queried_item_doc.reference.collection(fbc_name).document(group_id).delete()

    # TODO: delete the item's collections and tags sub-fbcs first
    group_ref.collection(ITEMS).document(item_id).delete()

    return f"Removed {ITEM_TYPE}({ID}={item_id}) from {group_type}({ID}={group_id}) successfully.", 200



@current_app.route("/collections/<string:collection_id>/items")
def get_items_from_collection(collection_id):
    return get_items_from_group(COLLECTION_TYPE, collection_id)


@current_app.route("/tags/<string:tag_id>/items")
def get_items_from_tag(tag_id):
    return get_items_from_group(TAG_TYPE, tag_id)


@current_app.route("/collections/<string:collection_id>/<string:item_id>")
def get_item_from_collection(collection_id, item_id):
    return get_item_from_group(COLLECTION_TYPE, collection_id, item_id)


@current_app.route("/tags/<string:tag_id>/<string:item_id>")
def get_item_from_tag(tag_id, item_id):
    return get_item_from_group(TAG_TYPE, tag_id, item_id)


@current_app.route("/collections/<string:collection_id>/<string:item_id>", methods=["PUT", "POST"])
def add_item_to_collection(collection_id, item_id):
    return add_item_to_group(COLLECTION_TYPE, collection_id, item_id)


@current_app.route("/tags/<string:tag_id>/<string:item_id>", methods=["PUT", "POST"])
def add_item_to_tag(tag_id, item_id):
    return add_item_to_group(TAG_TYPE, tag_id, item_id)


@current_app.route("/collections/<string:collection_id>/<string:item_id>", methods=["DELETE"])
def remove_item_from_collection(collection_id, item_id):
    return remove_item_from_group(COLLECTION_TYPE, collection_id, item_id)


@current_app.route("/tags/<string:tag_id>/<string:item_id>", methods=["DELETE"])
def remove_item_from_tag(tag_id, item_id):
    return remove_item_from_group(TAG_TYPE, tag_id, item_id)
