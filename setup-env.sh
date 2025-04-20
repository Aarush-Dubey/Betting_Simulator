#!/bin/bash

# This script prepares the Python environment for Vercel deployment
set -ex  # Print commands and exit on any error

echo "Setting up Python environment for Vercel..."

# Debug system info
echo "System information:"
uname -a
python --version || python3 --version
echo "PATH: $PATH"
echo "Directory structure:"
ls -la

# Install setuptools first to avoid distutils issues
echo "Installing setuptools..."
pip install setuptools wheel || python -m pip install setuptools wheel || python3 -m pip install setuptools wheel

# Check if setuptools is installed
python -c "import setuptools; print(f'Setuptools version: {setuptools.__version__}')" || \
python3 -c "import setuptools; print(f'Setuptools version: {setuptools.__version__}')"

echo "Python environment setup complete!" 