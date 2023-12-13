from listen_later.model.constants import *
from listen_later.index import app, user_ref

user_collections_ref = user_ref.collection(COLLECTIONS)
user_tags_ref = user_ref.collection(TAGS)

@app.route("/collections/<string:collection_pk>/<string:item_pk>", methods=['PUT', 'POST'])
def add_item_to_collection():
    pass

@app.route("/collections/<string:collection_pk>/<string:item_pk>", methods=['DELETE'])
def remove_item_from_collection():
    pass

@app.route("/tags/<string:tag_pk>/<string:item_pk>", methods=['PUT', 'POST'])
def add_item_to_tag():
    pass

@app.route("/tags/<string:tag_pk>/<string:item_pk>", methods=['DELETE'])
def remove_item_from_tag():
    pass