from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SECRET_KEY'] = '9912277968'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store active users and their rooms
active_users = {}

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    user_id = request.sid
    if user_id in active_users:
        room = active_users[user_id]['room']
        username = active_users[user_id]['username']
        leave_room(room)
        del active_users[user_id]
        emit('user_left', {'username': username}, room=room)
    print('Client disconnected')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    active_users[request.sid] = {'username': username, 'room': room}
    emit('user_joined', {'username': username}, room=room)

@socketio.on('leave')
def on_leave(data):
    user_id = request.sid
    if user_id in active_users:
        room = active_users[user_id]['room']
        username = active_users[user_id]['username']
        leave_room(room)
        del active_users[user_id]
        emit('user_left', {'username': username}, room=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    emit('message', data, room=room)

@socketio.on('get_active_users')
def get_active_users(data):
    room = data['room']
    users = [user['username'] for user in active_users.values() if user['room'] == room]
    emit('active_users', {'users': users}, room=room)

if __name__ == '__main__':
    # socketio.run(app, debug=True, host='0.0.0.0')
    socketio.run(app, debug=True)