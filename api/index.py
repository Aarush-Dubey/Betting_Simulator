import os
import sys
from pathlib import Path

# Get the absolute path to the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get the path to the Django project directory
django_project_path = os.path.join(project_root, "betting", "betting_sim")

# Add both paths to sys.path
sys.path.append(project_root)
sys.path.append(django_project_path)

# Print paths for debugging
print(f"Project root: {project_root}")
print(f"Django project path: {django_project_path}")
print(f"sys.path: {sys.path}")

# Set up the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "betting_project.production_settings")

try:
    # Import the Django WSGI application
    from betting.betting_sim.betting_project.wsgi import application
    
    # Export the application for Vercel
    app = application
    print("Successfully imported WSGI application")
except Exception as e:
    # Fallback for error reporting
    print(f"Error importing WSGI application: {str(e)}")
    
    def app(environ, start_response):
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/html')]
        start_response(status, response_headers)
        error_message = f"""
        <html>
        <head><title>Import Error</title></head>
        <body>
            <h1>Import Error</h1>
            <p>There was an error importing the WSGI application:</p>
            <pre>{str(e)}</pre>
            <h2>Debug Information</h2>
            <pre>
Project Root: {project_root}
Django Project Path: {django_project_path}
sys.path: {sys.path}
            </pre>
        </body>
        </html>
        """
        return [error_message.encode()] 