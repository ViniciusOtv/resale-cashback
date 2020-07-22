from flask_restful import Api, Resource
from apps.dealers.resources import SignUp
from apps.purchase.resources import Purchase


class Index(Resource):

    def get(self):
        return {'hello': 'world by apps'}


# Instânciamos a API do FlaskRestful
api = Api()


def configure_api(app):

    api.add_resource(SignUp, '/dealers')

    api.add_resource(Purchase, '/purchase')

    api.init_app(app)