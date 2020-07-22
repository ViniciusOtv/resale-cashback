from flask_restful import Api, Resource
from apps.dealers.resources import SignUp


class Index(Resource):

    def get(self):
        return {'hello': 'world by apps'}


# Instânciamos a API do FlaskRestful
api = Api()


def configure_api(app):

    api.add_resource(SignUp, '/dealers')

    api.init_app(app)