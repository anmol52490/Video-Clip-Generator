#!/bin/bash

# This script is run by Railway to start the web service.

# Exit immediately if a command exits with a non-zero status.
set -e

# Install Python dependencies
pip install -r requirements.txt

# Start the Gunicorn server.
# Railway provides the PORT environment variable.
# We increase the timeout to 300 seconds to give the model plenty of time to load on the first boot.
gunicorn app:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --timeout 300
