from app import app, socketio

if __name__ == "__main__":
    #app.run(debug=True)
    socketio.run(app, debug=True)
    # socketio.run(app, debug=True ,cors_allowed_origins='*', ping_timeout=30)    