import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
import requests
import json

kivy.require('2.1.0')  # Ensure the required version of Kivy is used

class ControlApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        # Label to display status
        self.status_label = Label(text="Status: Not connected", size_hint=(1, 0.2), color=(1, 1, 1, 1))
        self.layout.add_widget(self.status_label)
        
        # Text input for IP address
        self.ip_input = TextInput(hint_text="Enter laptop IP address", size_hint=(1, 0.1), multiline=False)
        self.layout.add_widget(self.ip_input)
        
        # Connect button
        self.connect_button = Button(text="Connect", size_hint=(1, 0.2))
        self.connect_button.bind(on_press=self.connect_to_server)
        self.layout.add_widget(self.connect_button)
        
        # Command buttons (they will be shown after connection is successful)
        self.command_buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.4))
        
        self.open_notepad_button = Button(text="Open Notepad")
        self.open_notepad_button.bind(on_press=self.send_command_open_notepad)
        self.command_buttons_layout.add_widget(self.open_notepad_button)
        
        self.shutdown_button = Button(text="Shutdown")
        self.shutdown_button.bind(on_press=self.send_command_shutdown)
        self.command_buttons_layout.add_widget(self.shutdown_button)
        
        self.lock_screen_button = Button(text="Lock Screen")
        self.lock_screen_button.bind(on_press=self.send_command_lock_screen)
        self.command_buttons_layout.add_widget(self.lock_screen_button)
        
        self.layout.add_widget(self.command_buttons_layout)
        self.command_buttons_layout.disabled = True  # Disable command buttons initially
        
        return self.layout
    
    def connect_to_server(self, instance):
        ip = self.ip_input.text.strip()  # Get IP address from input field
        if not ip:
            self.status_label.text = "Status: IP is required"
            self.status_label.color = (1, 0, 0, 1)  # Red color for missing IP
            return

        url = f"http://{ip}:5000/command"  # Use dynamic IP from TextInput
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"command": "ping"})  # Sending a "ping" command to check connection

        try:
            response = requests.post(url, headers=headers, data=payload)  # POST request with "ping"
            if response.status_code == 200:
                self.status_label.text = "Status: Connected!"
                self.status_label.color = (0, 1, 0, 1)  # Green color for success
                print("Connection successful!")
                self.command_buttons_layout.disabled = False  # Enable command buttons
            else:
                self.status_label.text = "Status: Failed to connect"
                self.status_label.color = (1, 0, 0, 1)  # Red color for failure
                print(f"Error {response.status_code}: {response.json()['message']}")
        except requests.exceptions.RequestException as e:
            self.status_label.text = "Status: Connection failed"
            self.status_label.color = (1, 0, 0, 1)  # Red color for failure
            print(f"Error connecting to server: {e}")
    
    def send_command_open_notepad(self, instance):
        self.send_command("open_notepad")
    
    def send_command_shutdown(self, instance):
        self.send_command("shutdown")
    
    def send_command_lock_screen(self, instance):
        self.send_command("lock_screen")
    
    def send_command(self, command):
        ip = self.ip_input.text.strip()  # Get IP address from input field
        if not ip:
            self.status_label.text = "Status: IP is required"
            self.status_label.color = (1, 0, 0, 1)  # Red color for missing IP
            return

        url = f"http://{ip}:5000/command"  # Use dynamic IP from TextInput
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"command": command})

        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                self.status_label.text = f"Status: {command} executed"
                self.status_label.color = (0, 1, 0, 1)  # Green color for success
            else:
                self.status_label.text = f"Status: {command} failed"
                self.status_label.color = (1, 0, 0, 1)  # Red color for failure
        except requests.exceptions.RequestException as e:
            self.status_label.text = f"Status: {command} failed"
            self.status_label.color = (1, 0, 0, 1)  # Red color for failure
            print(f"Error executing {command}: {e}")

if __name__ == '__main__':
    ControlApp().run()
