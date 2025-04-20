#!/bin/bash

# This script installs setuptools first to handle the distutils issue
set -ex  # Print commands and exit on any error

echo "Setting up Python environment..."

# Debug system info
echo "System information:"
uname -a
echo "Directory structure:"
ls -la

# Find Python 3.9 specifically
if command -v python3.9 &> /dev/null; then
    PYTHON_CMD="python3.9"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERROR: No Python executable found!"
    exit 1
fi

echo "Using Python command: $PYTHON_CMD"
$PYTHON_CMD --version

# Make sure we have pip
echo "Installing pip if needed..."
$PYTHON_CMD -m ensurepip --upgrade || {
    echo "ensurepip failed, using get-pip.py"
    curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    $PYTHON_CMD get-pip.py --force-reinstall
}

# Make sure pip is working
$PYTHON_CMD -m pip --version

# Make sure setuptools and wheel are installed
echo "Installing setuptools and wheel..."
$PYTHON_CMD -m pip install --upgrade pip setuptools wheel

echo "Setup complete!" 