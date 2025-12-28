#!/bin/bash

# Data Agent - Localhost Startup Script
# This script starts MongoDB, Redis, Backend, and Frontend

set -e

echo "🚀 Starting Data Agent on localhost..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if MongoDB is running
echo -e "${YELLOW}Checking MongoDB...${NC}"
if ! mongosh --eval "db.adminCommand('ping')" --quiet > /dev/null 2>&1; then
    echo -e "${RED}MongoDB is not running. Please start it first:${NC}"
    echo "  macOS: brew services start mongodb-community@7.0"
    echo "  Linux: sudo systemctl start mongod"
    exit 1
fi
echo -e "${GREEN}✓ MongoDB is running${NC}"

# Check if Redis is running
echo -e "${YELLOW}Checking Redis...${NC}"
if ! redis-cli ping > /dev/null 2>&1; then
    echo -e "${RED}Redis is not running. Please start it first:${NC}"
    echo "  macOS: brew services start redis"
    echo "  Linux: sudo systemctl start redis-server"
    exit 1
fi
echo -e "${GREEN}✓ Redis is running${NC}"

# Check for OpenAI API Key
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}⚠ Warning: OPENAI_API_KEY not set${NC}"
    echo "  Set it with: export OPENAI_API_KEY='your-key-here'"
fi

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate conda environment if it exists
if command -v conda &> /dev/null; then
    if conda env list | grep -q "data-agent"; then
        echo -e "${YELLOW}Activating conda environment...${NC}"
        eval "$(conda shell.bash hook)"
        conda activate data-agent
        echo -e "${GREEN}✓ Conda environment activated${NC}"
    fi
fi

# Start Backend
echo -e "${YELLOW}Starting Backend...${NC}"
cd backend

# Set default environment variables if not set
export MONGO_SERVER=${MONGO_SERVER:-127.0.0.1}
export REDIS_SERVER=${REDIS_SERVER:-127.0.0.1}
export CODE_EXECUTION_MODE=${CODE_EXECUTION_MODE:-local}
export FLASK_APP=${FLASK_APP:-backend.main}
export FLASK_ENV=${FLASK_ENV:-development}

# Start backend in background
python -m flask run -p 8000 --host=0.0.0.0 > ../backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
echo "  Logs: tail -f backend.log"

# Wait for backend to be ready
echo -e "${YELLOW}Waiting for backend to be ready...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:8000/api/llm_list > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend is ready${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}✗ Backend failed to start${NC}"
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

# Start Frontend
echo -e "${YELLOW}Starting Frontend...${NC}"
cd ../frontend

# Set frontend environment variable
export NEXT_PUBLIC_BACKEND_ENDPOINT=${NEXT_PUBLIC_BACKEND_ENDPOINT:-http://localhost:8000}

# Start frontend in background
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
echo "  Logs: tail -f frontend.log"

# Wait for frontend to be ready
echo -e "${YELLOW}Waiting for frontend to be ready...${NC}"
sleep 5

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}  Data Agent is running!${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:3000"
echo ""
echo "  Backend PID:  $BACKEND_PID"
echo "  Frontend PID: $FRONTEND_PID"
echo ""
echo "  To stop: Press Ctrl+C or run:"
echo "    kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "  View logs:"
echo "    tail -f backend.log"
echo "    tail -f frontend.log"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Stopping services...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo -e "${GREEN}✓ Services stopped${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT TERM

# Wait for processes
wait

