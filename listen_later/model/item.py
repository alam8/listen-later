import datetime as dt

from marshmallow import Schema, fields, post_load
from listen_later.model.constants import ALL_COLLECTION_ID

class Item(object):
    def __init__(self, content_link, tag_ids, collection_ids, rating, listened):
        # TODO: implement IDs
        self.id = 0
        self.date_added = dt.datetime.now()
        self.content_link = content_link
        # TODO: use SpotifyAPI to get type
        self.item_type_id = None

        self.tag_ids = tag_ids or []
        self.collection_ids = [ALL_COLLECTION_ID] + collection_ids
        self.rating = rating or None
        self.listened = listened or False

    def __repr__(self):
        return '<Item(id={self.id!r})>'.format(self=self)

class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    date_added = fields.DateTime(dump_only=True)
    content_link = fields.String()
    tag_ids = fields.List(fields.Int(), missing=[])
    collection_ids = fields.List(fields.Int(), missing=[])
    rating = fields.Int(missing=None)
    listened = fields.Boolean(missing=False)

    @post_load
    def make_item(self, data, **kwargs):
        return Item(**data)