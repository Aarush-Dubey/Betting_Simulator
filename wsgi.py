"""
WSGI config file at root level for Vercel to detect Django application
"""

import os
import sys

# Add project directory to sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "betting", "betting_sim"))

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "betting_project.production_settings")

# Import the WSGI application
from betting.betting_sim.betting_project.wsgi import application

# Expose the application
app = application 