from flask import request

from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist

from apps.responses import resp_ok, resp_exception
from apps.messages import MSG_RESOURCE_FETCHED_PAGINATED, MSG_RESOURCE_FETCHED
from apps.dealers.utils import get_user_by_email

from flask_jwt_extended import get_jwt_identity, jwt_required

from apps.dealers.models import User

from .models import OrderModel
from .schemas import OrderSchema
from .utils import get_order_by_id


class AdminUserOrderList(Resource):
    @jwt_required
    def get(self, page_id=1):
        schema = OrderSchema(many=True)
        page_size = 10

        if 'page_size' in request.args:
            if int(request.args.get('page_size')) < 1:
                page_size = 10
            else:
                page_size = int(request.args.get('page_size'))

        try:
            order = OrderModel.objects().paginate(page_id, page_size)

        except FieldDoesNotExist as e:
            return resp_exception('Users', description=e.__str__())

        except FieldDoesNotExist as e:
            return resp_exception('Users', description=e.__str__())

        except Exception as e:
            return resp_exception('Users', description=e.__str__())

        extra = {
            'page': order.page, 'pages': order.pages, 'total': order.total,
            'params': {'page_size': page_size}
        }

        result = schema.dump(order.items)

        return resp_ok(
            'order', MSG_RESOURCE_FETCHED_PAGINATED.format('compras'), data=result,
            **extra
        )


class AdminOrderResource(Resource):
    @jwt_required
    def get(self, order_id):
        result = None
        schema = OrderSchema()

        order = get_order_by_id(order_id)

        if not isinstance(order, OrderModel):
            return order

        result = schema.dump(order)

        return resp_ok(
            'order', MSG_RESOURCE_FETCHED.format('Compra'), data=result
        )


class AdminOrderDeleteResource(Resource):
    @jwt_required
    def get(self, order_values):
        result = None
        schema = OrderSchema(many=True)

        order = OrderModel.objects.get().delete()

        if not isinstance(order, OrderModel):
            return order

        result = schema.dump(order.items)

        return resp_ok(
            'order', MSG_RESOURCE_FETCHED_PAGINATED.format('compras'), data=result
        )
