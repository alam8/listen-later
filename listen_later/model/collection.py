import datetime as dt

from marshmallow import Schema, fields, post_load

class Collection(object):
    def __init__(self, id, name ):
        self.id = id
        self.name = name
        self.date_added = dt.datetime.now()

    def __repr__(self):
        return '<Collection(id={self.id!r},name={self.name!r})>'.format(self=self)

class CollectionSchema(Schema):
    id = fields.Int()
    name = fields.String()
    date_added = fields.DateTime()

    @post_load
    def make_collection(self, data, **kwargs):
        return Collection(**data)