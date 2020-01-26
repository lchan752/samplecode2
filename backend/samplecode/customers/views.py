from flask import (
    Blueprint,
    request,
)
from flask_restful import (
    Api,
    Resource,
)
from marshmallow.exceptions import ValidationError
from .schemas import (
    CustomerSchema,
    create_customer,
    update_customer,
)
from .helpers import (
    get_customer,
    get_customers,
    delete_customer,
)

bp = Blueprint('customers', __name__, url_prefix='/customers')
api = Api(bp)


@api.resource('/', endpoint='customer-list')
class CustomerList(Resource):
    def get(self):
        ser = CustomerSchema()
        customers = get_customers()
        response_data = ser.dump(customers, many=True)
        return response_data, 200

    def post(self):
        try:
            ser = CustomerSchema()
            validated_data = ser.load(request.form)
            customer = create_customer(validated_data=validated_data)
            response_data = ser.dump(customer)
            return response_data, 200
        except ValidationError as e:
            return e.messages, 400


@api.resource('/<int:customer_id>', endpoint='customer-detail')
class CustomerDetail(Resource):
    def get(self, customer_id):
        ser = CustomerSchema()
        customer = get_customer(customer_id=customer_id)
        response_data = ser.dump(customer)
        return response_data, 200

    def post(self, customer_id):
        try:
            ser = CustomerSchema(partial=True)
            validated_data = ser.load(request.form)
            customer = update_customer(customer_id=customer_id, validated_data=validated_data)
            response_data = ser.dump(customer)
            return response_data, 200
        except ValidationError as e:
            return e.messages, 400

    def delete(self, customer_id):
        delete_customer(customer_id=customer_id)
        return {}, 204
