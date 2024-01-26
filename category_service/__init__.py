from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from functools import wraps
import requests

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

# Danh sách đơn giản để lưu trữ danh mục
categories = [
    {"id": 1, "name": "Category 1", "image": "image_url_1"},
    {"id": 2, "name": "Category 2", "image": "image_url_2"},
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
category_parser = reqparse.RequestParser()
category_parser.add_argument('name', type=str, help='Name of the category is required', required=True)
category_parser.add_argument('image', type=str, help='Image URL of the category is required', required=True)

class CategoryResource(Resource):
    # @login_required
    def get(self, category_id):
        category = next((category for category in categories if category['id'] == category_id), None)
        if category:
            return {"name": category["name"], "image": category["image"]}
        else:
            return {"message": "Category not found"}, 404

    # @login_required
    def put(self, category_id):
        data = category_parser.parse_args()
        category = next((category for category in categories if category['id'] == category_id), None)
        if category:
            category['name'] = data['name']
            category['image'] = data['image']
            return {"message": "Category updated successfully", "category": category}
        else:
            return {"message": "Category not found"}, 404

    # @login_required
    def delete(self, category_id):
        global categories
        categories = [category for category in categories if category['id'] != category_id]
        return {"message": "Category deleted successfully"}

class CategoryListResource(Resource):
    # @login_required
    def get(self):
        return {"categories": categories}

    # @login_required
    def post(self):
        data = category_parser.parse_args()
        new_category = {'id': len(categories) + 1, 'name': data['name'], 'image': data['image']}
        categories.append(new_category)
        return {"message": "Category created successfully", "category": new_category}, 201

api.add_resource(CategoryListResource, '/categories')
api.add_resource(CategoryResource, '/categories/<int:category_id>')

# if __name__ == '__main__':
#     # authentication_api_response = requests.get()
#     app.run(debug=True, port=8082)
