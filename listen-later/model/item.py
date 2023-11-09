import datetime as dt

from marshmallow import Schema, fields

class Item(object):
    def __init__(self):
        pass

    def __repr__(self):
        return '<Transaction(name={self.description!r})>'.format(self=self)
    
class ItemSchema(Schema):
    pass