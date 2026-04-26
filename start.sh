#!/bin/bash
# University Portal - Complete Setup Script
# Run this to start both backend and frontend together

set -e

echo "=========================================="
echo "  University Portal - Full Stack Starter"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if port is in use
check_port() {
    lsof -i:$1 > /dev/null 2>&1
}

# Kill existing processes on ports
kill_port() {
    if check_port $1; then
        echo -e "${YELLOW}Killing existing process on port $1...${NC}"
        fuser -k $1/tcp 2>/dev/null || true
    fi
}

# Install dependencies if needed
echo -e "${GREEN}Installing dependencies...${NC}"
cd /workspace/university-portal
npm install 2>/dev/null || true
pip install django django-ninja django-cors-headers pyjwt Pillow python-dotenv 2>/dev/null || true

# Start Backend
echo -e "${GREEN}Starting Backend (port 8001)...${NC}"
cd /workspace/university-portal/apps/api
python3 manage.py runserver 8001 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
sleep 3

# Start Frontend  
echo -e "${GREEN}Starting Frontend (port 3000)...${NC}"
cd /workspace/university-portal/apps/web
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
sleep 5

# Test both
echo ""
echo "=========================================="
echo "  Testing Connection..."
echo "=========================================="

BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/api/config)
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)

echo -e "Backend: ${GREEN}$BACKEND_STATUS${NC}"
echo -e "Frontend: ${GREEN}$FRONTEND_STATUS${NC}"

if [ "$BACKEND_STATUS" = "200" ] && [ "$FRONTEND_STATUS" = "200" ]; then
    echo ""
    echo -e "${GREEN}✓ FULL STACK RUNNING!${NC}"
    echo ""
    echo "  Frontend: http://localhost:3000"
    echo "  Backend:  http://localhost:8001"
    echo "  API:     http://localhost:8001/api"
    echo ""
    echo "  Login:   admin@uni.edu / admin123"
    echo ""
    echo "  To stop: pkill -f 'manage.py' && pkill -f 'next dev'"
else
    echo -e "${YELLOW}Some issues detected. Check logs.${NC}"
fi