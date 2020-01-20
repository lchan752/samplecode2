from samplecode.database import db
from samplecode.postcards.models import Postcard


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    address1 = db.Column(db.String(), nullable=False)
    address2 = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=False)
    code = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    postcards = db.relationship(Postcard, lazy='select', backref='customer')

    def __repr__(self):
        return f"Customer(id={self.id}, first_name={self.first_name} last_name={self.last_name})"
