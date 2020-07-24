from flask_restful import Api, Resource

from apps.dealers.resources import SignUp
from apps.purchase.resources import Purchase
from apps.dealers.resources_admin import AdminUserPageList, AdminUserResource

from apps.auth.resources import AuthResource

class Index(Resource):

    def get(self):
        return {'hello': 'world by apps'}


# Instânciamos a API do FlaskRestful
api = Api()


def configure_api(app):

    api.add_resource(SignUp, '/dealers')
    api.add_resource(AdminUserPageList, '/admin/dealers/<int:page_id>')
    api.add_resource(AdminUserResource, '/admin/dealers/<string:user_id>')

    api.add_resource(AuthResource, '/auth')
    
    api.add_resource(Purchase, '/purchase')


    
    api.init_app(app)
