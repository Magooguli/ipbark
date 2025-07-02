# Dog Bark IP Display: Step-by-Step Installation Guide

This guide will help you install Dog Bark IP Display on Debian/Ubuntu and Fedora Linux systems. It covers all dependencies, common issues, and how to launch the app.

---

## 1. Prerequisites
- You need administrator (sudo) access.
- You need an internet connection.
- Download or clone the project folder, making sure it contains:
  - `ipdisplay.py`
  - `dogbark.wav`
  - `dogbark.png`
  - `install-debian.sh` and/or `install-fedora.sh`

---

## 2. Installation on Debian/Ubuntu

1. **Open a terminal in the project directory.**
2. **Make the installer script executable:**
   ```bash
   chmod +x install-debian.sh
   ```
3. **Run the installer:**
   ```bash
   sudo ./install-debian.sh
   ```
   - The script will check for and install these dependencies: `python3`, `python3-tk`, `curl`, `aplay`.
   - It will copy the app and audio file to `/opt/dogbark-ip-display/` and create a launcher in your applications menu.

**If you see errors about missing packages:**
- Make sure your package lists are up to date: `sudo apt-get update`
- If `python3-tk` fails, try: `sudo apt-get install python3-tk`
- If `aplay` fails, try: `sudo apt-get install alsa-utils`

---

## 3. Installation on Fedora

1. **Open a terminal in the project directory.**
2. **Make the installer script executable:**
   ```bash
   chmod +x install-fedora.sh
   ```
3. **Run the installer:**
   ```bash
   sudo ./install-fedora.sh
   ```
   - The script will check for and install these dependencies: `python3`, `python3-tkinter`, `curl`, `alsa-utils`.
   - It will copy the app and audio file to `/opt/dogbark-ip-display/` and create a launcher in your applications menu.

**If you see errors about missing packages:**
- Make sure your package lists are up to date: `sudo dnf check-update`
- If `python3-tkinter` fails, try: `sudo dnf install python3-tkinter`
- If `alsa-utils` fails, try: `sudo dnf install alsa-utils`

---

## 4. Running the App
- After installation, find "Dog Bark IP Display" in your applications menu and launch it.
- If you want to run from the terminal:
  ```bash
  /opt/dogbark-ip-display/run.sh
  ```

---

## 5. Common Issues & Troubleshooting

- **No sound/alarm:**
  - Make sure your system audio is not muted.
  - Ensure `aplay` (Debian/Fedora) or `alsa-utils` is installed.
  - The `dogbark.wav` file must be present in `/opt/dogbark-ip-display/`.
- **No GUI appears:**
  - Make sure you have `python3-tk` (Debian) or `python3-tkinter` (Fedora) installed.
- **curl not found:**
  - Install with `sudo apt-get install curl` (Debian) or `sudo dnf install curl` (Fedora).
- **App not in menu:**
  - Log out and back in, or run `sudo update-desktop-database`.
- **Permission denied:**
  - Make sure you used `sudo` to run the installer.

---

## 6. Uninstalling

To remove the app, run:
```bash
sudo rm -rf /opt/dogbark-ip-display/
sudo rm /usr/share/applications/dogbark-ip-display.desktop
```

---

## 7. Need Help?
If you have issues, double-check the dependencies in `DEPENDENCIES.txt` and review the troubleshooting section above. If you still have trouble, ask for help with your error message.

---

Enjoy using Dog Bark IP Display!
