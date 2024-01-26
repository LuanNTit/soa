from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from functools import wraps

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

# Danh sách đơn đặt hàng
orders = [
    {"id": 1, "id_account": 1, "id_category": 1, "request": "Order request 1", "status": "Pending"},
    {"id": 2, "id_account": 2, "id_category": 2, "request": "Order request 2", "status": "Completed"},
]

# Decorator để yêu cầu đăng nhập
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in request.headers:
            return {"message": "Unauthorized"}, 401
        return f(*args, **kwargs)

    return decorated_function

# Parser để xác thực và lấy dữ liệu từ yêu cầu
order_parser = reqparse.RequestParser()
order_parser.add_argument('id_account', type=int, help='Account ID is required', required=True)
order_parser.add_argument('id_category', type=int, help='Category ID is required', required=True)
order_parser.add_argument('request', type=str, help='Order request is required', required=True)
order_parser.add_argument('status', type=str, help='Order status is required', required=True)

class OrderResource(Resource):
    # @login_required
    def get(self, order_id):
        order = next((order for order in orders if order['id'] == order_id), None)
        if order:
            return {
                "id": order["id"],
                "id_account": order["id_account"],
                "id_category": order["id_category"],
                "request": order["request"],
                "status": order["status"]
            }
        else:
            return {"message": "Order not found"}, 404

    # @login_required
    def put(self, order_id):
        data = order_parser.parse_args()
        order = next((order for order in orders if order['id'] == order_id), None)
        if order:
            order.update({
                "id_account": data['id_account'],
                "id_category": data['id_category'],
                "request": data['request'],
                "status": data['status']
            })
            return {"message": "Order updated successfully", "order": order}
        else:
            return {"message": "Order not found"}, 404

    # @login_required
    def delete(self, order_id):
        global orders
        orders = [order for order in orders if order['id'] != order_id]
        return {"message": "Order deleted successfully"}

class OrderListResource(Resource):
    # @login_required
    def get(self):
        return {"orders": orders}

    # @login_required
    def post(self):
        data = order_parser.parse_args()
        new_order = {'id': len(orders) + 1, **data}
        orders.append(new_order)
        return {"message": "Order created successfully", "order": new_order}, 201

api.add_resource(OrderListResource, '/orders')
api.add_resource(OrderResource, '/orders/<int:order_id>')

# if __name__ == '__main__':
#     app.run(debug=True, port=8084)
