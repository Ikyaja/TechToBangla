#!/bin/bash

###############################################################################
#                                                                             #
#            🔥 SUPER SIMPLE INSTALLER - BOT V6 ULTIMATE 🔥                  #
#                                                                             #
#              SEKALI JALAN - OTOMATIS INSTALL SEMUANYA!                      #
#                                                                             #
###############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

clear

echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                          ║"
echo "║              🔥 INSTALLING BOT V6 ULTIMATE 🔥                           ║"
echo "║                                                                          ║"
echo "║                   Tunggu 2-3 menit ya...                                 ║"
echo "║                                                                          ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if source directory exists
if [ ! -d "/workspace/bot_v6_ultimate" ]; then
    echo -e "${RED}❌ Error: Source files not found at /workspace/bot_v6_ultimate${NC}"
    echo -e "${YELLOW}This script must be run from the workspace directory${NC}"
    exit 1
fi

INSTALL_DIR="$HOME/bot_v6_ultimate"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📦 Step 1/5: Checking system...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    echo -e "${GREEN}✅ Detected OS: $OS${NC}"
else
    echo -e "${RED}❌ Cannot detect OS${NC}"
    exit 1
fi

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📦 Step 2/5: Installing dependencies...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if command -v apt &> /dev/null; then
    echo -e "${YELLOW}Updating package list...${NC}"
    sudo apt update -qq
    
    echo -e "${YELLOW}Installing Python 3.10 and tools...${NC}"
    sudo apt install -y python3.10 python3.10-venv python3-pip git curl wget &> /dev/null || {
        echo -e "${YELLOW}⚠ Python 3.10 not available, installing Python 3...${NC}"
        sudo apt install -y python3 python3-venv python3-pip git curl wget
    }
elif command -v yum &> /dev/null; then
    echo -e "${YELLOW}Installing for RedHat/CentOS...${NC}"
    sudo yum install -y python3 python3-pip git curl wget
else
    echo -e "${RED}❌ Unsupported package manager${NC}"
    exit 1
fi

echo -e "${GREEN}✅ System dependencies installed!${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📂 Step 3/5: Copying bot files...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Remove old installation if exists
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}⚠ Removing old installation...${NC}"
    rm -rf "$INSTALL_DIR"
fi

# Copy entire bot directory
echo -e "${YELLOW}Copying files to $INSTALL_DIR...${NC}"
cp -r /workspace/bot_v6_ultimate "$INSTALL_DIR"

echo -e "${GREEN}✅ Bot files copied!${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}🐍 Step 4/5: Setting up Python environment...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

cd "$INSTALL_DIR"

# Detect Python version
if command -v python3.10 &> /dev/null; then
    PYTHON_CMD="python3.10"
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
else
    PYTHON_CMD="python3"
fi

PYTHON_VERSION=$($PYTHON_CMD --version)
echo -e "${GREEN}✅ Using: $PYTHON_VERSION${NC}"

echo -e "${YELLOW}Creating virtual environment...${NC}"
$PYTHON_CMD -m venv venv

echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip -q

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📚 Step 5/5: Installing Python packages...${NC}"
echo -e "${YELLOW}(This takes 2-3 minutes, please wait...)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

pip install -r requirements.txt

echo ""
echo -e "${GREEN}✅ All packages installed!${NC}"
echo ""

# Setup .env if not exists
if [ ! -f "config/.env" ]; then
    if [ -f "config/.env.example" ]; then
        echo -e "${YELLOW}Creating config/.env from template...${NC}"
        cp config/.env.example config/.env
        echo -e "${GREEN}✅ config/.env created${NC}"
    fi
fi

# Create run script
cat > run_bot.sh << 'RUNSCRIPT'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 main.py
RUNSCRIPT

chmod +x run_bot.sh

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                          ║"
echo "║                 ✅ INSTALLATION COMPLETE! ✅                             ║"
echo "║                                                                          ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}🎉 Bot V6 Ultimate berhasil diinstall!${NC}"
echo ""
echo -e "${YELLOW}📍 Location: $INSTALL_DIR${NC}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎯 LANGKAH SELANJUTNYA:${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}1. Edit konfigurasi:${NC}"
echo -e "   ${GREEN}nano $INSTALL_DIR/config/.env${NC}"
echo ""
echo -e "${YELLOW}2. Ganti token Telegram Bot:${NC}"
echo -e "   ${GREEN}TELEGRAM_BOT_TOKEN=YOUR_TOKEN_HERE${NC}"
echo ""
echo -e "${YELLOW}3. Save file (Ctrl+O, Enter, Ctrl+X)${NC}"
echo ""
echo -e "${YELLOW}4. Jalankan bot:${NC}"
echo -e "   ${GREEN}cd $INSTALL_DIR${NC}"
echo -e "   ${GREEN}./run_bot.sh${NC}"
echo ""
echo -e "   ${YELLOW}Atau:${NC}"
echo -e "   ${GREEN}cd $INSTALL_DIR${NC}"
echo -e "   ${GREEN}source venv/bin/activate${NC}"
echo -e "   ${GREEN}python3 main.py${NC}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}✅ Siap dijalankan! 🚀${NC}"
echo ""
echo -e "${YELLOW}💡 Tip: Test bot dengan send /start di Telegram!${NC}"
echo ""
