import datetime as dt

from marshmallow import Schema, fields, post_load

class Tag(object):
    def __init__(self, id, date_added, name):
        self.id = id or ""
        self.date_added = date_added or dt.datetime.now()
        self.name = name

    def __repr__(self):
        return "<Tag(id={self.id!r},name={self.name})>".format(self=self)

class TagSchema(Schema):
    id = fields.String(missing="")
    date_added = fields.DateTime(missing=dt.datetime.now())
    name = fields.String(required=True)

    @post_load
    def make_item(self, data, **kwargs):
        return Tag(**data)
    
class TagUpdateSchema(Schema):
    name = fields.String()