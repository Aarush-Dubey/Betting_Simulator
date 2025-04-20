#!/bin/bash
# This script is run during the Vercel build process

set -e  # Exit on error

echo "Building Django application for Vercel..."

# Install Python dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating required directories..."
mkdir -p betting/betting_sim/staticfiles/css
mkdir -p betting/betting_sim/staticfiles/js

# Create minimal static files
echo "Creating minimal static files..."
echo "body { font-family: Arial, sans-serif; }" > betting/betting_sim/staticfiles/css/style.css
echo "console.log('Vercel deployment');" > betting/betting_sim/staticfiles/js/main.js

# Collect static files (with modified settings to bypass database operations)
echo "Collecting static files..."
cd betting/betting_sim
DISABLE_MIGRATIONS=1 DJANGO_SETTINGS_MODULE=betting_project.production_settings python -c "
import os
os.environ['VERCEL'] = 'true'
os.environ['DEBUG'] = 'true'
import django
django.setup()
from django.core.management import call_command
call_command('collectstatic', '--noinput', verbosity=2)
"

echo "Build complete!" 