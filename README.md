# 🎮 Tic Tac Toe Multiplayer Web App

A beautiful, modern Tic Tac Toe multiplayer game with real-time gameplay, chat system, and stunning animations!

## Features

✨ **Beautiful Modern UI** - Gradient backgrounds, smooth animations, and polished design
🎯 **Real-time Multiplayer** - Play with friends using 4-digit room codes
💬 **Built-in Chat** - Communicate with your opponent during the game
🎉 **Victory Celebrations** - Confetti animations and victory messages
🔄 **Rematch System** - Easily start a new game with the same opponent
📱 **Responsive Design** - Works great on desktop and mobile devices

## Installation

### Local Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

### PythonAnywhere Deployment

1. **Upload Files**:
   - Upload all files (app.py, requirements.txt, templates/, static/) to your PythonAnywhere account

2. **Install Dependencies**:
   - Go to the "Consoles" tab
   - Start a Bash console
   - Navigate to your project directory
   - Run: `pip install --user -r requirements.txt`

3. **Configure Web App**:
   - Go to the "Web" tab
   - Click "Add a new web app"
   - Select "Flask" and Python version
   - Set the source code directory to your project folder
   - Edit the WSGI configuration file:
   
   ```python
   import sys
   path = '/home/yourusername/your-project-folder'
   if path not in sys.path:
       sys.path.append(path)

   from app import app as application
   ```

4. **Enable WebSocket Support**:
   - Note: PythonAnywhere free tier doesn't support WebSockets
   - You'll need a paid account or use alternative hosting

### Deployment with Pinggy (Port Forwarding)

If you want to use Pinggy for port forwarding:

1. Install Pinggy:
```bash
curl -O https://dashboard.pinggy.io/downloads/linux
chmod +x pinggy
```

2. Run your Flask app locally:
```bash
python app.py
```

3. In another terminal, start Pinggy:
```bash
./pinggy tcp 5000
```

4. Pinggy will provide you with a public URL that you can share with friends!

### Alternative Hosting Options

For production deployment with WebSocket support, consider:

- **Heroku**: Full WebSocket support
- **Railway.app**: Easy deployment with WebSockets
- **Render**: Free tier with WebSocket support
- **DigitalOcean**: VPS with full control
- **AWS/GCP**: Production-grade hosting

## How to Play

1. **Create a Room**: Click "Create Room" to generate a 4-digit room code
2. **Share the Code**: Give the room code to your friend
3. **Join Room**: Your friend enters the code and clicks "Join Room"
4. **Play**: Take turns clicking on the board to place X or O
5. **Chat**: Use the chat panel to communicate during the game
6. **Rematch**: After the game ends, click "Rematch" to play again

## Technical Details

### Technologies Used
- **Backend**: Flask + Flask-SocketIO
- **Frontend**: HTML5, CSS3, JavaScript
- **Real-time Communication**: Socket.IO
- **Styling**: Modern CSS with gradients, animations, and transitions

### Game Features
- 4-digit room code system for easy matchmaking
- Real-time synchronization using WebSockets
- Turn-based gameplay with validation
- Win detection with visual highlighting
- Draw detection
- Chat system with timestamps
- Confetti celebration for winners
- Smooth animations and transitions

### Code Structure
```
project/
├── app.py                 # Flask server with Socket.IO
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main game interface
└── README.md             # This file
```

## Configuration

To change the secret key (recommended for production):

Edit `app.py`:
```python
app.config['SECRET_KEY'] = 'your-unique-secret-key-here'
```

To change the port:
```python
socketio.run(app, host='0.0.0.0', port=YOUR_PORT, debug=False)
```

## Troubleshooting

**Issue**: "Room not found" error
- **Solution**: Make sure both players are connected to the same server

**Issue**: Chat messages not appearing
- **Solution**: Check that WebSockets are enabled and working

**Issue**: Game freezes
- **Solution**: Refresh the page and rejoin the room

**Issue**: Can't connect on PythonAnywhere
- **Solution**: PythonAnywhere free tier doesn't support WebSockets. Use paid tier or alternative hosting.

## Browser Support

Works on all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

## License

Free to use and modify!

## Credits

Created with ❤️ using Flask and Socket.IO

Enjoy playing! 🎮
