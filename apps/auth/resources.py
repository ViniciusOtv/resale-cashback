from flask import request

from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from bcrypt import checkpw

from apps.dealers.models import User
from apps.dealers.schemas import UserSchema
from apps.dealers.utils import get_user_by_email
from apps.messages import MSG_NO_DATA, MSG_TOKEN_CREATED
from apps.responses import resp_ok, resp_data_invalid, resp_notallowed_user

from .schemas import LoginSchema

class AuthResource(Resource):
    def post(self, *args, **kwargs):
        req_data = request.get_json() or None
        user = None
        login_schema = LoginSchema()
        schema = UserSchema()

        if req_data is None:
            return resp_data_invalid('Users', [], msg=MSG_NO_DATA)

        data, errors = login_schema.load(req_data)  

        if errors:
            return resp_data_invalid('Users', errors)

        # Buscando o usuário pelo email
        user = get_user_by_email(data.get('email'))

        if not isinstance(user, User):
            return user

        # Verificando se o usuário está ativo e possui permissão
        if not user.is_active():
            return resp_notallowed_user('Auth')

        if checkpw(data.get('password').encode('utf-8'), user.password.encode('utf-8')):

            extras = {
                'token': create_access_token(identity=user.email), 
                'refresh': create_refresh_token(identity=user.email)
            }

            result = schema.dump(user)

            return resp_ok(
                'Auth', MSG_TOKEN_CREATED, data=result.data, **extras
            )
            
        return resp_notallowed_user('Auth')    

