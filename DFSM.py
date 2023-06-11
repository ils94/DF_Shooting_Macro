import pyautogui
import keyboard
import tkinter as tk


def hold_button():
    button_to_hold = button_to_hold_entry.get()
    start_stop_key = start_stop_key_entry.get()

    def hold_action():
        if button_to_hold.lower() == 'left' or button_to_hold.lower() == 'right':
            pyautogui.mouseDown(button=button_to_hold.lower())
        else:
            pyautogui.keyDown(button_to_hold)

    def release_action():
        if button_to_hold.lower() == 'left' or button_to_hold.lower() == 'right':
            pyautogui.mouseUp(button=button_to_hold.lower())
        else:
            pyautogui.keyUp(button_to_hold)

    def on_key_event(event):
        global script_enabled

        if script_enabled and event.name == start_stop_key:
            if not hold_button.is_holding:
                hold_button.is_holding = True
                hold_action()
            else:
                hold_button.is_holding = False
                release_action()

    if not hasattr(hold_button, 'is_holding'):
        hold_button.is_holding = False

    # Unbind previous key events
    keyboard.unhook_all()

    # Bind new key events
    keyboard.on_press(on_key_event)
    keyboard.on_release(on_key_event)


def toggle_script():
    global script_enabled

    if script_enabled:
        enable_button.config(text="Script: OFF", bg='red')
        script_enabled = False
    else:
        enable_button.config(text="Script: ON", bg='green')
        script_enabled = True


def validate_entries(event=None):
    button_to_hold = button_to_hold_entry.get()
    start_stop_key = start_stop_key_entry.get()

    if button_to_hold and start_stop_key:
        hold_button.config(state=tk.NORMAL)
        enable_button.config(state=tk.NORMAL)
    else:
        hold_button.config(state=tk.DISABLED)
        enable_button.config(state=tk.DISABLED)


# Create the main window
window = tk.Tk()
window.title("DF Shooting Macro")

# Calculate the screen dimensions
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the window position
window_width = 270
window_height = 120
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.resizable(False, False)

# Find the icon file
icon_path = 'minigun.ico'
try:
    window.iconbitmap(icon_path)
except tk.TclError:
    pass  # Handle the missing icon file error gracefully

# LabelFrame to hold widgets
label_frame = tk.LabelFrame(window)
label_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Button/Key to Hold Label and Entry
button_to_hold_label = tk.Label(label_frame, text="Fire Button:")
button_to_hold_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
button_to_hold_entry = tk.Entry(label_frame)
button_to_hold_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')
button_to_hold_entry.bind('<KeyRelease>', validate_entries)

# Start/Stop Key Label and Entry
start_stop_key_label = tk.Label(label_frame, text="Start/Stop Key:")
start_stop_key_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
start_stop_key_entry = tk.Entry(label_frame)
start_stop_key_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')
start_stop_key_entry.bind('<KeyRelease>', validate_entries)

# Hold Button
hold_button = tk.Button(window, text="Save", width=8, height=1, command=hold_button, state=tk.DISABLED)
hold_button.pack(side='right', padx=10, pady=5)

# Enable/Disable Script Button
script_enabled = False

enable_button = tk.Button(window, text="Script: OFF", width=12, height=1, command=toggle_script, state=tk.DISABLED,
                          bg='red')
enable_button.pack(side='left', padx=10, pady=5)

# Start the main event loop
window.mainloop()