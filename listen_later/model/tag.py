import datetime as dt

from marshmallow import fields, post_load, Schema

from listen_later.constants import *

class Tag(object):
    def __init__(self, id, date_added, name):
        self.id = id or ""
        self.date_added = date_added or dt.datetime.now()
        self.name = name

    def __repr__(self):
        return f"{TAG_TYPE}({ID}={self.id!r},name={self.name})".format(self=self)

class TagSchema(Schema):
    id = fields.String(missing="")
    date_added = fields.DateTime(missing=dt.datetime.now())
    name = fields.String(required=True)

    @post_load
    def make_item(self, data, **kwargs):
        return Tag(**data)

class TagUpdateSchema(Schema):
    name = fields.String()