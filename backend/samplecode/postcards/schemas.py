from marshmallow import Schema
from marshmallow.fields import Integer, DateTime


class PostcardSchema(Schema):
    id = Integer(dump_only=True)
    customer_id = Integer(dump_only=True)
    created = DateTime(dump_only=True)
