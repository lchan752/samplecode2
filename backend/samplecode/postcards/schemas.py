from marshmallow import Schema
from marshmallow.fields import Integer, DateTime, String, URL


class PostcardSchema(Schema):
    id = Integer(dump_only=True)
    customer_id = Integer(dump_only=True)
    created = DateTime(dump_only=True)

    lob_id = String(dump_only=True)
    lob_expected_delivery_date = DateTime(dump_only=True)
    lob_url = URL(dump_only=True)
