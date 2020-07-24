import json

from flask import request

from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity
from bcrypt import checkpw

from apps.dealers.models import User
from apps.dealers.schemas import UserSchema
from apps.dealers.utils import get_user_by_email
from apps.messages import MSG_NO_DATA, MSG_TOKEN_CREATED
from apps.responses import resp_ok, resp_data_invalid,  resp_notallowed_user

from .schemas import LoginSchema

class AuthResource(Resource):
    def post(self, *args, **kwargs):
        req_data = request.get_json() or None
        user = None
        dict_data, errors, result = None, None, None
        login_schema = LoginSchema()
        schema = UserSchema()

        if req_data is None:
            return resp_data_invalid('Users', [], msg=MSG_NO_DATA)

        # data, errors = login_schema.load(req_data)

        dict_data = { 

            "email": req_data.get('email', None),
            "password": req_data.get('password', None)
        }  

        data = json.dumps(dict_data)

        if errors:
            return resp_data_invalid('Users', errors)

        # Buscando o usuário pelo email
        user = get_user_by_email(dict_data.get('email'))

        if not isinstance(user, User):
            return user

        # Verificando se o usuário está ativo e possui permissão
        if not user.is_active():
            return resp_notallowed_user('Auth')

        if checkpw(dict_data.get('password').encode('utf-8'), user.password.encode('utf-8')):

            extras = {
                'token': create_access_token(identity=user.email), 
                'refresh': create_refresh_token(identity=user.email)
            }

            result = schema.dump(user)

            return resp_ok(
                'Auth', MSG_TOKEN_CREATED, data=result, **extras
            )
            
        return resp_notallowed_user('Auth')    

class RefreshTokenResource(Resource): 

    @jwt_refresh_token_required
    def post(self, *args, **kwargs):
        '''

        Dando um Refresh no token caso expirado. 

        http://flask-jwt-extended.readthedocs.io/en/latest/refresh_tokens.html
        '''
        extras = { 
            'token': create_access_token(identity=get_jwt_identity()),
        }

        return resp_ok(
            'Auth', MSG_TOKEN_CREATED, **extras
        )