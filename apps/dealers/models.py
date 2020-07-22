# Python
from datetime import datetime

# Third
from mongoengine import (
    BooleanField,
    DateTimeField,
    DictField,
    EmailField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    StringField,
    URLField
)

# Apps
from apps.db import db


class Roles(EmbeddedDocument):
    """
    Roles permissions
    """
    admin = BooleanField(default=False)
    
    
class DealerMixin(db.Document):
    """
    Default implementation for User fields
    """
    meta = {
        'abstract': True,
        'ordering': ['email']
    }

    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    cpf = StringField(required=True)
    roles = EmbeddedDocumentField(Roles, default=Roles)
    created = DateTimeField(default=datetime.now)
    # status = StringField(default=False)

    def is_active(self):
        return self.active

    def is_admin(self):
        return self.roles.admin
       
class User(DealerMixin):
    '''
    Users
    '''
    meta = {'collection': 'users'}

    full_name = StringField(required=True)
    cpf = StringField(required=True)
