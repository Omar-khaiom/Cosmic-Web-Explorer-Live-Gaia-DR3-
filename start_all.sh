#!/bin/bash
# Start Cosmic-Web Explorer (Linux/macOS)
# Starts both backend (FastAPI on 5000) and frontend (static server on 3000)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Cosmic-Web Explorer (Gaia DR3 Live)${NC}"
echo "=========================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python 3 not found. Please install Python 3.10+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python: $PYTHON_VERSION${NC}"

# Check backend requirements
if [ ! -d "backend" ]; then
    echo -e "${RED}❌ Error: 'backend' directory not found. Run from repo root.${NC}"
    exit 1
fi

if [ ! -f "backend/requirements.txt" ]; then
    echo -e "${RED}❌ Error: 'backend/requirements.txt' not found${NC}"
    exit 1
fi

# Install/verify backend dependencies
echo -e "${YELLOW}📦 Checking backend dependencies...${NC}"
if ! python3 -c "import fastapi, uvicorn, astroquery" 2>/dev/null; then
    echo "   Installing requirements..."
    pip install -q -r backend/requirements.txt
    echo -e "   ${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "   ${GREEN}✓ All dependencies present${NC}"
fi

# Check for Gaia catalog
if [ ! -f "data/gaia_catalog.db" ]; then
    echo -e "${YELLOW}⚠️  Gaia catalog not found at: data/gaia_catalog.db${NC}"
    echo -e "   You can download it with:"
    echo -e "   ${BLUE}python3 backend/scripts/download_gaia_catalog.py --mag-limit 7.0 --output data/gaia_catalog.db${NC}"
    echo ""
    echo -e "   For now, using offline fallback sample (limited stars)"
    echo ""
fi

# Function to start backend
start_backend() {
    echo -e "${BLUE}🔧 Starting Backend (FastAPI on port 5000)...${NC}"
    cd backend
    python3 -m uvicorn app:app --host 0.0.0.0 --port 5000 --reload &
    BACKEND_PID=$!
    echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
    cd ..
    sleep 2
}

# Function to start frontend
start_frontend() {
    echo -e "${BLUE}🎨 Starting Frontend (HTTP server on port 3000)...${NC}"
    python3 -m http.server 3000 &
    FRONTEND_PID=$!
    echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
    sleep 1
}

# Function for cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
        echo "   Backend stopped"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
        echo "   Frontend stopped"
    fi
    echo -e "${GREEN}✓ Done${NC}"
}

# Register cleanup function
trap cleanup EXIT

# Start both servers
start_backend
start_frontend

# Print URLs
echo ""
echo -e "${GREEN}=========================================="
echo "✅ Both servers running!"
echo "=========================================="
echo -e "API Docs:  ${BLUE}http://localhost:5000/docs${NC}"
echo -e "Viewer:    ${BLUE}http://localhost:3000/viewer/index.html${NC}"
echo -e "=========================================${NC}"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for processes
wait
