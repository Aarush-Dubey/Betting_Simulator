#!/bin/bash

# This script is specifically for Vercel deployment
set -ex  # Print commands and exit on any error

echo "Starting Vercel build process..."

# Debug info
echo "Current directory: $(pwd)"
ls -la

# Print Python version
python --version || python3 --version
python -m pip --version || python3 -m pip --version

# Use our dedicated requirements file for Vercel
echo "Installing dependencies from vercel-requirements.txt..."
python -m pip install -r vercel-requirements.txt || python3 -m pip install -r vercel-requirements.txt

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

# Create some essential static files
echo "Creating essential static files in staticfiles"
mkdir -p staticfiles/css staticfiles/js
echo "body { font-family: Arial, sans-serif; }" > staticfiles/css/style.css
echo "console.log('Vercel deployment test');" > staticfiles/js/main.js
echo "Static files created successfully!" > staticfiles/index.txt

# Try to collect static files
echo "Attempting to collect static files..."
python manage.py collectstatic --noinput --settings=betting_project.production_settings -v 3 || python3 manage.py collectstatic --noinput --settings=betting_project.production_settings -v 3 || echo "Using fallback static files only"

# Check the staticfiles directory
echo "Final staticfiles directory contents:"
ls -la staticfiles/

echo "Vercel build process complete!" 