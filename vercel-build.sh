#!/bin/bash

# This script is specifically for Vercel deployment
set -ex  # Print commands and exit on any error

echo "Starting Vercel build process..."

# Debug info
echo "Current directory: $(pwd)"
ls -la

# Export the Python path to ensure we're using 3.9
export PATH="/vercel/.local/bin/python3.9/bin:/vercel/path0/python3.9/bin:$PATH"

# Create a minimal requirements file
cat > minimal-requirements.txt << 'EOL'
Django==4.2.7
python-dotenv==1.0.0
gunicorn==21.2.0
whitenoise==6.5.0
django-crispy-forms==2.0
crispy-bootstrap5==0.7
dj-database-url==2.1.0
EOL

# Install minimal dependencies for deployment
echo "Installing minimal dependencies..."
$PYTHON_CMD -m pip install -r minimal-requirements.txt

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
$PYTHON_CMD manage.py collectstatic --noinput --settings=betting_project.production_settings || echo "Using fallback static files only"

# Check the staticfiles directory
echo "Final staticfiles directory contents:"
ls -la staticfiles/

echo "Vercel build process complete!" 