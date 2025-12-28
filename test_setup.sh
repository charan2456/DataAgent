#!/bin/bash

# Data Agent - Setup Test Script
# This script checks if all prerequisites are installed and helps set up the environment

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "🔍 Checking prerequisites for Data Agent..."

# Check Python
echo -n "Checking Python... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3.10+ not found${NC}"
    echo "  Install: https://www.python.org/downloads/"
    exit 1
fi

# Check Node.js
echo -n "Checking Node.js... "
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Found Node.js $NODE_VERSION${NC}"
else
    echo -e "${RED}✗ Node.js 18+ not found${NC}"
    echo "  Install: https://nodejs.org/"
    exit 1
fi

# Check MongoDB
echo -n "Checking MongoDB... "
if command -v mongosh &> /dev/null || command -v mongo &> /dev/null; then
    echo -e "${GREEN}✓ MongoDB found${NC}"
    MONGO_OK=true
else
    echo -e "${YELLOW}⚠ MongoDB not found${NC}"
    echo "  Install: https://www.mongodb.com/try/download/community"
    MONGO_OK=false
fi

# Check Redis
echo -n "Checking Redis... "
if command -v redis-cli &> /dev/null; then
    if redis-cli ping > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Redis found and running${NC}"
        REDIS_OK=true
    else
        echo -e "${YELLOW}⚠ Redis found but not running${NC}"
        echo "  Start with: sudo systemctl start redis-server (Linux) or brew services start redis (macOS)"
        REDIS_OK=false
    fi
else
    echo -e "${YELLOW}⚠ Redis not found${NC}"
    echo "  Install: https://redis.io/download"
    REDIS_OK=false
fi

# Check API Key
echo -n "Checking OpenAI API Key... "
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}⚠ Not set${NC}"
    echo "  Set with: export OPENAI_API_KEY='your-key-here'"
    echo "  Get free key: https://platform.openai.com/api-keys"
    echo "  See FREE_API_KEYS.md for options"
    API_KEY_OK=false
else
    echo -e "${GREEN}✓ API Key is set${NC}"
    API_KEY_OK=true
fi

echo ""
echo "════════════════════════════════════════"
echo "Setup Status:"
echo "════════════════════════════════════════"
echo "Python:     ${GREEN}✓${NC}"
echo "Node.js:    ${GREEN}✓${NC}"
echo "MongoDB:    $([ "$MONGO_OK" = true ] && echo -e "${GREEN}✓${NC}" || echo -e "${YELLOW}⚠${NC}")"
echo "Redis:      $([ "$REDIS_OK" = true ] && echo -e "${GREEN}✓${NC}" || echo -e "${YELLOW}⚠${NC}")"
echo "API Key:    $([ "$API_KEY_OK" = true ] && echo -e "${GREEN}✓${NC}" || echo -e "${YELLOW}⚠${NC}")"
echo ""

if [ "$MONGO_OK" = false ] || [ "$REDIS_OK" = false ] || [ "$API_KEY_OK" = false ]; then
    echo -e "${YELLOW}⚠ Some prerequisites are missing${NC}"
    echo ""
    echo "Quick fixes:"
    [ "$MONGO_OK" = false ] && echo "  - Install MongoDB: See LOCALHOST_SETUP.md"
    [ "$REDIS_OK" = false ] && echo "  - Install/Start Redis: See LOCALHOST_SETUP.md"
    [ "$API_KEY_OK" = false ] && echo "  - Get API Key: See FREE_API_KEYS.md"
    echo ""
    echo "You can still proceed, but some features may not work."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}Ready to start Data Agent!${NC}"
echo ""
echo "Next steps:"
echo "1. Initialize MongoDB (if not done):"
echo "   mongosh"
echo "   > use data_agent"
echo "   > db.createCollection('user')"
echo "   > db.createCollection('message')"
echo "   > db.createCollection('conversation')"
echo "   > db.createCollection('folder')"
echo ""
echo "2. Start backend:"
echo "   cd backend"
echo "   python main.py"
echo ""
echo "3. Start frontend (in new terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "Or use the automated script:"
echo "   ./start_localhost.sh"

