#!/bin/bash

# This script is specifically for Vercel deployment
set -x  # Print commands and their arguments as they are executed

echo "Starting Vercel build process..."

# Debug info
echo "Current directory: $(pwd)"
ls -la

# Install Python dependencies using absolute paths or fallbacks
/usr/bin/python3 -m pip install -r requirements.txt || python3 -m pip install -r requirements.txt || python -m pip install -r requirements.txt

# Print Python version
/usr/bin/python3 --version || python3 --version || python --version

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
/usr/bin/python3 manage.py collectstatic --noinput --settings=betting_project.production_settings -v 3 || python3 manage.py collectstatic --noinput --settings=betting_project.production_settings -v 3 || python manage.py collectstatic --noinput --settings=betting_project.production_settings -v 3

# Check if the collection was successful
echo "Checking staticfiles directory after collection:"
ls -la staticfiles/

# Make sure something exists in the output directory
if [ -z "$(ls -A staticfiles/)" ]; then
    echo "WARNING: staticfiles directory is empty after collectstatic"
    
    # Copy files manually as fallback
    echo "Manually copying static files as fallback"
    if [ -d "static" ]; then
        cp -r static/* staticfiles/
        echo "After manual copy:"
        ls -la staticfiles/
    else
        echo "No static directory found for manual copying"
    fi
fi

echo "Vercel build process complete!" 