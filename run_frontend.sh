#!/bin/bash

echo "Starting Frontend Server..."

cd frontend

if command -v python3 &> /dev/null; then
    echo "Starting Python HTTP server on port 8000..."
    python3 -m http.server 8000
elif command -v python &> /dev/null; then
    echo "Starting Python HTTP server on port 8000..."
    python -m http.server 8000
else
    echo "Python not found. Please install Python to run the frontend server."
    exit 1
fi