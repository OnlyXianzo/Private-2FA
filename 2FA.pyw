import os
import sys
import time
import pyperclip
import pyotp
import tkinter as tk
from functools import partial
from dotenv import dotenv_values

# Detect base directory (for .py or .exe)
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Correct .env path handling
env_path = os.path.join(base_dir, "code.env")
print("Looking for .env at:", env_path)

# Load secrets from .env
accounts = dotenv_values(env_path)
print("Loaded accounts:", accounts)

# GUI setup
root = tk.Tk()
root.title("🔐 TOTP Authenticator")
root.geometry("420x600")
root.configure(bg="#1e1e1e")

# Scrollable canvas setup
canvas = tk.Canvas(root, bg="#1e1e1e", highlightthickness=0)
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas, bg="#1e1e1e")
canvas_frame = canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)

title = tk.Label(frame, text="⏳ Refreshes in 30s", fg="#ccc", bg="#1e1e1e", font=("Segoe UI", 14, "bold"))
title.pack(pady=10)

buttons = {}

def copy_code(name, code):
    pyperclip.copy(code)
    title.config(text=f"✔️ Copied: {name}")

def refresh_codes():
    for name, secret in accounts.items():
        try:
            totp = pyotp.TOTP(secret)
            code = totp.now()
        except Exception:
            code = "❌ Error"
        buttons[name].config(text=f"{name}: {code}", command=partial(copy_code, name, code))
    
    # After updating codes, start countdown
    update_countdown()

def update_countdown():
    now = time.time()
    seconds_remaining = 30 - int(now) % 30
    title.config(text=f"⏳ Refreshes in {seconds_remaining}s")

    # If 1 second left, refresh codes next
    if seconds_remaining == 1:
        root.after(1000, refresh_codes)
    else:
        root.after(1000, update_countdown)

# Button for each account
for name in accounts:
    btn = tk.Button(
        frame, text=f"{name}: ...", font=("Segoe UI", 10),
        bg="#2d2d2d", fg="white", relief="flat",
        padx=10, pady=6, anchor="w", width=40
    )
    btn.pack(pady=4, padx=10)
    buttons[name] = btn

# Scroll bindings
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def _on_mousewheel(event):
    canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)
frame.bind("<Configure>", on_frame_configure)

canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

refresh_codes()
root.mainloop()
