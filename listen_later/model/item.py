import datetime as dt

from marshmallow import Schema, fields, post_load

class Item(object):
    def __init__(self, id, content_link, item_type_id, tag_ids, collection_ids, rating, listened):
        self.id = id
        self.date_added = dt.datetime.now()
        self.content_link = content_link
        self.item_type_id = item_type_id
        self.tag_ids = tag_ids
        self.collection_ids = collection_ids
        self.rating = rating
        self.listened = listened

    @post_load
    def make_item(self, data, **kwargs):
        return Item(**data)

    def __repr__(self):
        return '<Item(id={self.id!r})>'.format(self=self)
    
class ItemSchema(Schema):
    id = fields.Int()
    date_added = fields.DateTime()
    content_link = fields.String()
    item_type_id = fields.Int()
    tag_ids = fields.List(fields.Int())
    collection_ids = fields.List(fields.Int())
    rating = fields.Int()
    listened = fields.Bool()