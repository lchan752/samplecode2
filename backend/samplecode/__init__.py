from environs import Env
from flask import Flask
from flask_migrate import Migrate
from .database import db
from .customers.views import bp as customer_bp
from .postcards.views import bp as postcard_bp
from .postcards.helpers import create_anniversary_postcards

env = Env()
env.read_env()

DATABASE_URI = env.str("DATABASE_URI", "sqlite:////tmp/samplecode.db")
TEST_DATABASE_URI = env.str("TEST_DATABASE_URI", "sqlite:////tmp/samplecode_test.db")
LOB_SECRET_KEY = env("LOB_SECRET_KEY")
LOB_FROM_ADDRESS = env("LOB_FROM_ADDRESS", "adr_5aa11423698ade2f")


def create_app(testing=False):
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI=TEST_DATABASE_URI if testing else DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        LOB_SECRET_KEY=LOB_SECRET_KEY,
        LOB_FROM_ADDRESS=LOB_FROM_ADDRESS,
        TESTING=testing,
    )

    # setup database connection
    db.init_app(app)
    Migrate(app, db)

    # register blueprints
    app.register_blueprint(customer_bp)
    app.register_blueprint(postcard_bp)
    app.add_url_rule("/", endpoint="customers.customer-list")

    return app
