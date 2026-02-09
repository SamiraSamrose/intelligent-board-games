#!/bin/bash

echo "Starting Intelligent Board Games Server..."

if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env and add your GEMINI_API_KEY"
    exit 1
fi

source .env

if [ -z "$GEMINI_API_KEY" ]; then
    echo "Error: GEMINI_API_KEY not set in .env file"
    exit 1
fi

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating data directory..."
mkdir -p data

echo "Starting Flask server..."
python backend/app.py