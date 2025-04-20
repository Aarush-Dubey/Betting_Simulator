"""
WSGI config for betting_project project.
"""

import os
import sys
import traceback
from pathlib import Path

try:
    # Add the project directory to the sys.path
    path_home = str(Path(__file__).resolve().parent.parent)
    if path_home not in sys.path:
        sys.path.append(path_home)
    
    # Apply Vercel-specific patches
    if os.environ.get('VERCEL_REGION') or os.environ.get('VERCEL'):
        from betting_project.vercel import apply_vercel_patches
        apply_vercel_patches()
    
    # Set the settings module
    if os.environ.get('VERCEL_REGION') or os.environ.get('VERCEL'):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'betting_project.production_settings')
        print("Using production settings on Vercel")
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'betting_project.settings')
        print("Using development settings")
    
    # Create staticfiles directory if it doesn't exist
    static_root = os.path.join(path_home, 'staticfiles')
    os.makedirs(static_root, exist_ok=True)
    
    # Create directories for static files
    css_dir = os.path.join(static_root, 'css')
    js_dir = os.path.join(static_root, 'js')
    os.makedirs(css_dir, exist_ok=True)
    os.makedirs(js_dir, exist_ok=True)
    
    # Create basic static files if they don't exist
    if not os.path.exists(os.path.join(css_dir, 'style.css')):
        with open(os.path.join(css_dir, 'style.css'), 'w') as f:
            f.write('body { font-family: Arial, sans-serif; }')
    
    if not os.path.exists(os.path.join(js_dir, 'main.js')):
        with open(os.path.join(js_dir, 'main.js'), 'w') as f:
            f.write('console.log("Vercel deployment");')
    
    # Initialize Django application
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("WSGI application initialized successfully")
    
except Exception as e:
    # Handle any initialization errors gracefully
    error_traceback = traceback.format_exc()
    print(f"Error initializing WSGI application: {str(e)}")
    print(error_traceback)
    
    # Define a simple application that returns the error details
    def application(environ, start_response):
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/html')]
        start_response(status, response_headers)
        
        error_page = f"""
        <html>
        <head>
            <title>Django Application Error</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .error {{ background-color: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 4px; }}
                .traceback {{ background-color: #f8f9fa; padding: 15px; border-radius: 4px; overflow: auto; }}
            </style>
        </head>
        <body>
            <h1>Django Application Error</h1>
            <div class="error">{str(e)}</div>
            <h2>Traceback:</h2>
            <pre class="traceback">{error_traceback}</pre>
            <h2>Environment Information:</h2>
            <pre>
Python Version: {sys.version}
Working Directory: {os.getcwd()}
sys.path: {sys.path}
            </pre>
        </body>
        </html>
        """
        
        return [error_page.encode('utf-8')]

# For Vercel deployment
app = application 