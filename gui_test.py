import customtkinter as ctk


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

gui = ctk.CTk()
gui.title("🌥️ Cloudie Server Control Panel")
gui.geometry("800x620")
gui.resizable(False, False)

def start_server():
    pass

def stop_server():
    pass


title = ctk.CTkLabel(gui, text="Cloudie Server", font=ctk.CTkFont(size=26, weight="bold"))
title.pack(pady=15)

status_label = ctk.CTkLabel(gui, text="Server not running ❌", text_color="red", font=ctk.CTkFont(size=15))
status_label.pack(pady=5)

# Button Frame with defined size
btn_frame = ctk.CTkFrame(gui, width=400, height=80, corner_radius=10, fg_color="#1f1f1f")
btn_frame.pack(pady=10)
btn_frame.pack_propagate(False)

# Buttons inside the frame
ctk.CTkButton(btn_frame, text="Start Server", font=("Poppins", 16), width=150, height=50, command=start_server).grid(row=0, column=0, padx=15, pady=10)
ctk.CTkButton(btn_frame, text="Stop Server", font=("Poppins", 16), width=150,  height=50, command=stop_server).grid(row=0, column=1, padx=15, pady=10)

# Log Section
ctk.CTkLabel(gui, text="📜 Activity Log", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=8)

log_box = ctk.CTkTextbox(gui, width=650, height=300, font=ctk.CTkFont(size=13), corner_radius=10)
log_box.pack(padx=10)
log_box.configure(state="disabled")

gui.mainloop()