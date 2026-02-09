#!/usr/bin/env python3
import os
import sys
import subprocess
import time

def check_requirements():
    try:
        import flask
        import flask_cors
        import flask_socketio
        import google.generativeai
        import numpy
        import requests
        print("All dependencies installed")
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return check_requirements()

def check_env():
    if not os.path.exists('.env'):
        print("Creating .env file from .env.example...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as src:
                content = src.read()
            with open('.env', 'w') as dst:
                dst.write(content)
        else:
            print("Warning: .env.example not found")
            return False
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("Installing python-dotenv...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
        from dotenv import load_dotenv
        load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your-gemini-api-key-here':
        print("ERROR: Please set GEMINI_API_KEY in .env file")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        return False
    
    return True

def create_directories():
    directories = ['data', 'logs']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def start_backend():
    print("Starting backend server...")
    backend_process = subprocess.Popen(
        [sys.executable, "backend/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    return backend_process

def start_frontend():
    print("Starting frontend server on port 8000...")
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8000"],
        cwd="frontend",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    return frontend_process

def print_startup_info():
    print("\n" + "="*70)
    print("  INTELLIGENT BOARD GAMES - AI POWERED")
    print("="*70)
    print("\nServers running:")
    print("  Backend API:  http://localhost:5000")
    print("  Frontend UI:  http://localhost:8000")
    print("\nFeatures:")
    print("  - Society of Thought AI reasoning")
    print("  - Character personality mimicry")
    print("  - Nano Banana Pro decision engine")
    print("  - Genie3 VR integration (if available)")
    print("\nGames available:")
    print("  1. Brass: Birmingham (4 players)")
    print("  2. Gloomhaven (4 players)")
    print("  3. Terraforming Mars (5 players)")
    print("  4. Dune (6 players)")
    print("  5. Dungeons & Dragons (6 players)")
    print("  6. Exploding Kittens (5 players)")
    print("\n" + "="*70)
    print("\nPress Ctrl+C to stop all servers\n")

def monitor_process(process, name):
    for line in iter(process.stdout.readline, ''):
        if line:
            print(f"[{name}] {line.strip()}")

def main():
    print("Intelligent Board Games - Starting...")
    print("-" * 50)
    
    if not check_requirements():
        print("Failed to install requirements")
        sys.exit(1)
    
    if not check_env():
        print("Environment configuration failed")
        sys.exit(1)
    
    create_directories()
    
    backend = start_backend()
    time.sleep(3)
    
    if backend.poll() is not None:
        print("ERROR: Backend failed to start")
        print("Check if port 5000 is already in use")
        sys.exit(1)
    
    frontend = start_frontend()
    time.sleep(2)
    
    if frontend.poll() is not None:
        print("ERROR: Frontend failed to start")
        print("Check if port 8000 is already in use")
        backend.terminate()
        sys.exit(1)
    
    print_startup_info()
    
    try:
        backend.wait()
    except KeyboardInterrupt:
        print("\n\nShutting down servers...")
        backend.terminate()
        frontend.terminate()
        
        backend.wait(timeout=5)
        frontend.wait(timeout=5)
        
        print("Servers stopped successfully")
        print("Thank you for using Intelligent Board Games!")

if __name__ == '__main__':
    main()