from sqlalchemy import func
from flask import current_app
from samplecode.database import db
from samplecode.customers.models import Customer
from .models import Postcard
from datetime import datetime
from dateutil.parser import parse as parse_datetime
from lob.error import LobError
import lob
import logging

logger = logging.getLogger(__name__)


def get_postcards(customer_id=None):
    qry = db.session.query(Postcard)
    if customer_id:
        qry = qry.filter(Postcard.customer_id == customer_id)
    return qry.all()


def create_anniversary_postcards(current=datetime.now, fail_on_first_error=False):
    customer_ids_to_send_postcards = set()

    threshold = datetime(current.year - 1, current.month, current.day)
    maxdate = func.max(Postcard.created).label('maxdate')
    qry = db.session.query(Postcard.customer_id, maxdate).group_by(Postcard.customer_id).having(maxdate <= threshold)
    for record in qry:
        customer_ids_to_send_postcards.add(record.customer_id)

    qry = db.session.query(Customer.id.label('customer_id')).outerjoin(Postcard).filter(Customer.created <= threshold, Postcard.id == None)
    for record in qry:
        customer_ids_to_send_postcards.add(record.customer_id)

    qry = db.session.query(Customer).filter(Customer.id.in_(customer_ids_to_send_postcards))
    for customer in qry:
        try:
            postcard = create_lob_postcard(customer)
            logger.info(f"Sent postcard to customer_id{customer.id}. lob id:{postcard.lob_id}")
        except LobError as e:
            logger.error(f"Failed to send postcard to customer_id:{customer.id}. lob error:{e}. lob status:{e.http_status}")


def create_lob_postcard(customer):
    lob.api_key = current_app.config['LOB_SECRET_KEY']
    resp = lob.Postcard.create(
        description='Demo Postcard job',
        to_address={
            'name': customer.full_name(),
            'address_line1': customer.address1,
            'address_line2': customer.address2,
            'address_city': customer.city,
            'address_state': customer.state,
            'address_zip': customer.code
        },
        from_address=current_app.config['LOB_FROM_ADDRESS'],
        front='<html style="padding: 1in; font-size: 50;">Front HTML for {{name}}</html>',
        back='<html style="padding: 1in; font-size: 20;">Back HTML for {{name}}</html>',
        merge_variables={
            'name': customer.full_name()
        }
    )
    lob_id = resp['id']
    lob_expected_delivery_date = parse_datetime(resp['expected_delivery_date'])
    lob_url = resp['url']
    created = datetime.utcnow()
    postcard = Postcard(
        customer=customer,
        created=created,
        lob_id=lob_id,
        lob_expected_delivery_date=lob_expected_delivery_date,
        lob_url=lob_url,
    )
    db.session.add(postcard)
    db.session.commit()
    return postcard
