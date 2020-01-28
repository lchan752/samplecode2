from samplecode.database import db
from .models import Postcard


def get_postcards(customer_id=None):
    qry = db.session.query(Postcard)
    if customer_id:
        qry = qry.filter(Postcard.customer_id == customer_id)
    return qry.all()


def create_anniversary_postcards():
    pass
