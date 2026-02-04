import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import random
import string
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store game rooms
rooms = {}

def generate_room_code():
    """Generate a random 4-digit room code"""
    return ''.join(random.choices(string.digits, k=4))

def check_winner(board):
    """Check if there's a winner or draw"""
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    
    for combo in winning_combinations:
        if board[combo[0]] and board[combo[0]] == board[combo[1]] == board[combo[2]]:
            return board[combo[0]], combo
    
    if all(cell is not None for cell in board):
        return 'draw', None
    
    return None, None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('create_room')
def handle_create_room():
    room_code = generate_room_code()
    while room_code in rooms:
        room_code = generate_room_code()
    
    rooms[room_code] = {
        'board': [None] * 9,
        'players': {request.sid: 'X'},
        'current_turn': 'X',
        'winner': None,
        'chat': []
    }
    
    join_room(room_code)
    emit('room_created', {
        'room_code': room_code,
        'symbol': 'X',
        'board': rooms[room_code]['board'],
        'current_turn': rooms[room_code]['current_turn'],
        'chat': rooms[room_code]['chat']
    })

@socketio.on('join_room')
def handle_join_room(data):
    room_code = data.get('room_code')
    
    if not room_code:
        emit('error', {'message': 'Room code is required!'})
        return
    
    if room_code not in rooms:
        emit('error', {'message': 'Room not found!'})
        return
    
    if len(rooms[room_code]['players']) >= 2:
        emit('error', {'message': 'Room is full!'})
        return
    
    join_room(room_code)
    rooms[room_code]['players'][request.sid] = 'O'
    
    # Send room info to the joining player
    emit('room_joined', {
        'room_code': room_code,
        'symbol': 'O',
        'board': rooms[room_code]['board'],
        'current_turn': rooms[room_code]['current_turn'],
        'chat': rooms[room_code]['chat']
    })
    
    # Notify the room creator that opponent has joined
    emit('opponent_joined', {
        'board': rooms[room_code]['board'],
        'current_turn': rooms[room_code]['current_turn']
    }, to=room_code, skip_sid=request.sid)

@socketio.on('make_move')
def handle_move(data):
    room_code = data.get('room_code')
    position = data.get('position')
    
    if not room_code or position is None:
        emit('error', {'message': 'Invalid move data!'})
        return
    
    if room_code not in rooms:
        emit('error', {'message': 'Room not found!'})
        return
    
    room = rooms[room_code]
    player_symbol = room['players'].get(request.sid)
    
    if not player_symbol:
        emit('error', {'message': 'You are not in this room!'})
        return
    
    if player_symbol != room['current_turn']:
        emit('error', {'message': 'Not your turn!'})
        return
    
    if room['board'][position] is not None:
        emit('error', {'message': 'Cell already occupied!'})
        return
    
    if room['winner']:
        emit('error', {'message': 'Game is already over!'})
        return
    
    # Make the move
    room['board'][position] = player_symbol
    room['current_turn'] = 'O' if player_symbol == 'X' else 'X'
    
    winner, winning_combo = check_winner(room['board'])
    
    if winner:
        room['winner'] = winner
        emit('game_over', {
            'board': room['board'],
            'winner': winner,
            'winning_combo': winning_combo
        }, to=room_code)
    else:
        emit('move_made', {
            'board': room['board'],
            'position': position,
            'symbol': player_symbol,
            'current_turn': room['current_turn']
        }, to=room_code)

@socketio.on('send_message')
def handle_message(data):
    room_code = data.get('room_code')
    message = data.get('message')
    
    if not room_code or not message:
        return
    
    if room_code not in rooms:
        return
    
    player_symbol = rooms[room_code]['players'].get(request.sid)
    
    if not player_symbol:
        return
    
    timestamp = datetime.now().strftime('%H:%M')
    
    chat_message = {
        'symbol': player_symbol,
        'message': message,
        'timestamp': timestamp
    }
    
    rooms[room_code]['chat'].append(chat_message)
    emit('new_message', chat_message, to=room_code)

@socketio.on('rematch')
def handle_rematch(data):
    room_code = data.get('room_code')
    
    if not room_code:
        return
    
    if room_code not in rooms:
        return
    
    rooms[room_code]['board'] = [None] * 9
    rooms[room_code]['current_turn'] = 'X'
    rooms[room_code]['winner'] = None
    
    emit('rematch_started', {
        'board': rooms[room_code]['board'],
        'current_turn': rooms[room_code]['current_turn']
    }, to=room_code)

@socketio.on('disconnect')
def handle_disconnect():
    for room_code, room in list(rooms.items()):
        if request.sid in room['players']:
            emit('opponent_left', {}, to=room_code, skip_sid=request.sid)
            leave_room(room_code)
            del room['players'][request.sid]
            if len(room['players']) == 0:
                del rooms[room_code]
            break

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
