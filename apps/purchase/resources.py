from flask import request
import json
# Third
from flask_restful import Resource
from bcrypt import gensalt, hashpw
from mongoengine.errors import NotUniqueError, ValidationError

from apps.responses import (
    resp_already_exists,
    resp_exception,
    resp_data_invalid,
    resp_ok
)
from apps.messages import MSG_NO_DATA, MSG_PASSWORD_WRONG, MSG_INVALID_DATA, MSG_PASSWORD_NOT_SAME, MSG_DOCUMENT_NULL
from apps.messages import MSG_RESOURCE_CREATED

from .models import PurchaseModel
from .schemas import PurchaseSchema
from .utils import check_approved_dealer, generate_guid


class Purchase(Resource):
    def post(self, *args, **kwargs):
        req_data = request.get_json() or None
        dict_purchase_data, errors, result = None, None, None
        password, confirm_password = None, None
        schema = PurchaseSchema()

        if req_data is None:
            return resp_data_invalid('Purchase', [], msg=MSG_NO_DATA)

        document = req_data.get('document_dealer', None)

        purchase_status = req_data.get('purchase_status', None)
        purchase_status = check_approved_dealer(document)

        if not purchase_status:
            purchase_status == 'Em Validação'

        dict_purchase_data = {
            "purchase_id": req_data.get('purchase_id', None),
            "purchase_status": req_data.get('purchase_status', None),
            "purchase_values": req_data.get('purchase_values', None),
            "document_dealer": req_data.get('document_dealer', None)
        }

        # if dict_purchase_data:
        #     return resp_data_invalid('Purchase', dict_purchase_data)

        # try:
        dict_purchase_data['purchase_id'] = generate_guid()
        dict_purchase_data['purchase_status'] = check_approved_dealer(document)
        model = PurchaseModel(**dict_purchase_data)
        model.save()

        if dict_purchase_data['purchase_id']:
            return resp_data_invalid('Purchase', dict_purchase_data['purchase_id'])

        # except ValidationError as e:
        #     return resp_exception('Purchase', msg=MSG_INVALID_DATA, description=e)

        # except Exception as e:
        #     return resp_exception('Purchase', description=e)

        schema = PurchaseSchema()
        result = schema.dump(model)

        return resp_ok(
            'Purchase', MSG_RESOURCE_CREATED.format('Purchase'), data=result,
        )
