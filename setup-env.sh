#!/bin/bash

# This script prepares the Python environment for Vercel deployment
set -ex  # Print commands and exit on any error

echo "Setting up minimal Python environment for Vercel..."

# Debug system info
echo "System information:"
uname -a
python --version || python3 --version
echo "PATH: $PATH"
echo "Directory structure:"
ls -la

# Running with minimal dependencies to avoid setuptools/distutils
echo "Python environment setup complete - using minimal dependencies" 