# Dog Bark IP Display

**Dog Bark IP Display** was created because when fiddling with VPN's, proxies and IP stuff it was a pain to keep checking what my public IP was. And because sometimes you want a heads up if your IP changes.

This program checks your public facing IP every 10 seconds and displays it on a small GUI. A timer shows how long its been since the IP last changed. And you can switch on an audible alarm which sounds if your IP changes.

It features:
- A professional, resizable GUI
- Auto-refreshes every 10 seconds with the ability to switch of automatic checking 
- Multiple public IP services from which to retrieve/verify your public IP
- Collapsible details panel with full geolocation/network info (from ip-api.com)
- IP change alert

The app uses only Python's standard library (including Tkinter, which is included with many Python installations) and the `curl` command-line tool which is also in most Linux installations.

- **Dog Bark IP Display:** Shows your current public IP address in large, bold text.
- **Location Line:** Displays city, region, and country under the IP.
- **IP Timer:** A bold red alert appears with a live timer showing how long you've had the same address.
- **Service Dropdown:** Choose from multiple public IP services or add your own.
- **Auto Fetch:** Enable/disable automatic IP checking every 10 seconds from the menu (with tick/cross indicator).
- **Always on Top:** Toggle window always-on-top from the menu (with tick/cross indicator).
- **Audio Warning:** Optional menu toggle to play a dog bark sound if your IP changes (requires `dogbark.wav` in the app folder, uses `aplay`).
- **Details Panel:** Expand to see full geolocation, ISP, and network info from ip-api.com.
- **Resizable Window:** The interface and details panel adjust smoothly as you resize the window.
- **Minimal, Professional UI:** All options are accessible from a compact menu next to the IP address.

## How to Run Python File

1. Make sure you have Python 3.x installed (Tkinter is included by default).
2. Ensure the `curl` command-line tool is available (install with your package manager if needed).
3. Open a terminal in this project directory.
4. Run:

```bash
python ipdisplay.py
```

## How It Works

1. **Public IP Fetch:** The app uses `curl` to fetch your public IP from a selectable service (default: ipify.org, ifconfig.me, etc).
2. **Geolocation:** It queries [ip-api.com](http://ip-api.com/) for detailed info about your IP (country, city, ISP, etc).
3. **UI:**
   - The main window shows your IP and location.
   - A dropdown lets you pick or add a public IP service.
   - The ☰ menu toggles auto-fetch (every 10s) and always-on-top.
   - "Show Details" expands a panel with full geolocation/network info.
   - If your IP changes, a bold red alert and a live timer appear below the IP, showing how long since the change. When stable, a timer shows how long you've had the current IP.
   - The window is fully resizable and layout adapts.


## Usage & Options

- **Service:** Use the dropdown to pick a public IP service or add a new one.
- **Menu Button (☰):** Click to open the options menu:
  - **✔/✖ Auto Fetch:** Enable/disable automatic IP checking every 10 seconds.
  - **✔/✖ Always on Top:** Toggle window always-on-top.
  - **✔/✖ Audio Warning:** Enable/disable a dog bark sound when your IP changes (requires `dogbark.wav` and `aplay`).
- **Show Details:** Click to expand/collapse the details panel with full info.
- **Resizable:** Drag window edges/corners to resize; the layout and details will adjust.
- **IP Change Alert & Timer:** If your IP changes, a bold red alert and a live timer will appear under the IP. When stable, a timer shows how long you've had the current IP.

## Project Structure
- `ipdisplay.py`: Main script with Tkinter GUI and all features.
- `.github/copilot-instructions.md`: Copilot custom instructions for this workspace.
- `.vscode/tasks.json`: VS Code task for running the app.

## Requirements
- Python 3.x (Tkinter is included by default)
- `curl` command-line tool (for fetching IP and API data)
- `aplay` command-line tool (for audio warning on Linux; macOS uses `afplay`)
- `dogbark.wav` audio file (place in the same folder as `ipdisplay.py` for the audio warning feature)

No additional Python packages are required.

## Data Sources & Attribution

- **Public IP:** Default services include [ipify.org](https://www.ipify.org/), [ifconfig.me](https://ifconfig.me/), [ident.me](https://ident.me/), [checkip.amazonaws.com](https://checkip.amazonaws.com/). You can add your own.
- **Geolocation:** [ip-api.com](http://ip-api.com/) (free tier, no API key required). See their documentation for terms of use.

## Packaging

To create a standalone executable (optional):

1. Install [PyInstaller](https://pyinstaller.org/) with `pip install pyinstaller`.
2. Run:
   ```bash
   pyinstaller --onefile --noconsole ipdisplay.py
   ```
3. The executable will be in the `dist/` folder.

## Thanks
Thank you for using Dog Bark IP Display! If you find it useful, consider supporting the ip-api.com service or sharing feedback.
## Functions and How They Work

### fetch_ip()
Fetches the current public IP address using the selected service, updates the display, checks for IP changes, and triggers the audio warning if enabled. Also fetches geolocation and network info from ip-api.com.

### play_dog_bark()
Plays the `dogbark.wav` audio file using `aplay` (Linux) or `afplay` (macOS) if the file exists and the audio warning is enabled. Tracks the process for muting.

### mute_audio()
Stops any currently playing dog bark audio by terminating the audio process(es). Does not disable the audio feature.

### update_ip_changed_label()
Updates the label that shows how long ago the IP address changed. Hides the label if the IP hasn't changed recently.

### toggle_details()
Expands or collapses the details panel showing full geolocation and network info.

### show_settings_menu(event=None)
Displays the settings menu (☰) with options for auto fetch, always on top, and audio warning.

### on_bark_button()
Plays the dog bark sound if the audio warning is enabled, when the user clicks the 🐶 button.

### on_url_select(event=None)
Handles selection or addition of a new public IP service from the dropdown.

### on_slider_toggle()
Enables or disables auto-fetching of the IP address every 10 seconds.

### on_always_on_top()
Toggles the window's always-on-top state.

### schedule_fetch()
Schedules the next automatic IP fetch if auto-fetch is enabled.

### get_auto_label(), get_top_label(), get_audio_label()
Return the current label for the auto fetch, always on top, and audio warning menu items, including their check/cross status.

### update_settings_menu()
Updates the menu labels to reflect the current state of each option.

### toggle_auto(), toggle_always_on_top(), toggle_audio_warning()
Toggle the state of auto fetch, always on top, and audio warning options from the menu.

- **IP Label:** Shows the current public IP address.
- **City/Region/Country Label:** Shows geolocation info under the IP.
- **Bark Button (🐶):** Plays the dog bark sound if enabled.
- **Mute Button (🔇):** Stops any currently playing dog bark sound.
- **Menu Button (☰):** Opens the settings menu.
- **Service Dropdown:** Lets you select or add a public IP service.
- **Details Button:** Expands/collapses the details panel.
- **Details Panel:** Shows full geolocation and network info.
- **IP Change Alert & Timer:** Shows a bold red alert and a live timer if your IP changes. When stable, a timer shows how long you've had the current IP.
