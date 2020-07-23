from os import getenv
from os.path import dirname, isfile, join

from uuid import uuid4

from mongoengine.errors import FieldDoesNotExist, DoesNotExist, MultipleObjectsReturned

# Apps
from apps.responses import resp_exception, resp_does_not_exist

# Local
from .models import PurchaseModel

_ENV_FILE = join(dirname(__file__), '.env')


if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)

def generateUUID(_id):
    
    if not _id:
        return str(uuid4())

def check_approved_dealer(document):

    status = " "

    if document == getenv('APPROVED_DEALER'): 

        status = "Aprovado"
        return status 

    status = "Em Validação"
    return status     

