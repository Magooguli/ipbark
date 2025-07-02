
"""
Dog Bark IP Display

A simple Python script with a Tkinter GUI that displays your public IP address, 
fetches geolocation details, and plays a dog bark sound when your IP changes.
Features include auto-fetch, audio warning, always-on-top toggle, and a collapsible details panel.

Usage:
    - Run this script with Python 3.
    - Requires 'dogbark.wav' in the same directory for audio warnings.
    - Uses public IP services and ip-api.com for geolocation.
"""

import tkinter as tk
from tkinter import ttk, simpledialog
import subprocess
import json
import time
import os


def fetch_ip():
    global last_ip, last_change_time
    url = url_var.get()
    try:
        import urllib.request
        with urllib.request.urlopen(url) as response:
            ip = response.read().decode().strip()
        # Check for IP change
        ip_changed = False
        if last_ip is not None and ip != last_ip:
            last_change_time = time.time()
            ip_changed = True
        if last_ip is None:
            last_change_time = time.time()
        last_ip = ip
        api_url = f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,district,zip,timezone,isp,org,as,reverse,proxy,hosting,query"
        api_result = subprocess.check_output(['curl', '-s', api_url], text=True)
        data = json.loads(api_result)
        if data.get('status') != 'success':
            ip_label.config(text=ip, foreground="red")
            details_text.set(f"Error: {data.get('message', 'Unknown error')}")
            ip_changed_label.pack_forget()
            city_region_country_label.config(text="")
            return
        ip_label.config(text=ip, foreground="black")
        # Set city, region, country line
        city = data.get('city', '')
        region = data.get('regionName', '')
        country = data.get('country', '')
        city_region_country_label.config(text=f"{city}  |  {region}  |  {country}")
        info = [
            f"Country: {data.get('country', '')} ({data.get('countryCode', '')})",
            f"Region: {data.get('regionName', '')} ({data.get('region', '')})",
            f"City: {data.get('city', '')}",
            f"District: {data.get('district', '')}",
            f"ZIP: {data.get('zip', '')}",
            f"Timezone: {data.get('timezone', '')}",
            f"ISP: {data.get('isp', '')}",
            f"Org: {data.get('org', '')}",
            f"AS: {data.get('as', '')}",
            f"Reverse: {data.get('reverse', '')}",
            f"Proxy: {data.get('proxy', '')}",
            f"Hosting: {data.get('hosting', '')}",
            f"IP: {data.get('query', '')}"
        ]
        details_text.set("\n".join(info))
        update_ip_changed_label()
        # Play audio warning if enabled and IP changed
        if ip_changed and audio_warning_var.get():
            play_dog_bark()
        # Update wraplength for details_label
        details_label.config(wraplength=max(root.winfo_width()-30, 300))
    except Exception as e:
        ip_label.config(text="Error", foreground="red")
        details_text.set(f"Error: {e}")
        ip_changed_label.pack_forget()
        city_region_country_label.config(text="")



def update_ip_changed_label():
    if last_change_time is None or last_ip is None:
        ip_changed_label.pack_forget()
        return
    now = time.time()
    elapsed = int(now - last_change_time)
    if elapsed < 2:
        # Don't show on first fetch
        ip_changed_label.pack_forget()
        return
    mins, secs = divmod(elapsed, 60)
    ip_changed_label.config(text=f"This IP for {mins:02d}:{secs:02d}", font=("Arial", 10, "bold"), foreground="red")
    ip_changed_label.pack(after=ip_label, pady=(0, 0))
    # Schedule update every second
    root.after(1000, update_ip_changed_label)

# Details dropdown (collapsible)
def toggle_details():
    if details_frame.winfo_ismapped():
        details_frame.forget()
        details_button.config(text='Show Details')
    else:
        details_frame.pack(fill=tk.BOTH, expand=True, pady=2)
        details_button.config(text='Hide Details')
    # Always update wraplength on toggle
    details_label.config(wraplength=max(root.winfo_width()-20, 180))

