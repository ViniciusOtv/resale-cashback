from os import getenv
from os.path import dirname, isfile, join

import uuid

from mongoengine.errors import FieldDoesNotExist, DoesNotExist, MultipleObjectsReturned

# Apps
from apps.responses import resp_exception, resp_does_not_exist

# Local
from .models import PurchaseModel

_ENV_FILE = join(dirname(__file__), '.env')


if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)

def generate_guid():
    
    purchase_id == uuid.uuid4()
    return purchase_id

def check_approved_dealer(document):
    status = ''
    if not document == getenv('APPROVED_DEALER'): 
        return status == 'Aprovado'
      
    return status == 'Em Validação'    

