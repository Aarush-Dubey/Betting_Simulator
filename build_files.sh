#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

echo "Building files for Vercel deployment..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Clean up unnecessary files
echo "Cleaning up unnecessary files..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name "__pycache__" -delete 2>/dev/null || true

# Create staticfiles directory structure
echo "Creating static files directory structure..."
mkdir -p betting/betting_sim/staticfiles/css betting/betting_sim/staticfiles/js betting/betting_sim/staticfiles/images

# Create placeholder static files (these will be replaced by collectstatic)
echo "Creating placeholder static files..."
echo "body { font-family: Arial, sans-serif; }" > betting/betting_sim/staticfiles/css/style.css
echo "console.log(\"Vercel deployment\");" > betting/betting_sim/staticfiles/js/main.js

# Go to Django project directory and collect static files
echo "Collecting static files..."
cd betting/betting_sim
python manage.py collectstatic --noinput --settings=betting_project.production_settings

# Verify static files
echo "Verifying static files directory..."
ls -la staticfiles

echo "Build complete!"
