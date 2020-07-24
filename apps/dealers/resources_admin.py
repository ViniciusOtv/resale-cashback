from flask import request

from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist

from apps.responses import resp_ok, resp_exception
from apps.messages import MSG_RESOURCE_FETCHED_PAGINATED, MSG_RESOURCE_FETCHED

from .models import User
from .schemas import UserSchema
from .utils import get_user_by_id

class AdminUserPageList(Resource):
    def get(self, page_id=1):
        schema = UserSchema(many=True)
        page_size = 10 

        if 'page_size' in request.args:
            if int(request.args.get('page_size')) < 1:
                page_size = 10 
            else: 
                page_size = int(request.args.get('page_size'))

        try: 
            users = User.objects().paginate(page_id, page_size)

        except FieldDoesNotExist as e:
            return resp_exception('Users', description=e.__str__())

        except FieldDoesNotExist as e: 
            return resp_exception('Users', description=e.__str__())

        except Exception as e: 
            return resp_exception('Users', description=e.__str__())

        extra = {
            'page': users.page, 'pages': users.pages, 'total': users.total,
            'params': {'page_size': page_size}
        }  

        result = schema.dump(users.items)

        return resp_ok(
            'Users', MSG_RESOURCE_FETCHED_PAGINATED.format('usuários'), data=result, 
            **extra
        )

class AdminUserResource(Resource): 
    
    def get(self, user_id):
        result = None
        schema = UserSchema()

        user = get_user_by_id(user_id)

        if not isinstance(user, User):
            return user

        result = schema.dump(user)    

        return resp_ok(
            'Users', MSG_RESOURCE_FETCHED.format('Usuários'), data=result
        )    

