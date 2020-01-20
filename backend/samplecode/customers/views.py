from flask import (
    Blueprint,
)
from flask_restful import (
    Api,
    Resource,
)

bp = Blueprint('customers', __name__, url_prefix='/customers')
api = Api(bp)


@api.resource('/', endpoint='customer-list')
class CustomerList(Resource):
    def get(self):
        return [{'id': 1, 'name': 'Jon Snow'}, {'id': 2, 'name': 'Tyrion Lannister'}]


@api.resource('/<int:customer_id>', endpoint='customer-detail')
class CustomerDetail(Resource):
    def get(self, customer_id):
        return {'id': 1, 'name': 'Jon Snow'}
