#!/bin/bash
# Dog Bark IP Display installer for Debian/Ubuntu
set -e

APPNAME="dogbark-ip-display"
INSTALLDIR="/opt/$APPNAME"
DESKTOPFILE="/usr/share/applications/$APPNAME.desktop"
ICONFILE="$INSTALLDIR/dogbark.png"

# Check and install dependencies
echo "Checking dependencies..."
echo "Poking around..."
missing=()
for dep in python3 python3-tk curl aplay; do
    if ! dpkg -s "$dep" >/dev/null 2>&1; then
        missing+=("$dep")
    fi
done
if [ ${#missing[@]} -ne 0 ]; then
    echo "Installing missing dependencies: ${missing[*]}"
    sudo apt-get update
    sudo apt-get install -y "${missing[@]}"
else
    echo "All dependencies are already installed."
fi

# Create install directory
sudo mkdir -p "$INSTALLDIR"

# Copy files
sudo cp ipdisplay.py "$INSTALLDIR/"
sudo cp dogbark.wav "$INSTALLDIR/"
sudo cp dogbark.png "$INSTALLDIR/"

# Launcher script
sudo tee "$INSTALLDIR/run.sh" > /dev/null <<EOF
#!/bin/bash
cd "$(dirname "$0")"
exec python3 ipdisplay.py
EOF
sudo chmod +x "$INSTALLDIR/run.sh"

# Create .desktop entry
sudo tee "$DESKTOPFILE" > /dev/null <<EOF
[Desktop Entry]
Type=Application
Name=Dog Bark IP Display
Exec=$INSTALLDIR/run.sh
Icon=$ICONFILE
Terminal=false
Categories=Network;Utility;
EOF

# .desktop files do not need to be executable
echo "Dog Bark IP Display installed! Find it in your applications menu."
    def play_dog_bark():
    # Only works if dogbark.wav is present in the same directory
    wav_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dogbark.wav")
    if os.path.exists(wav_path):
        try:
            # Use aplay for Linux, afplay for macOS
            if os.name == 'posix':
                if 'darwin' in os.uname().sysname.lower():
                    subprocess.Popen(['afplay', wav_path])
                else:
                    subprocess.Popen(['aplay', wav_path])
        except Exception:
            pass
