from environs import Env
from flask import Flask
from flask_migrate import Migrate
from samplecode.database import db

env = Env()
env.read_env()

DATABASE_URI = env.str("DATABASE_URI", "sqlite:////tmp/samplecode.db")
TEST_DATABASE_URI = env.str("TEST_DATABASE_URI", "sqlite:////tmp/samplecode_test.db")


def create_app(testing=False):
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI=TEST_DATABASE_URI if testing else DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        TESTING=testing,
    )

    # setup database connection
    db.init_app(app)
    Migrate(app, db)

    # importing the models to make sure they are known to Flask-Migrate
    from .customers.models import Customer
    from .postcards.models import Postcard

    # # register blueprints
    # app.register_blueprint(auth_bp)
    # app.register_blueprint(users_bp)
    # app.register_blueprint(ladders_bp)
    # app.register_blueprint(matches_bp)
    # app.register_blueprint(billing_bp)
    # app.add_url_rule("/", endpoint="auth.login")

    return app