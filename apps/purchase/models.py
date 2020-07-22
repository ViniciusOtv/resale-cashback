from datetime import datetime

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
)

from apps.db import db


class PurchaseModel(db.Document):
    '''
    Purchase
    '''
    meta = {'collection': 'purchase'}

    purchase_id = StringField()
    purchase_status = StringField(default='Em validação')
    created = DateTimeField(default=datetime.now)
    purchase_values = DecimalField(default=0)
    document_dealer = StringField(required=True,  unique=False)