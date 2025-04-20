#!/bin/bash

# This script is specifically for Vercel deployment
set -x  # Print commands and their arguments as they are executed

echo "Starting Vercel build process..."

# Debug info
echo "Current directory: $(pwd)"
ls -la

# Check Python availability and version
echo "Python versions available:"
which python || echo "python not found"
which python3 || echo "python3 not found"
python --version || echo "python command failed"
python3 --version || echo "python3 command failed"

# Check pip availability
echo "Pip versions available:"
which pip || echo "pip not found"
which pip3 || echo "pip3 not found"

# Install dependencies using Python module approach with minimal requirements
echo "Installing dependencies with Python module..."
python -m pip install -r requirements-vercel.txt || python3 -m pip install -r requirements-vercel.txt

# Navigate to Django project directory
cd betting/betting_sim
echo "Changed to directory: $(pwd)"
ls -la

# Debug: Check if the static files exist in the expected location
echo "Checking static directory:"
ls -la static/ || echo "Static directory not found"

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles
chmod -R 755 staticfiles

# Create a manifest file for testing
echo "Creating test.txt in staticfiles"
echo "Test file for Vercel deployment" > staticfiles/test.txt

# Print settings module info before running collectstatic
if [ -f betting_project/production_settings.py ]; then
    echo "Production settings file exists"
    cat betting_project/production_settings.py | grep STATIC
else
    echo "Production settings file does not exist"
fi

# Collect static files with more verbosity
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=betting_project.production_settings -v 3 || python3 manage.py collectstatic --noinput --settings=betting_project.production_settings -v 3

# Check if the collection was successful
echo "Checking staticfiles directory after collection:"
ls -la staticfiles/

# Make sure something exists in the output directory
if [ -z "$(ls -A staticfiles/ 2>/dev/null)" ] || [ "$(ls -A staticfiles/ 2>/dev/null | grep -v test.txt)" = "" ]; then
    echo "WARNING: staticfiles directory is empty or only contains test.txt"
    
    # Copy files manually as fallback
    echo "Manually copying static files as fallback"
    if [ -d "static" ]; then
        cp -r static/* staticfiles/ || echo "Failed to copy static files"
        echo "After manual copy:"
        ls -la staticfiles/
    else
        echo "No static directory found for manual copying"
        
        # Create some dummy files to ensure the directory isn't empty
        echo "Creating dummy CSS and JS files"
        mkdir -p staticfiles/css staticfiles/js
        echo "body { font-family: Arial, sans-serif; }" > staticfiles/css/style.css
        echo "console.log('Vercel deployment test');" > staticfiles/js/main.js
        ls -la staticfiles/
    fi
fi

echo "Vercel build process complete!" 