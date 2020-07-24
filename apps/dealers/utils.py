# -*- coding: utf-8

# Third

from mongoengine.errors import FieldDoesNotExist, DoesNotExist, MultipleObjectsReturned

# Apps
from apps.responses import resp_exception, resp_does_not_exist

# Local
from .models import User


def check_password_in_signup(password: str, confirm_password: str):

    if not password:
        return False

    if not confirm_password:
        return False

    return True

def check_password_is_same(password: str, confirm_password: str):

    if not password == confirm_password:
        return False

    return True 

def check_document(document):

    if not document: 
        return False
        
    return True           

def get_user_by_id(user_id: str):
    try:
        # buscamos todos os usuários da base utilizando o paginate
        return User.objects.get(id=user_id)

    except DoesNotExist:
        return resp_does_not_exist('Users', 'Usuário')

    except FieldDoesNotExist as e:
        return resp_exception('Users', description=e.__str__())

    except Exception as e:
        return resp_exception('Users', description=e.__str__())


def exists_email_in_users(email: str, instance=None):
    """
    Validando se existe um usuário com email já existente
    """
    user = None

    try:
        user = User.objects.get(email=email)

    except DoesNotExist:
        return False

    except MultipleObjectsReturned:
        return True

    # verifico se o id retornado na pesquisa é mesmo da minha instancia
    # informado no parâmetro
    if instance and instance.id == user.id:
        return False

    return True


def exists_cpf_in_users(cpf: str):
    """
    Validando se existe um usuário com cpf já existente
    """
    user = None
    try: 
        user = User.objects.get(cpf=cpf)

    except DoesNotExist:
        return True
    
    except MultipleObjectsReturned:
        return False  



def get_user_by_email(email: str):
    try:
        # buscamos todos os usuários da base utilizando o paginate
        return User.objects.get(email=email)

    except DoesNotExist:
        return resp_does_not_exist('Users', 'Usuário')

    except FieldDoesNotExist as e:
        return resp_exception('Users', description=e.__str__())

    except Exception as e:
        return resp_exception('Users', description=e.__str__())