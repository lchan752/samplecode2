from samplecode.customers.helpers import (
    get_customer,
    get_customers,
    delete_customer,
)
from samplecode.customers.models import Customer


def test_get_customer(db_session, customer_factory):
    expected1 = customer_factory()
    expected2 = customer_factory()
    db_session.commit()
    actual1 = get_customer(customer_id=expected1.id)
    actual2 = get_customer(customer_id=expected2.id)
    assert actual1 == expected1
    assert actual2 == expected2


def test_get_customers(db_session, customer_factory):
    expected = customer_factory.create_batch(3)
    db_session.commit()
    actual = get_customers()
    assert list(actual) == expected


def test_delete_customer(db_session, customer_factory):
    customer = customer_factory()
    db_session.commit()
    delete_customer(customer_id=customer.id)
    assert db_session.query(Customer).filter(Customer.id == customer.id).count() == 0
