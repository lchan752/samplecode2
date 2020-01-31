from sqlalchemy import func
from flask import current_app
from samplecode.database import db
from samplecode.customers.models import Customer
from .models import Postcard
from datetime import datetime
from dateutil.parser import parse as parse_datetime
from lob.error import LobError
import lob


def get_postcards(customer_id=None):
    qry = db.session.query(Postcard)
    if customer_id:
        qry = qry.filter(Postcard.customer_id == customer_id)
    return qry.all()


def create_anniversary_postcards(current=datetime.now()):
    logger = current_app.logger
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
    success, failure = 0, 0
    for customer in qry:
        try:
            postcard = create_lob_postcard(customer)
            logger.info(f"Sent postcard to customer_id{customer.id}. lob id:{postcard.lob_id}")
            success += 1
        except LobError as e:
            logger.error(f"Failed to send postcard to customer_id:{customer.id}. lob error:{e}. lob status:{e.http_status}")
            failure += 1
    logger.info(f"Done sending anniversary postcards. Success:{success} Failure:{failure}")


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


def create_dummy_postcards():
    customer1 = Customer(
        first_name='Monkey',
        last_name='Kong',
        address1='123 Sesame Street',
        address2='',
        city='New York',
        state='NY',
        code='12345',
    )
    customer2 = Customer(
        first_name='Donkey',
        last_name='Kong',
        address1='223 Sesame Street',
        address2='',
        city='New York',
        state='NY',
        code='12345',
    )
    customer3 = Customer(
        first_name='Mickey',
        last_name='Kong',
        address1='323 Sesame Street',
        address2='',
        city='New York',
        state='NY',
        code='12345',
    )
    customer1_postcards1 = Postcard(
        customer=customer1,
        lob_id="customer1_postcards1",
        lob_expected_delivery_date=datetime(2018, 4, 15),
        lob_url="http://google.com",
    )
    customer1_postcards2 = Postcard(
        customer=customer1,
        lob_id="customer1_postcards2",
        lob_expected_delivery_date=datetime(2017, 4, 15),
        lob_url="http://google.com",
    )
    customer2_postcards1 = Postcard(
        customer=customer2,
        lob_id="customer2_postcards1",
        lob_expected_delivery_date=datetime(2018, 4, 15),
        lob_url="http://google.com",
    )
    customer2_postcards2 = Postcard(
        customer=customer2,
        lob_id="customer2_postcards2",
        lob_expected_delivery_date=datetime(2017, 4, 15),
        lob_url="http://google.com",
    )
    db.session.add_all([
        customer1, customer2, customer3,
        customer1_postcards1, customer1_postcards2,
        customer2_postcards1, customer2_postcards2,
    ])
    db.session.commit()
