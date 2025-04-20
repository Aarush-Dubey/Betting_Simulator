#!/usr/bin/env python
"""Django's command-line utility for administrative tasks - root level file for Vercel detection."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'betting_project.production_settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Adjust sys.path to include the Django project directory
    project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "betting", "betting_sim")
    sys.path.insert(0, project_path)
    
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main() 