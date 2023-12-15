from flask import request
from listen_later.model.tag import TagSchema, TagUpdateSchema
from listen_later.model.constants import *
from listen_later.index import app, user_ref, not_found_error

user_tags_ref = user_ref.collection(TAGS)

@app.route("/tags")
def get_tags():
    tags_ref = user_tags_ref.collection(TAGS).stream()
    tags = []

    for tag_ref in tags_ref:
        tags.append(TagSchema().load(tag_ref.to_dict()))

    return TagSchema(many=True).dump(tags)

def get_tag_ref(pk=None):
    return user_tags_ref.document(pk)

@app.route("/tags/<string:pk>")
def get_tag(pk):
    tag_ref = get_tag_ref(pk)
    tag = tag_ref.get()

    if not tag.exists:
        return not_found_error(TAG_TYPE, pk)

    return tag.to_dict()

@app.route("/tags", methods=['POST'])
def create_tag():
    tag_ref = get_tag_ref()
    tag = TagSchema().load(request.get_json())

    tag.id = tag_ref.id
    tag_ref.set(TagSchema().dump(tag))

    return f'Created {tag} successfully', 201

@app.route("/tags/<int:pk>", methods=['PUT', 'POST'])
def update_tag(pk):
    tag_ref = get_tag_ref(pk)
    tag = tag_ref.get()

    if not tag.exists:
        return not_found_error(TAG_TYPE, pk)

    tag_update = TagUpdateSchema().load(request.get_json())

    if tag_update.get(TAG_NAME):
        tag_ref.update({TAG_NAME: tag_update.get(TAG_NAME)})

    return f'Updated tag id={pk} successfully with the following values:<br />{TagUpdateSchema().dump(tag_update)}', 200

@app.route("/tags/<int:pk>", methods=['DELETE'])
def delete_tag(pk):
    tag_ref = get_tag_ref(pk)
    tag = tag_ref.get()

    if not tag.exists:
        return not_found_error(TAG_TYPE, pk)

    # TODO: remove only this tag from each instance of every item in
    #       this tag's sub-fbc of tags

    tag_ref.delete()
    return f'Deleted tag id={pk} successfully', 200