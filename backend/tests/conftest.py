from samplecode import create_app
from samplecode.database import db as _db
from flask_migrate import upgrade as upgrade_database_schema
from sqlalchemy_utils.functions import drop_database
from samplecode.customers.models import Customer
from samplecode.postcards.models import Postcard
from tests.factories import CustomerFactoryBase

from datetime import datetime
import pytest
import factory
import pytz


@pytest.fixture(scope='session')
def app():
    app = create_app(testing=True)
    return app


@pytest.fixture(scope='session')
def db(app, request):
    with app.app_context():
        upgrade_database_schema()

    @request.addfinalizer
    def teardown():
        with app.app_context():
            drop_database(_db.engine.url)

    return _db


@pytest.fixture(scope='function')
def db_session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='function')
def customer_factory(db_session):
    class CustomerFactory(CustomerFactoryBase, factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Customer
            sqlalchemy_session = db_session

        created = datetime.now(pytz.utc)

    return CustomerFactory


@pytest.fixture(scope='function')
def postcard_factory(db_session, customer_factory):
    class PostcardFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Postcard
            sqlalchemy_session = db_session

        customer = factory.SubFactory(customer_factory)
    return PostcardFactory
