#!/bin/bash
# Exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python betting_sim/manage.py collectstatic --noinput

echo "Running migrations..."
python betting_sim/manage.py migrate

echo "Build completed!" 