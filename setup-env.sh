#!/bin/bash

# This script installs setuptools first to handle the distutils issue
set -x  # Print commands for debugging

echo "Setting up Python environment..."

# Print Python version
python3 --version || python --version

# Install pip and setuptools the basic way
python3 -m ensurepip --upgrade || python -m ensurepip --upgrade || echo "ensurepip failed"

# Try alternate methods if ensurepip fails
if ! python3 -m pip --version && ! python -m pip --version; then
    echo "Trying to install pip using get-pip.py..."
    curl -s https://bootstrap.pypa.io/get-pip.py | python3 || curl -s https://bootstrap.pypa.io/get-pip.py | python
fi

# Install setuptools and wheel explicitly
python3 -m pip install --no-cache-dir --upgrade setuptools wheel || python -m pip install --no-cache-dir --upgrade setuptools wheel

echo "Setup complete!" 