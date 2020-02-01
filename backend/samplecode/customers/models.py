from samplecode.database import db
from samplecode.postcards.models import Postcard
from datetime import datetime


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    address1 = db.Column(db.String(), nullable=False)
    address2 = db.Column(db.String(), nullable=False, default='')
    city = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=False)
    code = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    postcards = db.relationship(Postcard, lazy='select', backref='customer')

    def __repr__(self):
        return f"Customer(id={self.id}, first_name={self.first_name} last_name={self.last_name})"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
