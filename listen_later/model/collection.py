import datetime as dt
from marshmallow import Schema, fields, post_load

class Collection:
    def __init__(self, id, date_added, name):
        self.id = id or ""
        self.date_added = date_added or dt.datetime.now()
        self.name = name

    def __repr__(self):
        return "Collection(id={self.id!r}, name={self.name!r})".format(self=self)

class CollectionSchema(Schema):
    id = fields.String(missing="")
    date_added = fields.DateTime(missing=dt.datetime.now())
    name = fields.String(required=True)

    @post_load
    def make_collection(self, data, **kwargs):
        return Collection(**data)

class CollectionUpdateSchema(Schema):
    name = fields.String()