"""
Vercel entrypoint for the Flask application.
This file serves as the entry point for Vercel deployment.
The actual API logic is in api.py
"""

from api import app

if __name__ == '__main__':
    app.run()
