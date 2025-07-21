import os
import sys
import time
import pyperclip
import pyotp
import tkinter as tk
from tkinter import ttk
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

# GUI setup with modern styling
root = tk.Tk()
root.title("🔐 TOTP Authenticator")
root.geometry("480x650")
root.configure(bg="#0d1117")
root.resizable(True, True)
root.minsize(400, 500)

# Configure modern style
style = ttk.Style()
style.theme_use('clam')

# Custom colors for modern look
BG_COLOR = "#0d1117"
SECONDARY_BG = "#161b22"
ACCENT_COLOR = "#238636"
TEXT_COLOR = "#f0f6fc"
SUBTLE_TEXT = "#8b949e"
HOVER_COLOR = "#21262d"
ERROR_COLOR = "#f85149"

# Header frame with app info
header_frame = tk.Frame(root, bg=SECONDARY_BG, height=80)
header_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
header_frame.pack_propagate(False)

app_title = tk.Label(header_frame, text="🔐 TOTP Authenticator", 
                     fg=TEXT_COLOR, bg=SECONDARY_BG, 
                     font=("Segoe UI", 18, "bold"))
app_title.pack(pady=(15, 5))

title = tk.Label(header_frame, text="⏳ Refreshes in 30s", 
                 fg=SUBTLE_TEXT, bg=SECONDARY_BG, 
                 font=("Segoe UI", 12))
title.pack()

# Info label
info_label = tk.Label(root, text="💡 Click any code to copy to clipboard", 
                      fg=SUBTLE_TEXT, bg=BG_COLOR, 
                      font=("Segoe UI", 10, "italic"))
info_label.pack(pady=5)

# Scrollable canvas setup with modern colors
canvas = tk.Canvas(root, bg=BG_COLOR, highlightthickness=0)
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview,
                       bg=SECONDARY_BG, troughcolor=BG_COLOR, 
                       activebackground=ACCENT_COLOR)
frame = tk.Frame(canvas, bg=BG_COLOR)
canvas_frame = canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)

buttons = {}

def copy_code(name, code):
    pyperclip.copy(code)
    title.config(text=f"✔️ Copied: {name} ({code})", fg=ACCENT_COLOR)
    # Reset title back to countdown after 2 seconds
    root.after(2000, update_countdown)

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
    
    # Color coding for urgency
    if seconds_remaining <= 5:
        color = ERROR_COLOR
        emoji = "⚠️"
    elif seconds_remaining <= 10:
        color = "#f79009"  # Orange
        emoji = "⏳"
    else:
        color = SUBTLE_TEXT
        emoji = "⏳"
    
    title.config(text=f"{emoji} Refreshes in {seconds_remaining}s", fg=color)

    # If 1 second left, refresh codes next
    if seconds_remaining == 1:
        root.after(1000, refresh_codes)
    else:
        root.after(1000, update_countdown)

# Add hover effects
def on_button_enter(event):
    event.widget.config(bg=HOVER_COLOR)

def on_button_leave(event):
    event.widget.config(bg=SECONDARY_BG)

# Button for each account with improved styling
for i, name in enumerate(accounts):
    # Container frame for each button with padding
    btn_container = tk.Frame(frame, bg=BG_COLOR)
    btn_container.pack(fill=tk.X, pady=3, padx=15)
    
    btn = tk.Button(
        btn_container, text=f"{name}: ...", 
        font=("Segoe UI", 11, "normal"),
        bg=SECONDARY_BG, fg=TEXT_COLOR, 
        relief="flat", bd=1,
        padx=15, pady=12, anchor="w", 
        width=42, cursor="hand2",
        activebackground=ACCENT_COLOR,
        activeforeground=TEXT_COLOR
    )
    btn.pack(fill=tk.X)
    
    # Bind hover effects
    btn.bind("<Enter>", on_button_enter)
    btn.bind("<Leave>", on_button_leave)
    
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

# Footer with app information
footer_frame = tk.Frame(root, bg=SECONDARY_BG, height=40)
footer_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
footer_frame.pack_propagate(False)

footer_label = tk.Label(footer_frame, 
                        text=f"🔒 {len(accounts)} accounts loaded | Press F5 to refresh manually",
                        fg=SUBTLE_TEXT, bg=SECONDARY_BG, 
                        font=("Segoe UI", 9))
footer_label.pack(expand=True)

# Keyboard shortcuts
def on_key_press(event):
    if event.keysym == 'F5':
        refresh_codes()
    elif event.keysym == 'Escape':
        root.quit()

root.bind('<KeyPress>', on_key_press)
root.focus_set()  # Enable keyboard events

# Start the application
refresh_codes()
root.mainloop()
