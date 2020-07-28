from datetime import datetime
from uuid import uuid4

from mongoengine import (
    BooleanField,
    DateTimeField,
    DictField,
    EmailField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    StringField,
    URLField,
    DecimalField,
    UUIDField, 
)

from apps.db import db

class OrderModel(db.Document):
    '''
    Order
    '''
    meta = {'collection': 'order', 'strict': False}

    order_code = StringField()
    order_status = StringField()
    created = DateTimeField(default=datetime.now)
    order_values = DecimalField(default=0)
    cashback = DecimalField(default=0)
    cashback_values = DecimalField(default=0)
    cpf_dealer = StringField(required=True, unique=False)
