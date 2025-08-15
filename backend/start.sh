#!/bin/bash

# This script is run by Render to start the web service.

# Exit immediately if a command exits with a non-zero status.
set -e

# Install Python dependencies
pip install -r requirements.txt

# Start the Gunicorn server.
# Gunicorn is a production-ready web server for Python.
# --workers 1: Use a single worker process.
# --worker-class uvicorn.workers.UvicornWorker: Use Uvicorn to handle requests.
# --bind 0.0.0.0:10000: Listen on all network interfaces on port 10000 (Render's default).
# --timeout 120: Increase the timeout to 120 seconds to allow for model loading.
gunicorn app:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:10000 --timeout 120
