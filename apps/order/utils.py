from os import getenv
from os.path import dirname, isfile, join

from uuid import uuid4

from mongoengine.errors import FieldDoesNotExist, DoesNotExist, MultipleObjectsReturned

# Apps
from apps.responses import resp_exception, resp_does_not_exist

# Local
from .models import OrderModel

_ENV_FILE = join(dirname(__file__), '.env')

if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)


def generateUUID(_id):

    if not _id:
        return str(uuid4())


def cashback_percentage(order_value):

    if order_value <= 1000:
        percentage = 0.1
        return percentage

    elif order_value > 1000 and order_value <= 1500:
        percentage = 0.15
        return percentage

    else:
        percentage = 0.15
        return percentage


def calculate_value_cashback(value, percentage):
    cashback_value = value * percentage 
    return cashback_value


def check_approved_dealer(document):

    status = ""

    if document == getenv('APPROVED_DEALER'):

        status = "Aprovado"
        return status

    status = "Em Validação"
    return status


def get_order_by_id(order_id: str):
    try:
        return OrderModel.objects.get(id=order_id)

    except DoesNotExist:
        return resp_does_not_exist('Order', 'Pedido')

    except FieldDoesNotExist as e:
        return resp_exception('Order', description=e.__str__())

    except Exception as e:
        return resp_exception('Order', description=e.__str__())
