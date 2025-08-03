import ctypes
import socket
from flask import Flask, request, jsonify
import subprocess
import os
from flask_cors import CORS  # Enable CORS

app = Flask(__name__)
CORS(app)  # Allow requests from any origin (especially from your mobile)

SECRET_TOKEN = "XjD9f8#@df0s8d2kFz"  # Change this to any strong secret key you like

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'

@app.route('/')
def index():
    return 'Laptop Server is Running 🎯'

def is_authorized(request):
    token = request.headers.get('Authorization')
    if token != SECRET_TOKEN:
        return False
    return True

@app.route('/command', methods=['POST'])
def handle_command():
    if not is_authorized(request):
        return jsonify({"message": "Unauthorized", "status": "error"}), 401

    data = request.get_json()
    print(f"Received data: {data}")
    command = data.get('command')
    
    if command == "ping":
        return jsonify({"message": "Connection successful", "status": "success"}), 200
    elif command == "open_notepad":
        subprocess.Popen(['notepad.exe'])
        return jsonify({"message": "Notepad opened", "status": "success"}), 200
    elif command == "shutdown":
        os.system("shutdown /s /f /t 0")
        return jsonify({"message": "Shutting down", "status": "success"}), 200
    elif command == "lock_screen":
        ctypes.windll.user32.LockWorkStation()
        return jsonify({"message": "Screen locked", "status": "success"}), 200
    else:
        return jsonify({"message": "Unknown command", "status": "error"}), 400

if __name__ == '__main__':
    ip = get_local_ip()
    print(f"🚀 Server is live at http://{ip}:5000")
    app.run(host='0.0.0.0', port=5000)
