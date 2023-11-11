import datetime as dt

from marshmallow import Schema, fields, post_load

class Collection:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.date_added = dt.datetime.now()

    def __repr__(self):
        return '<Collection(id={self.id!r},name={self.name!r})>'.format(self=self)

class CollectionSchema(Schema):
    id = fields.Int()
    date_added = fields.DateTime(dump_only=True)
    name = fields.String()

    @post_load
    def make_collection(self, data, **kwargs):
        return Collection(**data)