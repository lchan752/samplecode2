from samplecode.database import db


class Postcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    def __repr__(self):
        return f"Postcard(id={self.id}, customer_id={self.customer_id})"
