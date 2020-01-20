import pytest
from samplecode import create_app
from samplecode.database import db as _db
from flask_migrate import upgrade as upgrade_database_schema
from sqlalchemy_utils.functions import drop_database


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