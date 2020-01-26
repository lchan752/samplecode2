from marshmallow import Schema, missing
from marshmallow.fields import String, Integer, DateTime
from datetime import datetime
from samplecode.database import db
from .models import Customer
import pytz


def create_customer(validated_data):
    customer = Customer(created=datetime.now(pytz.utc), **validated_data)
    db.session.add(customer)
    db.session.commit()
    return customer


def update_customer(customer_id, validated_data):
    customer = db.session.query(Customer).filter(Customer.id == customer_id).first()
    for field, new_value in validated_data.items():
        if new_value != missing:
            setattr(customer, field, new_value)
    db.session.commit()
    return customer


class CustomerSchema(Schema):
    id = Integer(dump_only=True)
    created = DateTime(dump_only=True)
    first_name = String(required=True)
    last_name = String(required=True)
    address1 = String(required=True)
    address2 = String()
    city = String(required=True)
    state = String(required=True)
    code = String(required=True)
