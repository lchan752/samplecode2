from samplecode.postcards.helpers import (
    get_postcards,
)


def test_get_postcards(db_session, postcard_factory):
    postcards = postcard_factory.create_batch(3)
    results = get_postcards()
    assert results == postcards

    postcard1 = postcards[0]
    customer1 = postcard1.customer
    results = get_postcards(customer_id=customer1.id)
    assert [postcard1] == results

