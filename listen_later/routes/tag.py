from flask import request
from listen_later.model.tag import TagSchema, TagUpdateSchema
from listen_later.model.constants import *
from listen_later.index import app, db

@app.route("/tags")
def get_tags():
    docs = db.collection(TAGS).stream()
    tags = []

    for doc in docs:
        tags.append(TagSchema().load(doc.to_dict()))

    return TagSchema(many=True).dump(tags)

@app.route("/tags/<string:pk>")
def get_tag(pk):
    doc_ref = db.collection(TAGS).document(pk)
    tag = doc_ref.get()

    if not tag.exists:
        return {"errors": f"Tag id={pk} could not be found"}, 404

    return tag.to_dict()

@app.route("/tags", methods=['POST'])
def add_tag():
    doc_ref = db.collection(TAGS).document()
    tag = TagSchema().load(request.get_json())

    tag.id = doc_ref.id
    doc_ref.set(TagSchema().dump(tag))

    return f'Added {tag} successfully', 201

@app.route("/tags/<int:pk>", methods=['PUT', 'POST'])
def update_tag(pk):
    doc_ref = db.collection(TAGS).document(pk)
    tag = doc_ref.get()

    if not tag.exists:
        return {"errors": f"Tag id={pk} could not be found"}, 404
    
    tag_update = TagUpdateSchema().load(request.get_json())

    if tag_update.get(TAG_NAME):
        doc_ref.update({TAG_NAME: tag_update.get(TAG_NAME)})

    return f'Updated tag id={pk} successfully with the following values:<br />{TagUpdateSchema().dump(tag_update)}', 200

@app.route("/tags/<int:pk>", methods=['DELETE'])
def delete_tag(pk):    
    doc_ref = db.collection("Tag").document(pk)
    tag = doc_ref.get()

    if not tag.exists:
        return {"errors": f"Tag id={pk} could not be found"}, 404

    # TODO: remove pk from each item's tag_ids

    doc_ref.delete()
    return f'Deleted tag id={pk} successfully', 200