from flask import request

from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist

from apps.responses import resp_ok, resp_exception
from apps.messages import MSG_RESOURCE_FETCHED_PAGINATED, MSG_RESOURCE_FETCHED

from flask_jwt_extended import get_jwt_identity, jwt_required

from .models import User
from .schemas import UserSchema
from .utils import get_user_by_id, exists_email_in_users, get_user_by_email

class AdminUserPageList(Resource):
    @jwt_required
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
    @jwt_required
    def get(self, user_id):
        result = None
        schema = UserSchema()
        current_user = get_user_by_email(get_jwt_identity())
        
        if not isinstance(current_user, User):
            return current_user

        if not (current_user.is_active()) and current_user.is_admin():
            return resp_notallowed_user('Users')    

        user = get_user_by_id(user_id)

        if not isinstance(user, User):
            return user

        result = schema.dump(user)    

        return resp_ok(
            'Users', MSG_RESOURCE_FETCHED.format('Usuários'), data=result
        )    

