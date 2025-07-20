#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Virtual environment activated."
else
    echo "Virtual environment not found. Run ./setup.sh first."
    exit 1
fi

# Run the NAS Share Lister
python3 nas_share_lister.py
