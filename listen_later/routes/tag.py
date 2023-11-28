from flask import request
from listen_later.model.tag import TagSchema, TagUpdateSchema
from listen_later.index import app

tags = []

@app.route("/tags")
def get_tags():
    return TagSchema(many=True).dump(tags)

@app.route("/tags/<int:pk>")
def get_tag(pk):
    # TODO: query tag w/ ORM
    tag = None # db.collection("Tag").document(pk)
    if not tag:
        return {"errors": "Tag could not be found"}, 404
    return TagSchema.dump(tag)

@app.route("/tags", methods=['POST'])
def add_tag():
    tag = TagSchema().load(request.get_json())
    tags.append(tag)
    return '', 204

@app.route("/tags/<int:pk>", methods=['PUT', 'POST'])
def update_tag(pk):
    # TODO: query tag w/ ORM
    tag = None # db.collection("Tag").document(pk)

    if not tag:
        return {"errors": f"Tag id={pk} could not be found"}, 404
    
    tag_update = TagUpdateSchema().load(request.get_json())

    if tag_update.name:
        tag.update({"name": tag_update.name})

    return TagUpdateSchema().dump(tag_update)

@app.route("/tags/<int:pk>", methods=['DELETE'])
def delete_tag(pk):
    # TODO: query tag w/ ORM
    tag = None # db.collection("Tag").document(pk)

    if not tag:
        return {"errors": f"Tag id={pk} could not be found"}, 404

    # TODO: remove pk from each item's tag_ids

    tags.remove(tag)
    return f'Deleted {tag} successfully', 200