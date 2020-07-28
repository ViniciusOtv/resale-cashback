from flask import request
import json
# Third
from flask_restful import Resource
from bcrypt import gensalt, hashpw
from mongoengine.errors import NotUniqueError, ValidationError

# Apps
from apps.responses import (
    resp_already_exists,
    resp_exception,
    resp_data_invalid,
    resp_ok
)
from apps.messages import MSG_NO_DATA, MSG_PASSWORD_WRONG, MSG_INVALID_DATA, MSG_PASSWORD_NOT_SAME, MSG_DOCUMENT_NULL, MSG_DOCUMENT_ALREAD_EXIST, MSG_EMAIL_NULL, MSG_EMAIL_ALREAD_EXIST
from apps.messages import MSG_RESOURCE_CREATED

# Local
from .models import User
from .schemas import UserRegistrationSchema, UserSchema
from .utils import check_password_in_signup, check_password_is_same, check_document, exists_cpf_in_users, exists_email_in_users


class SignUp(Resource):
    def post(self, *args, **kwargs):
        # Inicializo todas as variaveis utilizadas
        req_data = request.get_json() or None
        dict_data, errors, result = None, None, None
        password, confirm_password = None, None
        schema = UserRegistrationSchema()

        # Se meus dados postados forem Nulos retorno uma respota inválida
        if req_data is None:
            return resp_data_invalid('Users', [], msg=MSG_NO_DATA)

        password = req_data.get('password', None)
        confirm_password = req_data.pop('confirm_password', None)
        document = req_data.get('cpf', None)

        if not check_document(document):
            errors = {'cpf': MSG_DOCUMENT_NULL}
            return resp_data_invalid('Users', errors)

        if not exists_cpf_in_users(document):
            errors = {'cpf': MSG_DOCUMENT_ALREAD_EXIST}
            return resp_data_invalid('Users', errors)

        if not exists_email_in_users(document):
            errors = {'email': MSG_EMAIL_ALREAD_EXIST}
            return resp_data_invalid('Users', errors)

        # verifico através de uma função a senha e a confirmação da senha
        # Se as senhas não são iguais retorno uma respota inválida
        if not check_password_in_signup(password, confirm_password):
            errors = {'password': MSG_PASSWORD_WRONG}
            return resp_data_invalid('Users', errors)

        if not check_password_is_same(password, confirm_password):
            errors = {'password': MSG_PASSWORD_NOT_SAME}
            return resp_data_invalid('Users', errors)

        dict_data = {
            "full_name": req_data.get('full_name', None),
            "email": req_data.get('email', None),
            "password": req_data.get('password', None),
            "cpf": req_data.get('cpf', None),
            "active": req_data.get('active', None)
        }

        data = json.dumps(dict_data)

        # Se houver erros retorno uma resposta inválida
        if errors:
            return resp_data_invalid('Users', errors)

        # Crio um hash da minha senha
        hashed = hashpw(password.encode('utf-8'), gensalt(12))

        # Salvo meu modelo de usuário com a senha criptografada e email em lower case
        # Qualquer exceção ao salvar o modelo retorno uma resposta em JSON
        # ao invés de levantar uma exception no servidor
        try:
            dict_data['password'] = hashed
            dict_data['email'] = dict_data['email'].lower()
            model = User(**dict_data)
            model.save()

        except ValidationError as e:
            return resp_exception('Users', msg=MSG_INVALID_DATA, description=e)

        except Exception as e:
            return resp_exception('Users', description=e)

        # Realizo um dump dos dados de acordo com o modelo salvo
        schema = UserSchema()
        result = schema.dump(model)

        # Retorno 200 o meu endpoint
        return resp_ok(
            'Users', MSG_RESOURCE_CREATED.format('Usuário'), data=result,
        )
