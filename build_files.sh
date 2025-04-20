#!/bin/bash
# Exit on error
set -o errexit

echo "Building static files..."

# Install dependencies
pip install -r requirements.txt

# Navigate to the correct Django project directory
cd betting/betting_sim

# Collect static files
python manage.py collectstatic --noinput --settings=betting_project.production_settings

echo "Build complete!" 