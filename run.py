import subprocess
import os
import sys
import time
import webbrowser
import threading

def run_backend():
    print("Starting Flask backend server...")
    subprocess.Popen([sys.executable, "app.py"], cwd=os.path.dirname(os.path.abspath(__file__)))
    time.sleep(2)  # Give time for the backend to start

def run_frontend():
    print("Starting React frontend development server...")
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend"))
    
    if os.name == 'nt':  # Windows
        subprocess.Popen(["npm.cmd", "start"], shell=True)
    else:  # Unix/Linux
        subprocess.Popen(["npm", "start"], shell=True)
    
    time.sleep(5)  # Give time for the frontend to compile and start

def setup_frontend():
    """Check if node_modules exists, if not run npm install"""
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
    if not os.path.exists(os.path.join(frontend_dir, "node_modules")):
        print("Installing frontend dependencies (this might take a few minutes)...")
        os.chdir(frontend_dir)
        
        if os.name == 'nt':  # Windows
            subprocess.call(["npm.cmd", "install"], shell=True)
        else:  # Unix/Linux
            subprocess.call(["npm", "install"], shell=True)

def open_browser():
    """Open browser after a delay"""
    time.sleep(8)  # Wait for everything to be up
    print("Opening application in browser...")
    webbrowser.open('http://localhost:3000')

if __name__ == "__main__":
    print("VYB Nutrition Calculator")
    print("------------------------")
    
    # First check if frontend dependencies are installed
    setup_frontend()
    
    # Start the backend server
    run_backend()
    
    # Start the frontend development server
    run_frontend()
    
    # Open browser tab
    thread = threading.Thread(target=open_browser)
    thread.start()
    
    print("\nBoth servers are now running.")
    print("Backend: http://localhost:5000")
    print("Frontend: http://localhost:3000")
    print("\nPress Ctrl+C to stop both servers.")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
