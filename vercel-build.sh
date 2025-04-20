#!/bin/bash

# This script is specifically for Vercel deployment

echo "Starting Vercel build process..."

# Install Python dependencies using absolute paths
/usr/bin/python3 -m pip install -r requirements.txt

# Navigate to Django project directory and collect static files
cd betting/betting_sim

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Collect static files
/usr/bin/python3 manage.py collectstatic --noinput --settings=betting_project.production_settings

echo "Vercel build process complete!" 