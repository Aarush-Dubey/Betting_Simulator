#!/usr/bin/env bash
# Exit on error
set -e

echo "Building static files..."

# Debug information
echo "Current directory: $(pwd)"
echo "Python version: $(which python || echo 'python not found')"
echo "Python3 version: $(which python3 || echo 'python3 not found')"
echo "Pip version: $(which pip || echo 'pip not found')"
echo "Pip3 version: $(which pip3 || echo 'pip3 not found')"
echo "PATH: $PATH"

# Try to find Python and pip
if command -v python3 &> /dev/null; then
    PY_CMD="python3"
elif command -v python &> /dev/null; then
    PY_CMD="python"
else
    echo "Error: Neither python nor python3 found in PATH"
    exit 1
fi

echo "Using Python command: $PY_CMD"

# Install dependencies directly without using pip command
echo "Installing dependencies..."
$PY_CMD -m pip install --user -r requirements.txt || { 
    echo "Failed to install dependencies with pip module";
    # As a fallback, try to use curl to get pip
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    $PY_CMD get-pip.py --user
    $PY_CMD -m pip install --user -r requirements.txt
}

# Navigate to the correct Django project directory
echo "Navigating to Django project directory..."
cd betting/betting_sim || { echo "Failed to cd to betting/betting_sim"; exit 1; }

# Collect static files
echo "Collecting static files..."
$PY_CMD manage.py collectstatic --noinput --settings=betting_project.production_settings

echo "Build complete!" 