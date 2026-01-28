#!/bin/bash
set -e

echo "[Entrypoint] Starting Celestial Navigator..."

# Start backend in background
echo "[Entrypoint] Starting backend (Uvicorn on 0.0.0.0:5000)..."
cd /app/backend
python -m uvicorn app:app --host 0.0.0.0 --port 5000 --log-level info &
BACKEND_PID=$!
echo "[Entrypoint] Backend started (PID: $BACKEND_PID)"

# Wait for backend to stabilize
sleep 2

# Start frontend in background (serve from /app/viewer)
echo "[Entrypoint] Starting frontend (http.server on 0.0.0.0:3000)..."
cd /app/viewer
python -m http.server 3000 --bind 0.0.0.0 &
FRONTEND_PID=$!
echo "[Entrypoint] Frontend started (PID: $FRONTEND_PID)"

echo "[Entrypoint] ✅ Both services started!"
echo "[Entrypoint] Backend:  http://0.0.0.0:5000"
echo "[Entrypoint] Frontend: http://0.0.0.0:3000"

# Keep container running and handle signals
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true" SIGTERM SIGINT

wait -n

# If one dies, keep the container alive for logging/debugging
while true; do
  sleep 10
done
