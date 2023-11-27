from flask import request
from listen_later.model.item import ItemSchema
from listen_later.model.item_type import ItemType
from listen_later.index import app

items = []

@app.route("/items")
def get_items():
    return ItemSchema(many=True).dump(items)

@app.route("/items/<int:pk>")
def get_item(pk):
    # TODO: query item w/ ORM
    item = None # Item.get(Item.id == pk)
    if not item:
        return {"errors": "Item could not be found"}, 404
    return ItemSchema.dump(item)

@app.route("/items", methods=['POST'])
def add_item():
    item = ItemSchema().load(request.get_json())
    items.append(item)
    return f'Added {item} successfully', 201

@app.route("/items/<int:pk>", methods=['PUT', 'POST'])
def update_item(pk):
    # TODO: query item w/ ORM
    item = None # Item.get(Item.id == pk)

    # TODO: change update logic
    try:
        new_link = request.get_json()["content_link"]
    except:
        return {"errors": "Link not provided"}, 400

    if not item:
        return {"errors": f"Item id={pk} could not be found"}, 404

    update_link = item.update(content_link=new_link)
    update_link.execute()
    return ItemSchema().dump(item)

@app.route("/items/<int:pk>", methods=['DELETE'])
def delete_item(pk):
    # TODO: query item w/ ORM
    item = None # Item.get(item.id == pk)

    if not item:
        return {"errors": f"Item id={pk} could not be found"}, 404

    items.remove(item)
    return f'Deleted {item} successfully', 200