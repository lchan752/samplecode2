from samplecode.database import db
from .models import Customer
from datetime import datetime
import pytz


def create_customer(first_name: str, last_name: str, address1: str, address2: str, city: str, state: str, code: str):
    customer = Customer(
        first_name=first_name,
        last_name=last_name,
        address1=address1,
        address2=address2,
        city=city,
        state=state,
        code=code,
        created=datetime.now(pytz.utc)
    )
    db.session.add(customer)
    db.session.commit()
    return customer


def edit_customer(customer_id: int):
    pass


def delete_customer(customer_id: int):
    pass


def get_customer(customer_id: int):
    pass


def get_customers():
    pass
