from samplecode.postcards.helpers import (
    get_postcards,
    create_anniversary_postcards,
)
from datetime import datetime
from unittest.mock import patch, call


def test_get_postcards(db_session, postcard_factory):
    postcards = postcard_factory.create_batch(3)
    results = get_postcards()
    assert results == postcards

    postcard1 = postcards[0]
    customer1 = postcard1.customer
    results = get_postcards(customer_id=customer1.id)
    assert [postcard1] == results


def test_create_anniversary_postcards(db_session, postcard_factory, customer_factory):
    customer1 = customer_factory(created=datetime(2017, 4, 15))
    customer2 = customer_factory(created=datetime(2018, 3, 15))
    customer3 = customer_factory(created=datetime(2014, 4, 15))
    customer4 = customer_factory(created=datetime(2016, 3, 15))
    postcard_factory(customer=customer3, created=datetime(2015, 4, 15))
    postcard_factory(customer=customer3, created=datetime(2016, 4, 15))
    postcard_factory(customer=customer3, created=datetime(2017, 4, 15))
    postcard_factory(customer=customer4, created=datetime(2017, 3, 15))
    postcard_factory(customer=customer4, created=datetime(2018, 3, 15))
    with patch('samplecode.postcards.helpers.create_lob_postcard') as mock_create_lob_postcard:
        create_anniversary_postcards(current=datetime(2018, 4, 15))
    assert mock_create_lob_postcard.call_count == 2
    mock_create_lob_postcard.assert_has_calls([call(customer1), call(customer3)], any_order=True)
