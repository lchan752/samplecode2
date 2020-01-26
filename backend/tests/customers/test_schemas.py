from samplecode.customers.schemas import (
    CustomerSchema,
    create_customer,
    update_customer,
)
from samplecode.customers.models import (
    Customer
)
from tests.factories import (
    CustomerFactoryBase,
)
from funcy import (
    project,
    rpartial,
)
from marshmallow.exceptions import ValidationError
import factory
import pytest


def test_create_customer(db_session, customer_factory):
    ser = CustomerSchema()
    data = factory.build(dict, FACTORY_CLASS=CustomerFactoryBase)
    validated_data = ser.load(data)
    customer = create_customer(validated_data=validated_data)
    qry = [getattr(Customer, field_name).like(field_value) for field_name, field_value in data.items()]
    assert db_session.query(Customer).filter(*qry).first() == customer


@pytest.mark.parametrize("update_fields", [
    ['first_name', 'last_name'],
    ['address1', 'city', 'state', 'code'],
])
def test_update_customer(update_fields, db_session, customer_factory):
    initial_data = factory.build(dict, FACTORY_CLASS=CustomerFactoryBase)
    customer = customer_factory(**initial_data)
    db_session.commit()
    updated_data = project(factory.build(dict, FACTORY_CLASS=CustomerFactoryBase), update_fields)
    ser = CustomerSchema(partial=True)
    validated_data = ser.load(updated_data)
    updated_customer = update_customer(customer_id=customer.id, validated_data=validated_data)
    filter_data = {**initial_data, **updated_data}
    qry = [getattr(Customer, field_name).like(field_value) for field_name, field_value in filter_data.items()]
    assert db_session.query(Customer).filter(*qry).first() == updated_customer


@pytest.mark.parametrize("modifier, error_field, error_message", [
    (rpartial(dict.pop, 'first_name'), 'first_name', 'Missing data for required field.'),
    (rpartial(dict.update, {'first_name': None}), 'first_name', 'Field may not be null.'),
    (rpartial(dict.pop, 'last_name'), 'last_name', 'Missing data for required field.'),
    (rpartial(dict.update, {'last_name': None}), 'last_name', 'Field may not be null.'),
    (rpartial(dict.pop, 'address1'), 'address1', 'Missing data for required field.'),
    (rpartial(dict.update, {'address1': None}), 'address1', 'Field may not be null.'),
])
def test_customer_schema_validation(modifier, error_field, error_message):
    ser = CustomerSchema()
    data = factory.build(dict, FACTORY_CLASS=CustomerFactoryBase)
    with pytest.raises(ValidationError) as e:
        modifier(data)
        ser.load(data)
    assert error_message in e.value.messages[error_field], e.value.messages
