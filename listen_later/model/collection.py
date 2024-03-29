import datetime as dt

from marshmallow import fields, post_load, Schema

from listen_later.constants import *


class Collection:
    def __init__(self, id, date_added, collection_name):
        self.id = id or ""
        self.date_added = date_added or dt.datetime.now()
        self.collection_name = collection_name

    def __repr__(self):
        return f"{COLLECTION_TYPE}({ID}={self.id!r}, {COLLECTION_NAME}={self.collection_name!r})".format(self=self)


class CollectionSchema(Schema):
    id = fields.String(missing="")
    date_added = fields.DateTime(missing=dt.datetime.now())
    collection_name = fields.String(required=True)

    @post_load
    def make_collection(self, data, **kwargs):
        return Collection(**data)


class CollectionUpdateSchema(Schema):
    collection_name = fields.String()
