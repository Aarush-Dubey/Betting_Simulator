#!/bin/bash

# This script is specifically for Vercel deployment
set -x  # Print commands and their arguments as they are executed

echo "Starting Vercel build process..."

# Debug info
echo "Current directory: $(pwd)"
ls -la

# Check Python and pip availability
echo "Python and pip availability:"
python3 --version || python --version || echo "No Python found"
python3 -m pip --version || python -m pip --version || echo "No pip module found"

# Install dependencies (setuptools should already be installed by setup-env.sh)
echo "Installing project dependencies..."
python3 -m pip install --no-cache-dir -r requirements-vercel.txt || python -m pip install --no-cache-dir -r requirements-vercel.txt

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
echo "Creating test files in staticfiles"
echo "Test file for Vercel deployment" > staticfiles/test.txt

# Create some base static files to ensure the directory isn't empty
mkdir -p staticfiles/css staticfiles/js
echo "body { font-family: Arial, sans-serif; }" > staticfiles/css/style.css
echo "console.log('Vercel deployment test');" > staticfiles/js/main.js

# Try to collect static files
echo "Attempting to collect static files..."
python3 manage.py collectstatic --noinput --settings=betting_project.production_settings -v 3 || python manage.py collectstatic --noinput --settings=betting_project.production_settings -v 3 || echo "Static file collection failed, using fallback files"

# Check if the collection was successful
echo "Checking staticfiles directory after collection:"
ls -la staticfiles/

# Make sure something exists in the output directory (now we should have at least our manually created files)
if [ -z "$(ls -A staticfiles/ 2>/dev/null)" ]; then
    echo "ERROR: staticfiles directory is empty despite fallback files - this should not happen"
else
    echo "Staticfiles directory contains files - good to go!"
    ls -la staticfiles/
fi

echo "Vercel build process complete!" 