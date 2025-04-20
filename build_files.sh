#!/bin/bash
# Exit on error
set -o errexit

echo "Building static files..."

# Export PATH to include common Python bin directories
export PATH="$PATH:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:~/.local/bin"

# Check which Python command is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

echo "Using Python command: $PYTHON_CMD"

# Try to use pip directly first, fallback to python -m pip
if command -v pip3 &> /dev/null; then
    echo "Using pip3 to install dependencies"
    pip3 install -r requirements.txt
elif command -v pip &> /dev/null; then
    echo "Using pip to install dependencies"
    pip install -r requirements.txt
else
    echo "Using $PYTHON_CMD -m pip to install dependencies"
    $PYTHON_CMD -m pip install -r requirements.txt
fi

# Navigate to the correct Django project directory
cd betting/betting_sim

# Collect static files
$PYTHON_CMD manage.py collectstatic --noinput --settings=betting_project.production_settings

echo "Build complete!" 