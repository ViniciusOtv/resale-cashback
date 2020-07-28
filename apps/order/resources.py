from flask import request
import json
import decimal
# Third
from flask_restful import Resource
from bcrypt import gensalt, hashpw
from mongoengine.errors import NotUniqueError, ValidationError, FieldDoesNotExist

from flask_jwt_extended import get_jwt_identity, jwt_required

from apps.responses import (
    resp_already_exists,
    resp_exception,
    resp_data_invalid,
    resp_ok
)
from apps.messages import MSG_NO_DATA, MSG_INVALID_DATA, MSG_DOCUMENT_NULL
from apps.messages import MSG_RESOURCE_CREATED, MSG_RESOURCE_FETCHED_PAGINATED

from .models import OrderModel
from .schemas import OrderSchema
from .utils import check_approved_dealer, generateUUID, cashback_percentage, calculate_value_cashback


class order(Resource):
    def post(self, *args, **kwargs):
        req_data = request.get_json() or None
        dict_order_data, errors, result = None, None, None
        password, confirm_password = None, None
        schema = OrderSchema(many=True)

        if req_data is None:
            return resp_data_invalid('order', [], msg=MSG_NO_DATA)

        document = req_data.get('cpf_dealer', None)
        value = req_data.get('order_values', None)

        dict_order_data = {
            "order_values": req_data.get('order_values', None),
            "cpf_dealer": req_data.get('cpf_dealer', None)
        }

        if errors:
            return resp_data_invalid('order', errors)

        # try:
        dict_order_data['order_code'] = generateUUID(None)
        dict_order_data['order_status'] = check_approved_dealer(document)
        dict_order_data['cashback'] = cashback_percentage(value)
        dict_order_data['cashback_values'] = calculate_value_cashback(value, dict_order_data['cashback'])
        model = OrderModel(**dict_order_data)
        model.save()

        # except ValidationError as e:
        #     return resp_exception('order', msg=MSG_INVALID_DATA, description=e)

        # except Exception as e:
        #     return resp_exception('order', description=e)

        schema = OrderSchema()
        result = schema.dump(model)

        return resp_ok(
            'order', MSG_RESOURCE_CREATED.format('Order'), data=result,
        )

