from flask import url_for
from tests.factories import CustomerFactoryBase
from samplecode.customers.models import Customer
from funcy import project
import factory


def test_create_customer(client, db_session):
    data = factory.build(dict, FACTORY_CLASS=CustomerFactoryBase)
    resp = client.post(url_for('customers.customer-list'), data=data)
    assert resp.status_code == 200, resp.json
    qry = [getattr(Customer, field_name).like(field_value) for field_name, field_value in data.items()]
    assert db_session.query(Customer).filter(*qry).count() == 1


def test_update_customer(client, db_session, customer_factory):
    initial_data = factory.build(dict, FACTORY_CLASS=CustomerFactoryBase)
    customer = customer_factory(**initial_data)
    db_session.commit()
    updated_data = project(factory.build(dict, FACTORY_CLASS=CustomerFactoryBase), ['first_name', 'last_name'])
    resp = client.post(url_for('customers.customer-detail', customer_id=customer.id), data=updated_data)
    assert resp.status_code == 200, resp.json
    filter_data = {**initial_data, **updated_data}
    qry = [getattr(Customer, field_name).like(field_value) for field_name, field_value in filter_data.items()]
    assert db_session.query(Customer).filter(*qry).count() == 1


def test_delete_customer(client, db_session, customer_factory):
    customer = customer_factory()
    db_session.commit()
    resp = client.delete(url_for('customers.customer-detail', customer_id=customer.id))
    assert resp.status_code == 204, resp.json
    assert db_session.query(Customer).count() == 0


def test_get_customer(client, db_session, customer_factory):
    customer = customer_factory()
    db_session.commit()
    resp = client.get(url_for('customers.customer-detail', customer_id=customer.id))
    assert resp.status_code == 200, resp.json
    assert resp.json['id'] == customer.id


def test_list_customers(client, db_session, customer_factory):
    customers = customer_factory.create_batch(3)
    db_session.commit()
    resp = client.get(url_for('customers.customer-list'))
    assert resp.status_code == 200, resp.json
    assert set([x['id'] for x in resp.json]) == set([customer.id for customer in customers])
