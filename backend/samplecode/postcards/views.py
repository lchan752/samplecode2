from flask import (
    Blueprint,
    request,
)
from flask_restful import (
    Api,
    Resource,
)
from .schemas import PostcardSchema
from .helpers import get_postcards

bp = Blueprint('postcards', __name__, url_prefix='/postcards')
api = Api(bp)


@api.resource('/', endpoint='postcard-list')
class PostcardList(Resource):
    def get(self):
        customer_id = request.args.get('customer_id', None)
        ser = PostcardSchema()
        postcards = get_postcards(customer_id=customer_id)
        response_data = ser.dump(postcards, many=True)
        return response_data, 200