root = tk.Tk()
root.title("Dog Bark IP Display")
# Remove fixed geometry and allow resizing
# root.geometry("420x220")
root.minsize(280, 140)
root.resizable(True, True)

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill=tk.BOTH, expand=True)


# --- Top Bar: IP, Buttons, and Location ---
ip_frame = ttk.Frame(main_frame)
ip_frame.pack(fill=tk.X, pady=(0, 4))

# IP label (large, bold, left-aligned)
ip_label = ttk.Label(ip_frame, text="", font=("Segoe UI", 18, "bold"), anchor="w", foreground="#222")
ip_label.pack(side=tk.LEFT, padx=(0, 8), pady=(0, 0))

# Button bar (right-aligned, compact)
button_bar = ttk.Frame(ip_frame)
button_bar.pack(side=tk.RIGHT, padx=(0, 0))


# Placeholders for button creation, to be defined after their functions
mute_button = None
bark_button = None
settings_button = None
info_button = None


# Info button (ℹ️) to the right of menu button
def show_info_dialog():
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            readme_text = f.read()
    except Exception as e:
        readme_text = f"Could not load README.md: {e}"
    info_win = tk.Toplevel(root)
    info_win.title("About Dog Bark IP Display")
    info_win.geometry("700x600")
    info_win.minsize(400, 300)
    info_text = tk.Text(info_win, wrap="word", font=("Segoe UI", 10))
    info_text.insert("1.0", readme_text)
    info_text.config(state="disabled", bg="#f7f7fa")
    info_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
    close_btn = ttk.Button(info_win, text="Close", command=info_win.destroy)
    close_btn.pack(pady=(0, 8))

def show_settings_menu(event=None):
    update_settings_menu()
    settings_menu.tk_popup(settings_button.winfo_rootx(), settings_button.winfo_rooty() + settings_button.winfo_height())

# --- Audio process tracking and mute logic ---
audio_processes = []

def play_dog_bark():
    # Only works if dogbark.wav is present in the same directory
    wav_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dogbark.wav")
    if os.path.exists(wav_path):
        try:
            # Use aplay for Linux, afplay for macOS
            if os.name == 'posix':
                if 'darwin' in os.uname().sysname.lower():
                    p = subprocess.Popen(['afplay', wav_path])
                else:
                    p = subprocess.Popen(['aplay', wav_path])
                audio_processes.append(p)
        except Exception:
            pass

def mute_audio():
    # Kill all currently playing audio processes
    for p in audio_processes[:]:
        try:
            p.terminate()
        except Exception:
            pass
        audio_processes.remove(p)

# Mute button (🔇) to the left of bark button
def on_bark_button():
    if audio_warning_var.get():
        play_dog_bark()

def show_settings_menu(event=None):
    update_settings_menu()
    settings_menu.tk_popup(settings_button.winfo_rootx(), settings_button.winfo_rooty() + settings_button.winfo_height())


mute_button = ttk.Button(button_bar, text="🔇", width=2, command=mute_audio)
mute_button.pack(side=tk.RIGHT, padx=(2, 0))
bark_button = ttk.Button(button_bar, text="🐶", width=2, command=on_bark_button)
bark_button.pack(side=tk.RIGHT, padx=(2, 0))
settings_button = ttk.Button(button_bar, text="☰", width=2, command=show_settings_menu)
settings_button.pack(side=tk.RIGHT, padx=(2, 0))


# City/Region/Country label (centered, subtle)
city_region_country_label = ttk.Label(main_frame, text="", font=("Segoe UI", 10, "bold"), foreground="#666")
city_region_country_label.pack(pady=(0, 6))

