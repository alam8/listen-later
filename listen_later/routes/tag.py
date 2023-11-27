from flask import request
from listen_later.model.tag import TagSchema
from listen_later.index import app

tags = []

@app.route("/tags")
def get_tags():
    return TagSchema(many=True).dump(tags)

@app.route("/tags/<int:pk>")
def get_tag(pk):
    # TODO: query tag w/ ORM
    tag = None # Tag.get(Tag.id == pk)
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
    tag = None # Tag.get(Tag.id == pk)

    # TODO: change update logic
    try:
        new_name = request.get_json()["name"]
    except:
        return {"errors": "Name not provided"}, 400

    if not tag:
        return {"errors": f"Tag id={pk} could not be found"}, 404

    update_name = tag.update(name=new_name)
    update_name.execute()
    return TagSchema().dump(tag)

@app.route("/tags/<int:pk>", methods=['DELETE'])
def delete_tag(pk):
    # TODO: query tag w/ ORM
    tag = None # Tag.get(tag.id == pk)

    if not tag:
        return {"errors": f"Tag id={pk} could not be found"}, 404

    # TODO: remove pk from each item's tag_ids

    tags.remove(tag)
    return f'Deleted {tag} successfully', 200