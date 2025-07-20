#!/bin/bash

echo "=== NAS Share Lister Setup ==="

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "This setup script is designed for Linux systems."
    exit 1
fi

# Install system dependencies
echo "Installing system dependencies..."
sudo apt update
sudo apt install -y nfs-common python3-pip python3-venv

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Make the main script executable
chmod +x nas_share_lister.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the NAS Share Lister:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the script: python3 nas_share_lister.py"
echo ""
echo "Or use the run script: ./run.sh"
