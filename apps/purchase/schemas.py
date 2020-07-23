from marshmallow import Schema
from marshmallow.fields import Email, Str, Decimal, UUID
from apps.messages import MSG_FIELD_REQUIRED

class PurchaseSchema(Schema):
    purchase_id = Str()
    purchase_status = Str()
    purchase_values = Decimal(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    document_dealer = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})