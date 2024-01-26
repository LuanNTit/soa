from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Thông tin kết nối với MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'events'

mysql = MySQL(app)

# Route hiển thị tất cả sự kiện
@app.route('/events', methods=['GET'])
def get_events():
    try:
        # Kết nối MySQL và thực hiện truy vấn
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM blogs")
        data = cur.fetchall()
        cur.close()

        # Chuyển đổi dữ liệu thành JSON và trả về
        return jsonify({'events': data})

    except Exception as e:
        return jsonify({'error': str(e)})

# Route hiển thị sự kiện theo id
@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    try:
        # Kết nối MySQL và thực hiện truy vấn
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM events WHERE id = %s", (event_id,))
        data = cur.fetchone()
        cur.close()

        # Nếu không tìm thấy sự kiện, trả về thông báo
        if data is None:
            return jsonify({'message': 'Event not found'})

        # Chuyển đổi dữ liệu thành JSON và trả về
        return jsonify({'event': data})

    except Exception as e:
        return jsonify({'error': str(e)})

# Route xóa sự kiện theo id
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        # Kết nối MySQL và thực hiện truy vấn xóa
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM events WHERE id = %s", (event_id,))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'Event deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})

# Route cập nhật thông tin sự kiện theo id
@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    try:
        # Lấy dữ liệu mới từ request
        new_data = request.get_json()

        # Kết nối MySQL và thực hiện truy vấn cập nhật
        cur = mysql.connection.cursor()
        cur.execute("UPDATE events SET name = %s, location = %s, date = %s WHERE id = %s",
                    (new_data['name'], new_data['location'], new_data['date'], event_id))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'Event updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=8083)
