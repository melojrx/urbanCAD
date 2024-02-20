from app import app, socketio

if __name__ == "__main__":
        # app.run(host='0.0.0.0', port=8009)
        socketio.run(app, debug=True)
        # socketio.run(app, debug=True, cors_allowed_origins='*', ping_timeout=30)