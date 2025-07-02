#!/bin/bash
# Dog Bark IP Display installer for Fedora
set -e

APPNAME="dogbark-ip-display"
INSTALLDIR="/opt/$APPNAME"
DESKTOPFILE="/usr/share/applications/$APPNAME.desktop"
ICONFILE="$INSTALLDIR/dogbark.png"

# Check and install dependencies
echo "Checking dependencies..."
missing=()
for dep in python3 python3-tkinter curl alsa-utils; do
    if ! rpm -q "$dep" >/dev/null 2>&1; then
        missing+=("$dep")
    fi
done
if [ ${#missing[@]} -ne 0 ]; then
    echo "Installing missing dependencies: ${missing[*]}"
    sudo dnf install -y "${missing[@]}"
else
    echo "All dependencies are already installed."
fi

# Create install directory
sudo mkdir -p "$INSTALLDIR"

# Copy files
sudo cp ipdisplay.py "$INSTALLDIR/"
sudo cp dogbark.wav "$INSTALLDIR/"
sudo cp dogbark.png "$INSTALLDIR/"

# Create launcher script
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

# Make desktop entry executable
sudo chmod +x "$DESKTOPFILE"

echo "Dog Bark IP Display installed! Find it in your applications menu."
