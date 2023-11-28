import datetime as dt

from marshmallow import Schema, fields, post_load

class Tag(object):
    def __init__(self, name):
        # TODO: implement ids
        self.id = 0
        self.date_added = dt.datetime.now()

        self.name = name

    def __repr__(self):
        return '<Tag(id={self.id!r},name={self.name})>'.format(self=self)

class TagSchema(Schema):
    id = fields.Int(dump_only=True)
    date_added = fields.DateTime(dump_only=True)
    name = fields.String()

    @post_load
    def make_item(self, data, **kwargs):
        return Tag(**data)
    
class TagUpdateSchema(Schema):
    name = fields.String()