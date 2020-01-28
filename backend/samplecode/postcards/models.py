from samplecode.database import db
from datetime import datetime


class Postcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Postcard(id={self.id}, customer_id={self.customer_id})"
