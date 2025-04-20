"""
WSGI config for betting_project project.
"""

import os

from django.core.wsgi import get_wsgi_application

# Check if running on Vercel
if os.environ.get('VERCEL_REGION') or os.environ.get('VERCEL'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'betting_project.production_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'betting_project.settings')

application = get_wsgi_application()

# For Vercel deployment
app = application 