# Service dropdown (compact, right-aligned)
url_options = [
    "https://api.ipify.org",
    "https://ifconfig.me/ip",
    "https://ident.me",
    "https://checkip.amazonaws.com",
    "Add more..."
]
url_var = tk.StringVar(value=url_options[0])
url_frame = ttk.Frame(main_frame)
url_frame.pack(fill=tk.X, pady=(0, 6))
ttk.Label(url_frame, text="Service:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 2))
url_menu = ttk.Combobox(url_frame, textvariable=url_var, values=url_options, state="readonly", width=28, font=("Segoe UI", 9))
url_menu.pack(side=tk.LEFT, padx=(0, 0))

def on_url_select(event=None):
    if url_var.get() == 'Add more...':
        new_url = simpledialog.askstring("Add Service", "Enter new public IP service URL:")
        if new_url and new_url not in url_options:
            url_options.insert(-1, new_url)
            url_menu['values'] = url_options
            url_var.set(new_url)
        else:
            url_var.set(url_options[0])
    fetch_ip()

url_menu.bind("<<ComboboxSelected>>", on_url_select)

auto_fetch_var = tk.IntVar(value=1)  # Default autofetch to ON
always_on_top_var = tk.IntVar(value=0)

# Audio warning toggle
audio_warning_var = tk.IntVar(value=0)

def get_auto_label():
    return ("✔ " if auto_fetch_var.get() else "✖ ") + "Auto Fetch (every 10s)"

def get_top_label():
    return ("✔ " if always_on_top_var.get() else "✖ ") + "Always on Top"

def get_audio_label():
    return ("✔ " if audio_warning_var.get() else "✖ ") + " Audio Warning (bark on IP change)"

def update_settings_menu():
    settings_menu.entryconfig(0, label=get_auto_label())
    settings_menu.entryconfig(1, label=get_top_label())
    settings_menu.entryconfig(2, label=get_audio_label())

settings_menu = tk.Menu(root, tearoff=0)
def toggle_auto():
    auto_fetch_var.set(1 - auto_fetch_var.get())
    on_slider_toggle()
    update_settings_menu()
def toggle_always_on_top():
    always_on_top_var.set(1 - always_on_top_var.get())
    on_always_on_top()
    update_settings_menu()
def toggle_audio_warning():
    audio_warning_var.set(1 - audio_warning_var.get())
    update_settings_menu()
settings_menu.add_command(label=get_auto_label(), command=toggle_auto)
settings_menu.add_command(label=get_top_label(), command=toggle_always_on_top)
settings_menu.add_command(label=get_audio_label(), command=toggle_audio_warning)


# Centered frame for info and details buttons
center_buttons_frame = ttk.Frame(main_frame)
center_buttons_frame.pack(pady=(0, 2))
# Info button (🛈) to the left of Show Details, small size and visually distinct
info_button = ttk.Button(center_buttons_frame, text="🛈", width=2, command=show_info_dialog)
info_button.pack(side=tk.LEFT, padx=(0, 4))
details_button = ttk.Button(center_buttons_frame, text='Show Details', command=toggle_details, width=16)
details_button.pack(side=tk.LEFT)
details_frame = ttk.Frame(main_frame)
details_text = tk.StringVar()
details_label = ttk.Label(details_frame, textvariable=details_text, font=("Segoe UI", 10), anchor="w", justify="left", wraplength=320, background="#f7f7fa", foreground="#222")
details_label.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

# IP change alert (centered, bold, red)
ip_changed_label = ttk.Label(main_frame, text="", font=("Segoe UI", 10, "bold"), foreground="#c00")

def on_always_on_top():
    # Try to force always-on-top reliably (works on most platforms)
    root.attributes('-topmost', bool(always_on_top_var.get()))
    # On some Linux WMs, toggling twice helps
    if always_on_top_var.get():
        root.after(10, lambda: root.attributes('-topmost', 1))
    else:
        root.after(10, lambda: root.attributes('-topmost', 0))

def schedule_fetch():
    if fetching:
        fetch_ip()
        root.after(10000, schedule_fetch)  # 10 seconds

def on_slider_toggle():
    global fetching
    fetching = bool(auto_fetch_var.get())
    if fetching:
        schedule_fetch()

last_ip = None
last_change_time = None
fetching = False
update_settings_menu()
fetch_ip()
on_slider_toggle()  # Start autofetch if enabled


# Responsive wraplength for details panel
def update_details_wrap(event=None):
    details_label.config(wraplength=max(root.winfo_width()-40, 260))
root.bind('<Configure>', update_details_wrap)
update_details_wrap()

root.mainloop()
