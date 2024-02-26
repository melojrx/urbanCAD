from app import app, socketio

if __name__ == "__main__":
    #app.run(debug=True)
    #socketio.run(app, debug=True)
    socketio.run(app, debug=True ,cors_allowed_origins='http://201.47.23.87:8009/', ping_timeout=90, ping_interval=20, transports=["websocket"])    