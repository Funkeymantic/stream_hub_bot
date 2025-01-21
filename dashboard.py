from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/status')
def status():
    return jsonify({"status": "Bot is running"})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
