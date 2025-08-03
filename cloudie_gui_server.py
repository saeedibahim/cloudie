import customtkinter as ctk
import threading
import socket
import subprocess
import ctypes
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.serving import make_server
from datetime import datetime

# --------------------- Flask Server Setup ---------------------
app = Flask(__name__)
CORS(app)

SECRET_TOKEN = "XjD9f8#@df0s8d2kFz"
LOG_FUNCTION = None  # GUI logger set later

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'

def log_event(message):
    if LOG_FUNCTION:
        timestamp = datetime.now().strftime('%H:%M:%S')
        LOG_FUNCTION(f"[{timestamp}] {message}")

# Optional: Try to get MAC from IP (only works on LAN)
def get_mac_from_ip(ip):
    try:
        result = subprocess.check_output(f"arp -a {ip}", shell=True).decode()
        for line in result.splitlines():
            if ip in line:
                return line.split()[1]
    except:
        pass
    return "Unknown MAC"

@app.route('/')
def index():
    log_event("Ping received on `/`")
    return 'Laptop Server is Running 🎯'

def is_authorized(request):
    token = request.headers.get('Authorization')
    return token == SECRET_TOKEN

@app.route('/command', methods=['POST'])
def handle_command():
    if not is_authorized(request):
        log_event("⚠️ Unauthorized request blocked")
        return jsonify({"message": "Unauthorized", "status": "error"}), 401

    data = request.get_json()
    command = data.get('command')
    device_name = data.get('device_name', 'Unknown Device')
    device_id = data.get('device_id', 'Unknown ID')
    client_ip = request.remote_addr
    mac = get_mac_from_ip(client_ip)

    log_event(f"📲 [{device_name}] ({device_id} / {client_ip} / {mac}) → Command: {command}")

    if command == "ping":
        return jsonify({"message": "Connection successful", "status": "success"}), 200
    elif command == "open_notepad":
        subprocess.Popen(['notepad.exe'])
        log_event("✅ Action: Opened Notepad")
        return jsonify({"message": "Notepad opened", "status": "success"}), 200
    elif command == "shutdown":
        log_event("⚠️ Action: Shutdown requested")
        os.system("shutdown /s /f /t 0")
        return jsonify({"message": "Shutting down", "status": "success"}), 200
    elif command == "lock_screen":
        ctypes.windll.user32.LockWorkStation()
        log_event("🔒 Action: Screen locked")
        return jsonify({"message": "Screen locked", "status": "success"}), 200
    else:
        log_event("❓ Action: Unknown command received")
        return jsonify({"message": "Unknown command", "status": "error"}), 400

# --------------------- Flask Server Thread Wrapper ---------------------
class FlaskServerThread(threading.Thread):
    def __init__(self, host="0.0.0.0", port=5000):
        threading.Thread.__init__(self)
        self.server = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()
        self.daemon = True

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

# --------------------- GUI ---------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

gui = ctk.CTk()
gui.title("🌥️ Cloudie Server Control Panel")
gui.geometry("800x620")
gui.resizable(False, False)

server_thread = None

# GUI Logger Function
def log_to_gui(message):
    log_box.configure(state="normal")
    log_box.insert("end", message + "\n")
    log_box.configure(state="disabled")
    log_box.see("end")

LOG_FUNCTION = log_to_gui

# Start/Stop Server
def start_server():
    global server_thread
    if server_thread is None:
        try:
            server_thread = FlaskServerThread()
            server_thread.start()
            ip = get_local_ip()
            status_label.configure(text=f"Server running at {ip}:5000 ✅", text_color="green")
            log_event(f"🚀 Server started on http://{ip}:5000")
        except Exception as e:
            status_label.configure(text=f"Error: {e}", text_color="red")
            log_event(f"❌ Server error: {e}")
    else:
        status_label.configure(text="Server already running ✅", text_color="green")

def stop_server():
    global server_thread
    if server_thread:
        server_thread.shutdown()
        server_thread = None
        status_label.configure(text="Server stopped ⛔", text_color="red")
        log_event("⛔ Server stopped manually")
    else:
        status_label.configure(text="Server not running ❌", text_color="orange")
        log_event("ℹ️ Stop requested but server not running")

# --- UI Layout ---
title = ctk.CTkLabel(gui, text="Cloudie Server", font=ctk.CTkFont(size=26, weight="bold"))
title.pack(pady=15)

status_label = ctk.CTkLabel(gui, text="Server not running ❌", text_color="red", font=ctk.CTkFont(size=15))
status_label.pack(pady=5)

# Button Frame with defined size
btn_frame = ctk.CTkFrame(gui, width=400, height=80, corner_radius=10, fg_color="#1f1f1f")
btn_frame.pack(pady=10)
btn_frame.pack_propagate(False)

# Buttons inside the frame
ctk.CTkButton(btn_frame, text="▶️ Start Server", width=150, command=start_server).grid(row=0, column=0, padx=15)
ctk.CTkButton(btn_frame, text="⏹️ Stop Server", width=150, command=stop_server).grid(row=0, column=1, padx=15)

# Log Section
ctk.CTkLabel(gui, text="📜 Activity Log", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=8)

log_box = ctk.CTkTextbox(gui, width=650, height=300, font=ctk.CTkFont(size=13), corner_radius=10)
log_box.pack(padx=10)
log_box.configure(state="disabled")

gui.mainloop()
