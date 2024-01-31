from app import app, socketio
from flask_socketio import SocketIO

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug=True)