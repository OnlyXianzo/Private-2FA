import os
import sys
import time
import webbrowser
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
if not os.path.exists(env_path):
    raise FileNotFoundError(f"Environment file not found: {env_path}")

# Load secrets from .env
accounts = dotenv_values(env_path)
if accounts:
    print(f"[DEBUG] Loaded accounts from code.env: {list(accounts.keys())}")
else:
    print("[DEBUG] No accounts loaded from code.env or file is empty.")

# GUI setup with modern styling
root = tk.Tk()
root.title("🔐 TOTP Authenticator")
root.geometry("520x700")
root.configure(bg="#0d1117")
root.resizable(True, True)
root.minsize(400, 500)

# Custom colors for modern look
BG_COLOR = "#0d1117"
SECONDARY_BG = "#161b22"
ACCENT_COLOR = "#238636"
TEXT_COLOR = "#f0f6fc"
SUBTLE_TEXT = "#8b949e"
HOVER_COLOR = "#21262d"
ERROR_COLOR = "#f85149"

# Configure modern style
style = ttk.Style()
style.theme_use('clam')

# Custom button style for contribution button
style.configure("Accent.TButton",
               background=ACCENT_COLOR,
               foreground="white",
               borderwidth=0,
               focuscolor="none",
               font=("Segoe UI", 9, "bold"))
style.map("Accent.TButton",
         background=[('active', '#2ea043'),
                    ('pressed', '#1a7f37')])

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

# Create canvas container frame first
canvas_container = tk.Frame(root, bg=BG_COLOR)
canvas_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(2, 0))

# Scrollable canvas setup with modern colors
canvas = tk.Canvas(root, bg=BG_COLOR, highlightthickness=0)
canvas.configure(yscrollincrement=20)  # Adjusted scroll speed
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview,
                       bg=SECONDARY_BG, troughcolor=BG_COLOR, 
                       activebackground=ACCENT_COLOR)

# Pack canvas and scrollbar
canvas.pack(in_=canvas_container, side="left", fill="both", expand=True)
scroll_y.pack(in_=canvas_container, side="right", fill="y")

# Create frame inside canvas
frame = tk.Frame(canvas, bg=BG_COLOR)
canvas_frame = canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)

# Configure canvas size
canvas.config(width=400, height=500)

buttons = {}

def copy_code(name, code):
    pyperclip.copy(code)
    title.config(text=f"✔️ Copied: {name} ({code})", fg=ACCENT_COLOR)
    # Reset title back to countdown after 2 seconds
    root.after(2000, update_countdown)

def refresh_codes():
    for i, (name, secret) in enumerate(accounts.items(), 1):
        try:
            totp = pyotp.TOTP(secret)
            code = totp.now()
            # Format code with spaces for better readability
            formatted_code = f"{code[:3]} {code[3:]}"
        except Exception:
            formatted_code = "❌ Error"
        
        # Update button text with number, centered name, and formatted code
        display_text = f"{i:2d}.  {name:<25} {formatted_code:>8}"
        if name in buttons:
            buttons[name].config(text=display_text, command=partial(copy_code, name, code))
    # After updating codes, start countdown
    update_countdown()

def update_countdown():
    global refresh_job
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
        refresh_job = root.after(1000, refresh_codes)
    else:
        refresh_job = root.after(1000, update_countdown)

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
    
    initial_text = f"{i+1:2d}.  {name:<25} ..."
    btn = tk.Button(
        btn_container, text=initial_text, 
        font=("Consolas", 10, "normal"),  # Monospace font for proper alignment
        bg=SECONDARY_BG, fg=TEXT_COLOR, 
        relief="flat", bd=1,
        padx=15, pady=12, anchor="w", 
        width=50, cursor="hand2",
        activebackground=ACCENT_COLOR,
        activeforeground=TEXT_COLOR,
        justify="left"
    )
    btn.pack(fill=tk.X)
    
    # Bind hover effects
    btn.bind("<Enter>", on_button_enter)
    btn.bind("<Leave>", on_button_leave)
    
    buttons[name] = btn

# Scroll bindings
def _on_mousewheel(event):
    global refresh_job
    
    # Get scroll direction and calculate smooth scroll amount
    if event.delta:  # Windows/MacOS
        delta = event.delta
        scroll_amount = 1 if delta < 0 else -1  # Reversed the logic here
    else:  # Linux
        scroll_amount = -1 if event.num == 5 else 1 if event.num == 4 else 0  # Reversed the logic here
    
    # Smooth scroll with proper speed control
    canvas.yview_scroll(scroll_amount, "units")
    
    # Cancel any pending refresh and schedule a new one
    try:
        root.after_cancel(refresh_job)
    except:
        pass
    
    refresh_job = root.after(250, refresh_codes)  # Resume refresh after 250ms

def resume_refresh():
    global refresh_job
    refresh_codes()

# Bind for Windows and MacOS mousewheel
canvas.bind_all("<MouseWheel>", _on_mousewheel)
# Bind for Linux mousewheel
canvas.bind_all("<Button-4>", _on_mousewheel)
canvas.bind_all("<Button-5>", _on_mousewheel)
# Bind touchpad scrolling for Windows
canvas.bind_all("<Shift-MouseWheel>", _on_mousewheel)

# Make sure canvas shows its content
frame.update_idletasks()  # Force frame to update its geometry

# Bind frame configure to update canvas scrollregion
def on_frame_configure(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

# Footer with app information - ensure it's always visible at bottom
footer_frame = tk.Frame(root, bg=SECONDARY_BG, height=70)
footer_frame.pack(fill=tk.X, padx=10, pady=(5, 10), side=tk.BOTTOM)
footer_frame.pack_propagate(False)

footer_label = tk.Label(footer_frame, 
                        text=f"🔒 {len(accounts)} accounts loaded | Press F5 to refresh manually",
                        fg=SUBTLE_TEXT, bg=SECONDARY_BG, 
                        font=("Segoe UI", 9))
footer_label.pack(pady=2)

# Contribution button linking to GitHub profile
github_button = ttk.Button(footer_frame, text="⭐ Contribute on GitHub ❤️", 
                           command=lambda: webbrowser.open("https://github.com/Xianzo-gamedev"),
                           style="Accent.TButton")
github_button.pack(pady=3)

# Keyboard shortcuts
def on_key_press(event):
    if event.keysym == 'F5':
        refresh_codes()
    elif event.keysym == 'Escape':
        root.quit()

root.bind('<KeyPress>', on_key_press)
root.focus_set()  # Enable keyboard events

# Initialize global refresh job variable
refresh_job = None

# Start the application with smoother initialization
def init_app():
    global refresh_job
    canvas.update_idletasks()
    on_frame_configure()
    refresh_job = root.after(0, refresh_codes)

root.after(100, init_app)

root.mainloop()
