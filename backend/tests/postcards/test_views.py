from flask import url_for


def test_list_postcards(client, db_session, postcard_factory):
    postcards = postcard_factory.create_batch(3)
    db_session.commit()
    url = url_for('postcards.postcard-list')
    resp = client.get(url)
    assert resp.status_code == 200, resp.json
    assert set([x['id'] for x in resp.json]) == set([postcard.id for postcard in postcards])

    postcard1 = postcards[0]
    customer1 = postcard1.customer
    resp = client.get(url + f'?customer_id={customer1.id}')
    assert resp.status_code == 200, resp.json
    assert set([x['id'] for x in resp.json]) == set([postcard1.id])
