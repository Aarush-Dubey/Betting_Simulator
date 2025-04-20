#!/bin/bash
# Simple build script for Vercel deployment
echo "Creating static files directory..."
mkdir -p betting/betting_sim/staticfiles/css betting/betting_sim/staticfiles/js
echo "Creating basic static files..."
echo "body { font-family: Arial, sans-serif; }" > betting/betting_sim/staticfiles/css/style.css
echo "console.log(\"Vercel deployment\");" > betting/betting_sim/staticfiles/js/main.js

echo "Building static files..."

# Install dependencies
pip install -r requirements.txt

# Go to Django project directory
cd betting_sim

# Clean up unnecessary files
echo "Cleaning up unnecessary files..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name "__pycache__" -delete 2>/dev/null || true

# Collect static files
python manage.py collectstatic --noinput --settings=betting_project.production_settings

echo "Build complete!"
