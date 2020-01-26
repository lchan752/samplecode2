from samplecode.database import db
from .models import Customer


def delete_customer(customer_id: int):
    db.session.query(Customer).filter(Customer.id == customer_id).delete()
    db.session.commit()


def get_customer(customer_id: int):
    return db.session.query(Customer).filter(Customer.id == customer_id).first()


def get_customers():
    return db.session.query(Customer)
