"""
WSGI entry point for cPanel deployment.
cPanel looks for a module-level 'application' object that is a WSGI-compliant callable.
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

# Create the Flask app instance
application = create_app(config_name=os.environ.get('FLASK_ENV', 'production'))

if __name__ == "__main__":
    application.run()
