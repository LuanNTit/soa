from flask import Flask, request, session
from flask_restful import Api, Resource
from functools import wraps

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

users = [
    {"username": "luanit", "password": "1234", "roles": ["admin"]},
    {"username": "test123", "password": "4567", "roles": ["user"]}
]

class User:
    def __init__(self, user_id, username, password, roles=None):
        self.id = user_id
        self.username = username
        self.password = password
        self.roles = roles if roles else []

    def has_role(self, role):
        return role in self.roles

def load_user(user_id):
    user_data = next((user for user in users if user['username'] == user_id), None)
    if user_data:
        return User(user_data['username'], user_data['username'], user_data['password'], user_data.get('roles', []))
    return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Giả mạo việc người dùng đã đăng nhập và gán giá trị cụ thể cho 'user_id'
        session['user_id'] = 'luanit'
        # session.clear()
        print(session)
        if 'user_id' not in session:
            return {"message": "Unauthorized"}, 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/protected')
@login_required
def protected_route():
    return {"message": "This is a protected route."}

class RegistrationResource(Resource):
    def post(self):
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')
        roles = data.get('roles', [])

        if not username or not password:
            return {"message": "Missing username or password"}, 400

        if any(user['username'] == username for user in users):
            return {"message": "Username already exists"}, 400

        new_user = {'username': username, 'password': password, 'roles': roles}
        users.append(new_user)

        return {"message": "Registration successful", "user": new_user}, 201

api.add_resource(RegistrationResource, '/register')

class LoginResource(Resource):
    def post(self):
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        user = next((user for user in users if user['username'] == username), None)

        if user and user['password'] == password:
            session['user_id'] = user['username']
            print(session)
            return {"message": "Login successful", "user": user}
        else:
            return {"message": "Invalid username or password"}, 401

api.add_resource(LoginResource, '/login')

class UsersResource(Resource):
    @login_required
    def get(self):
        user_id = session.get('user_id')
        user = load_user(user_id)
        print(session)

        if not user.has_role('admin'):
            return {"message": "Permission denied"}, 403

        return {"users": [{"username": user.username, "roles": user.roles} for user in [load_user(user['username']) for user in users]]}

api.add_resource(UsersResource, '/users')

class LogoutResource(Resource):
    @login_required
    def post(self):
        session.pop('user_id', None)
        print(session)
        return {"message": "Logout successful"}

api.add_resource(LogoutResource, '/logout')

class UserInfoResource(Resource):
    @login_required
    def get(self):
        user_id = session.get('user_id')
        user = load_user(user_id)

        if not user:
            return {"message": "User not found"}, 404

        return {
            "username": user.username,
            "roles": user.roles
        }

api.add_resource(UserInfoResource, '/user-info')

if __name__ == '__main__':
    app.run(debug=True, port=8081)
