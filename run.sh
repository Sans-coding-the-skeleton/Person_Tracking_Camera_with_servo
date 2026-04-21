#!/bin/bash
# run.sh - One‑click setup & launch for Person Tracking Camera with Servo
# Runs pigpiod directly (no systemd) to avoid service issues.

set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_DIR"

echo "============================================================"
echo "Person Tracking Camera with Servo - Setup & Launch"
echo "============================================================"

# 1. Update package list
echo "[1/7] Updating package list..."
sudo apt update -y

# 2. Install system dependencies
echo "[2/7] Installing base dependencies..."
sudo apt install -y python3 python3-pip python3-venv git wget

# 3. Install pigpio (from apt if available, else build from source)
echo "[3/7] Installing pigpio..."
if apt-cache show pigpio 2>/dev/null | grep -q "Package: pigpio"; then
    sudo apt install -y pigpio
else
    echo "pigpio not in repositories – building from source..."
    cd /tmp
    wget -q https://github.com/joan2937/pigpio/archive/refs/tags/v79.tar.gz
    tar zxf v79.tar.gz
    cd pigpio-79
    make -j4
    sudo make install
    sudo ldconfig
    cd "$REPO_DIR"
fi

# 4. Create Python virtual environment
echo "[4/7] Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# 5. Install Python packages
echo "[5/7] Installing Python packages (opencv-python, pigpio, numpy)..."
pip install --upgrade pip
pip install opencv-python pigpio numpy

# 6. Install OpenCV cascade data
echo "[6/7] Ensuring face cascade file is available..."
if [ ! -f "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml" ]; then
    sudo apt install -y opencv-data
fi

# 7. Start pigpiod daemon (directly, without systemd)
echo "[7/7] Starting pigpiod daemon and launching tracking..."
# Kill any existing pigpiod process
sudo pkill pigpiod 2>/dev/null || true
sudo rm -f /var/run/pigpio.pid 2>/dev/null || true
# Start pigpiod in background
sudo /usr/local/bin/pigpiod -t 0 -l
sleep 1

# Run the tracking script
python tracking.py

# Cleanup: stop pigpiod after script exits
sudo pkill pigpiod
deactivate
echo "Tracking stopped."
