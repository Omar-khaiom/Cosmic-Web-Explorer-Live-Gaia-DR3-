#!/usr/bin/env python3
"""
Combined entrypoint for Celestial Navigator
Starts both backend (FastAPI on 5000) and frontend (http.server on 3000) in parallel
"""
import subprocess
import time
import signal
import sys
import os

# Make sure we're in the right directory
os.chdir('/app')

# Process handles
backend_process = None
frontend_process = None

def signal_handler(sig, frame):
    """Handle graceful shutdown"""
    print('\n[Entrypoint] Shutting down...')
    if backend_process:
        backend_process.terminate()
    if frontend_process:
        frontend_process.terminate()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

try:
    print('[Entrypoint] Starting backend (Uvicorn on 0.0.0.0:5000)...')
    backend_process = subprocess.Popen(
        [
            'python', '-m', 'uvicorn',
            'app:app',
            '--host', '0.0.0.0',
            '--port', '5000',
            '--log-level', 'info'
        ],
        cwd='/app/backend',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    print('[Entrypoint] Backend process started (PID: {})'.format(backend_process.pid))

    # Wait 2 seconds for backend to stabilize
    time.sleep(2)

    print('[Entrypoint] Starting frontend (http.server on 0.0.0.0:3000)...')
    frontend_process = subprocess.Popen(
        [
            'python', '-m', 'http.server',
            '3000',
            '--directory', '/app/viewer'
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    print('[Entrypoint] Frontend process started (PID: {})'.format(frontend_process.pid))

    print('[Entrypoint] ✅ Both services started successfully!')
    print('[Entrypoint] Backend:  http://0.0.0.0:5000')
    print('[Entrypoint] Frontend: http://0.0.0.0:3000')
    print('[Entrypoint] Keep running (press Ctrl+C to stop)...')

    # Keep the main process alive and monitor both services
    while True:
        time.sleep(1)
        
        # Check if processes are still alive
        if backend_process and backend_process.poll() is not None:
            print('[Entrypoint] ⚠️ Backend process died! Exit code: {}'.format(backend_process.returncode))
            # Restart backend
            print('[Entrypoint] Restarting backend...')
            backend_process = subprocess.Popen(
                [
                    'python', '-m', 'uvicorn',
                    'app:app',
                    '--host', '0.0.0.0',
                    '--port', '5000',
                    '--log-level', 'info'
                ],
                cwd='/app/backend',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            print('[Entrypoint] Backend restarted (PID: {})'.format(backend_process.pid))

        if frontend_process and frontend_process.poll() is not None:
            print('[Entrypoint] ⚠️ Frontend process died! Exit code: {}'.format(frontend_process.returncode))
            # Restart frontend
            print('[Entrypoint] Restarting frontend...')
            frontend_process = subprocess.Popen(
                [
                    'python', '-m', 'http.server',
                    '3000',
                    '--directory', '/app/viewer'
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            print('[Entrypoint] Frontend restarted (PID: {})'.format(frontend_process.pid))

except Exception as e:
    print('[Entrypoint] ❌ Error: {}'.format(str(e)))
    if backend_process:
        backend_process.terminate()
    if frontend_process:
        frontend_process.terminate()
    sys.exit(1)
