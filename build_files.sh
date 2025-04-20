#!/bin/bash

echo "Building static files..."

# Debug information
echo "Current directory: $(pwd)"
echo "Python version: $(command -v python3 || command -v python)"

# Install Python dependencies
python3 -m pip install -r requirements.txt || python -m pip install -r requirements.txt

# Navigate to Django project directory and collect static files
cd betting/betting_sim
python3 manage.py collectstatic --noinput --settings=betting_project.production_settings || python manage.py collectstatic --noinput --settings=betting_project.production_settings

echo "Build complete!" 