from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from functools import wraps

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

# Danh sách đơn giản để lưu trữ sự kiện với thông tin danh mục
events = [
    {"id": 1, "title": "Event 1", "content": "Content for Event 1", "category_id": 1},
    {"id": 2, "title": "Event 2", "content": "Content for Event 2", "category_id": 2},
]

# Decorator để yêu cầu đăng nhập
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in request.headers:
            return {"message": "Unauthorized"}, 401
        return f(*args, **kwargs)

    return decorated_function

# Parser để xác thực và lấy dữ liệu từ yêu cầu, bao gồm cả loại danh mục
event_parser = reqparse.RequestParser()
event_parser.add_argument('title', type=str, help='Title of the event is required', required=True)
event_parser.add_argument('content', type=str, help='Content of the event is required', required=True)
event_parser.add_argument('category_id', type=str, help='Category id of the event is required', required=True)

class EventResource(Resource):
    # @login_required
    def get(self, event_id):
        event = next((event for event in events if event['id'] == event_id), None)
        if event:
            return {"title": event["title"], "content": event["content"], "category": event["category_id"]}
        else:
            return {"message": "Event not found"}, 404

    # @login_required
    def put(self, event_id):
        data = event_parser.parse_args()
        event = next((event for event in events if event['id'] == event_id), None)
        if event:
            event['title'] = data['title']
            event['content'] = data['content']
            event['category_id'] = data['category_id']
            return {"message": "Event updated successfully", "event": event}
        else:
            return {"message": "Event not found"}, 404

    # @login_required
    def delete(self, event_id):
        global events
        events = [event for event in events if event['id'] != event_id]
        return {"message": "Event deleted successfully"}

class EventListResource(Resource):
    # @login_required
    def get(self):
        return {"events": events}

    # @login_required
    def post(self):
        data = event_parser.parse_args()
        new_event = {'id': len(events) + 1, 'title': data['title'], 'content': data['content'], 'category_id': data['category_id']}
        events.append(new_event)
        return {"message": "Event created successfully", "event": new_event}, 201

api.add_resource(EventListResource, '/events')
api.add_resource(EventResource, '/events/<int:event_id>')

if __name__ == '__main__':
    app.run(debug=True, port=8083)
