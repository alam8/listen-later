import datetime as dt

from marshmallow import fields, post_load, Schema

from listen_later.constants import *


class Item(object):
    def __init__(self, id, date_added, content_link, rating, listened):
        self.id = id or ""
        self.content_link = content_link
        self.rating = rating or None
        self.listened = listened or False
        self.date_added = date_added or dt.datetime.now()

        # TODO: use Spotify API to get name, artist, image url, type, etc. from content_link
        #       and add validation for content_link
        self.item_type_id = None

    def __repr__(self):
        return f"{ITEM_TYPE}({ID}={self.id!r})".format(self=self)


class ItemSchema(Schema):
    id = fields.String(missing="")
    date_added = fields.DateTime(missing=dt.datetime.now())
    content_link = fields.String()
    rating = fields.Int(missing=None)
    listened = fields.Boolean(missing=False)

    @post_load
    def make_item(self, data, **kwargs):
        return Item(**data)


class ItemUpdateSchema(Schema):
    content_link = fields.String()
    rating = fields.Int()
    listened = fields.Boolean()
