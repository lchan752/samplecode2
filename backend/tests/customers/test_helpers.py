from samplecode.customers.helpers import (
    create_customer,
)
from samplecode.customers.models import (
    Customer
)


def test_create_customer(db_session):
    customer = create_customer(
        first_name='Jon',
        last_name='Snow',
        address1='123 Spooner Street',
        address2='',
        city='Quahog',
        state='Rhode Island',
        code='12345'
    )
    assert Customer.query.count() == 1


def test_create_customer_2(db_session):
    assert Customer.query.count() == 0
