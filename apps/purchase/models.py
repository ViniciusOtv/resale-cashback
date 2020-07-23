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
    UUIDField
)

from apps.db import db

def generateUUID():
    return str(uuid4())

class PurchaseModel(db.Document):
    '''
    Purchase
    '''
    meta = {'collection': 'purchase'}

    purchase_id = StringField()
    purchase_status = StringField()
    created = DateTimeField(default=datetime.now)
    purchase_values = DecimalField(default=0)
    document_dealer = StringField(required=True,  unique=False)
