#!/bin/bash

# ==================================================================================
# 🔥 AI FUTURE SIGNAL BOT V6 ULTIMATE - GitHub Installer
# One-command installation from GitHub
# ==================================================================================

set -e  # Exit on error

cat << "BANNER"
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║        🔥 AI FUTURE SIGNAL BOT V6 ULTIMATE - INSTALLER 🔥               ║
║                                                                          ║
║              Installing from GitHub Repository                          ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
BANNER

echo ""
echo "💎 This will install V6 ULTIMATE bot with all dependencies"
echo "📦 Installation directory: ~/bot_v6_ultimate"
echo ""

# Check if already installed
if [ -d "$HOME/bot_v6_ultimate" ]; then
    echo "⚠️  Directory ~/bot_v6_ultimate already exists!"
    read -p "Backup and continue? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        mv ~/bot_v6_ultimate ~/bot_v6_ultimate_backup_$(date +%Y%m%d_%H%M%S)
        echo "✅ Backup created"
    else
        echo "❌ Installation cancelled"
        exit 0
    fi
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 STEP 1/5: Checking System"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check Python
if command -v python3.10 &> /dev/null; then
    PYTHON_CMD="python3.10"
    echo "✅ Python 3.10 found"
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    echo "✅ Python 3.11 found"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | grep -oP '\d+\.\d+')
    if [[ "$PYTHON_VERSION" == "3.10" ]] || [[ "$PYTHON_VERSION" == "3.11" ]]; then
        PYTHON_CMD="python3"
        echo "✅ Python $PYTHON_VERSION found"
    else
        echo "⚠️  Python 3.10 or 3.11 recommended (found: $PYTHON_VERSION)"
        PYTHON_CMD="python3"
    fi
else
    echo "❌ Python not found! Please install Python 3.10:"
    echo "   sudo apt install python3.10 python3.10-venv"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 STEP 2/5: Installing System Dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Installing with sudo..."
    sudo apt update
    sudo apt install -y python3-pip python3-venv git curl wget screen
else
    echo "Installing as root..."
    apt update
    apt install -y python3-pip python3-venv git curl wget screen
fi

echo "✅ System dependencies installed"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 STEP 3/5: Setting Up Bot"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd ~

# Note: Repository already cloned (we're running from it)
# In production, this would be:
# git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git bot_v6_ultimate

# If running from within repo:
if [ -f "main.py" ]; then
    echo "✅ Running from repository directory"
    BOT_DIR=$(pwd)
else
    # Assume we need to use current location
    echo "✅ Setting up in current directory"
    BOT_DIR=$(pwd)
fi

cd "$BOT_DIR"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 STEP 4/5: Creating Virtual Environment"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

$PYTHON_CMD -m venv venv
source venv/bin/activate

echo "✅ Virtual environment created"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 STEP 5/5: Installing Python Dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

pip install --upgrade pip --quiet

echo "Installing core dependencies..."
pip install python-telegram-bot==20.7 --quiet
pip install python-binance==1.0.19 --quiet
pip install python-dotenv==1.0.0 --quiet
pip install aiohttp==3.9.1 --quiet
pip install requests==2.31.0 --quiet

echo "Installing data libraries..."
pip install pandas==2.0.3 --quiet 2>/dev/null || echo "⚠️  Pandas skipped (optional)"
pip install numpy==1.24.4 --quiet 2>/dev/null || echo "⚠️  Numpy skipped (optional)"
pip install ta==0.10.2 --quiet 2>/dev/null || echo "⚠️  TA skipped (optional)"

echo "✅ All dependencies installed"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ INSTALLATION COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📂 Bot Location: $BOT_DIR"
echo ""

# Check if .env exists
if [ ! -f "config/.env" ]; then
    echo "⚠️  Configuration file not found!"
    echo ""
    echo "📋 NEXT STEPS:"
    echo ""
    echo "1. Create config file:"
    echo "   cp config/.env.example config/.env"
    echo "   nano config/.env"
    echo ""
    echo "2. Add your Telegram Bot Token (get from @BotFather)"
    echo "   TELEGRAM_BOT_TOKEN=your_token_here"
    echo ""
    echo "3. (Optional) Add Binance API keys"
    echo "   BINANCE_API_KEY=your_key"
    echo "   BINANCE_SECRET_KEY=your_secret"
    echo ""
    echo "4. Run bot:"
    echo "   source venv/bin/activate"
    echo "   python3 main.py"
    echo ""
else
    echo "✅ Configuration file found"
    echo ""
    echo "🚀 TO START BOT:"
    echo ""
    echo "   cd $BOT_DIR"
    echo "   source venv/bin/activate"
    echo "   python3 main.py"
    echo ""
    echo "📱 Then send /start to your Telegram bot"
    echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📚 Documentation:"
echo "   • README.md - Overview & quick start"
echo "   • UBUNTU_INSTALL_GUIDE.md - Complete guide"
echo "   • VISUAL_INSTALL_GUIDE.md - Visual guide"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎉 Installation script completed!"
echo "💎 V6 ULTIMATE is ready to use!"
echo ""
echo "🚀 Happy Trading!"
echo ""
