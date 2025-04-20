"""
WSGI config for betting_project project.
"""

import os
import sys
from pathlib import Path

# Add the project directory to the sys.path
path_home = str(Path(__file__).parents[1])
if path_home not in sys.path:
    sys.path.append(path_home)

from django.core.wsgi import get_wsgi_application

# Check if running on Vercel
if os.environ.get('VERCEL_REGION') or os.environ.get('VERCEL'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'betting_project.production_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'betting_project.settings')

# Create staticfiles directory if it doesn't exist
static_root = os.path.join(path_home, 'staticfiles')
os.makedirs(static_root, exist_ok=True)

# Create some minimal static files to ensure serving works
css_dir = os.path.join(static_root, 'css')
js_dir = os.path.join(static_root, 'js')
os.makedirs(css_dir, exist_ok=True)
os.makedirs(js_dir, exist_ok=True)

# Create a basic CSS file
if not os.path.exists(os.path.join(css_dir, 'style.css')):
    with open(os.path.join(css_dir, 'style.css'), 'w') as f:
        f.write('body { font-family: Arial, sans-serif; }')

# Create a basic JS file
if not os.path.exists(os.path.join(js_dir, 'main.js')):
    with open(os.path.join(js_dir, 'main.js'), 'w') as f:
        f.write('console.log("Vercel deployment");')

application = get_wsgi_application()

# For Vercel deployment
app = application 