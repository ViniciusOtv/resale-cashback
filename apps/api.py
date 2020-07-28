from flask_restful import Api, Resource

from apps.dealers.resources import SignUp
from apps.dealers.resources_admin import AdminUserPageList, AdminUserResource

from apps.auth.resources import AuthResource, RefreshTokenResource

from apps.order.resources import order
from apps.order.resource_admin import AdminUserOrderList, AdminOrderResource, AdminOrderDeleteResource


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
    api.add_resource(RefreshTokenResource, '/auth/refresh')
    
    api.add_resource(order, '/order')
    api.add_resource(AdminUserOrderList, '/admin/order/<int:page_id>')
    api.add_resource(AdminOrderResource, '/admin/order/<string:order_id>')
    api.add_resource(AdminOrderDeleteResource, '/admin/delete-order/<float:order_values>')


    api.init_app(app)
