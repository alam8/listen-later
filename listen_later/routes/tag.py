from flask import request

from listen_later.constants import *
from listen_later.index import flask_app, user_ref
from listen_later.model.tag import TagSchema, TagUpdateSchema
from listen_later.routes import responses

user_tags_ref = user_ref.collection(TAGS)


@flask_app.route("/tags")
def get_tags():
    tags_ref = user_tags_ref.collection(TAGS).stream()
    tags = []

    for tag_ref in tags_ref:
        tags.append(TagSchema().load(tag_ref.to_dict()))

    return TagSchema(many=True).dump(tags)


def get_tag_ref(tag_id=None):
    return user_tags_ref.document(tag_id)


@flask_app.route("/tags/<string:tag_id>")
def get_tag(tag_id):
    tag_ref = get_tag_ref(tag_id)
    tag = tag_ref.get()

    if not tag.exists:
        return responses.not_found_error(TAG_TYPE, tag_id)

    return tag.to_dict()


@flask_app.route("/tags", methods=["POST"])
def create_tag():
    tag_ref = get_tag_ref()
    tag = TagSchema().load(request.get_json())

    tag.id = tag_ref.id
    tag_ref.set(TagSchema().dump(tag))

    return responses.obj_created(tag)


@flask_app.route("/tags/<int:tag_id>", methods=["PUT", "POST"])
def update_tag(tag_id):
    tag_ref = get_tag_ref(tag_id)
    tag = tag_ref.get()

    if not tag.exists:
        return responses.not_found_error(TAG_TYPE, tag_id)

    tag_update = TagUpdateSchema().load(request.get_json())

    if tag_update.get(TAG_NAME):
        tag_ref.update({TAG_NAME: tag_update.get(TAG_NAME)})

    return responses.obj_updated(TAG_TYPE, tag_id, TagUpdateSchema().dump(tag_update))


@flask_app.route("/tags/<int:tag_id>", methods=["DELETE"])
def delete_tag(tag_id):
    tag_ref = get_tag_ref(tag_id)
    tag = tag_ref.get()

    if not tag.exists:
        return responses.not_found_error(TAG_TYPE, tag_id)

    # TODO: remove only this tag from each instance of every item in
    #       this tag's sub-fbc of tags

    tag_ref.delete()
    return responses.obj_deleted(TAG_TYPE, tag_id)
