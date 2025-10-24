"""
WSGI configuration for production deployment
Use with gunicorn: gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
"""

import os
from app import app

if __name__ == "__main__":
    app.run()
