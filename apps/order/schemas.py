from marshmallow import Schema
from marshmallow.fields import Email, Str, Decimal, UUID
from apps.messages import MSG_FIELD_REQUIRED

class OrderSchema(Schema):
    id = Str()
    order_status = Str()
    order_values = Decimal(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    cashback = Decimal()
    cashback_values = Decimal()
    cpf_dealer = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
