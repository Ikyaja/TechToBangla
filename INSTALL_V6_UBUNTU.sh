#!/bin/bash

# ==================================================================================
# 🔥 AI FUTURE SIGNAL BOT V6 ULTIMATE - UBUNTU AUTO-INSTALLER
# One-click installation untuk Ubuntu Server
# ==================================================================================

clear

cat << "LOGO"
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║        🔥 AI FUTURE SIGNAL BOT V6 ULTIMATE - AUTO INSTALLER 🔥         ║
║                                                                          ║
║                    Ubuntu Server Installation                            ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
LOGO

echo ""
echo "💎 This script will install V6 ULTIMATE bot on Ubuntu"
echo "⏱️  Estimated time: 5-10 minutes"
echo ""
read -p "Press ENTER to continue or Ctrl+C to cancel..."
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo "⚠️  Please DO NOT run as root. Run as normal user."
   exit 1
fi

# Detect Ubuntu version
echo "🔍 Detecting system..."
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "✅ OS: $NAME $VERSION"
else
    echo "❌ Cannot detect OS version"
    exit 1
fi

echo ""
echo "=" * 70
echo "📦 STEP 1/7: Updating System"
echo "=" * 70
echo ""

sudo apt update
echo "✅ System updated"

echo ""
echo "=" * 70
echo "📦 STEP 2/7: Installing System Dependencies"
echo "=" * 70
echo ""

sudo apt install -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    python3-pip \
    build-essential \
    libssl-dev \
    libffi-dev \
    git \
    curl \
    wget \
    screen \
    htop \
    nano

echo "✅ System dependencies installed"

echo ""
echo "=" * 70
echo "📦 STEP 3/7: Creating Bot Directory"
echo "=" * 70
echo ""

BOT_DIR="$HOME/trading_bot_v6_ultimate"

# Backup jika sudah ada
if [ -d "$BOT_DIR" ]; then
    echo "⚠️  Directory exists, creating backup..."
    mv "$BOT_DIR" "${BOT_DIR}_backup_$(date +%Y%m%d_%H%M%S)"
fi

mkdir -p "$BOT_DIR"/{modules,config,logs}
cd "$BOT_DIR"

echo "✅ Directory created: $BOT_DIR"

echo ""
echo "=" * 70
echo "📦 STEP 4/7: Creating Virtual Environment"
echo "=" * 70
echo ""

python3.10 -m venv venv
source venv/bin/activate

echo "✅ Virtual environment created"

echo ""
echo "=" * 70
echo "📦 STEP 5/7: Installing Python Dependencies"
echo "=" * 70
echo ""

pip install --upgrade pip --quiet
echo "Installing telegram bot library..."
pip install python-telegram-bot==20.7 --quiet
echo "Installing binance library..."
pip install python-binance==1.0.19 --quiet
echo "Installing other libraries..."
pip install python-dotenv==1.0.0 --quiet
pip install aiohttp==3.9.1 --quiet
pip install requests==2.31.0 --quiet

echo "Installing data libraries..."
pip install pandas==2.0.3 --quiet 2>/dev/null || echo "⚠️  Pandas skipped (optional)"
pip install numpy==1.24.4 --quiet 2>/dev/null || echo "⚠️  Numpy skipped (optional)"
pip install ta==0.10.2 --quiet 2>/dev/null || echo "⚠️  TA skipped (optional)"

echo "✅ Python dependencies installed"

echo ""
echo "=" * 70
echo "📦 STEP 6/7: Generating Bot Files"
echo "=" * 70
echo ""

# Create __init__ files
touch __init__.py modules/__init__.py

# Create config
cat > config/.env << 'ENVEOF'
TELEGRAM_BOT_TOKEN=8285776454:AAE2lg7Lrkc0e7dVNFTMPef_dZEQ6JK4Wko
BINANCE_API_KEY=8a81A0t9zsXIRtaPHBhK9nHw9oezbZZHhepnvcJVoiDu0obJ3DaOQl5tcEm20jpS
BINANCE_SECRET_KEY=8ZrwXhPRyPB0YGKkFIyba1ajoD90eAccHzd0nV1u2qTbMvMip4VQ0OXdp38mukva
BOT_NAME=AI FUTURE SIGNAL V6 ULTIMATE
DEFAULT_LEVERAGE=125
ENVEOF

echo "✅ Config file created"
echo "⚠️  NOTE: Edit config/.env to update your API keys if needed"

echo ""
echo "📂 Bot files need to be copied manually or via SCP"
echo ""
echo "📋 FILES NEEDED:"
echo "   1. main.py"
echo "   2. modules/technical_analysis_v6.py"
echo "   3. modules/signal_generator_v6.py"
echo "   4. modules/ui_formatter_v6.py"
echo "   5. modules/binance_client.py"
echo ""
echo "📍 Files location on development: /workspace/bot_v6_ultimate/"
echo ""
echo "🔧 COPY OPTIONS:"
echo ""
echo "   Option A - Via SCP (from your computer):"
echo "   scp -r /workspace/bot_v6_ultimate/* user@server-ip:$BOT_DIR/"
echo ""
echo "   Option B - Via Git:"
echo "   git clone your-repo-url $BOT_DIR/"
echo ""
echo "   Option C - Manual:"
echo "   nano main.py  # Then paste content"
echo ""

read -p "Have you copied all bot files? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "⏸️  Installation paused"
    echo "📋 Next steps:"
    echo "   1. Copy bot files to: $BOT_DIR/"
    echo "   2. Run this script again"
    echo ""
    exit 0
fi

echo ""
echo "=" * 70
echo "📦 STEP 7/7: Final Setup"
echo "=" * 70
echo ""

# Set permissions
chmod +x main.py 2>/dev/null || echo "main.py will be set executable when copied"
chmod 600 config/.env

echo "✅ Permissions set"

# Create systemd service
echo ""
echo "🔧 Creating systemd service..."

sudo tee /etc/systemd/system/trading-bot-v6.service > /dev/null << SERVICEEOF
[Unit]
Description=AI Future Signal Bot V6 Ultimate
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$BOT_DIR
Environment="PATH=$BOT_DIR/venv/bin"
ExecStart=$BOT_DIR/venv/bin/python3 main.py
Restart=always
RestartSec=10
StandardOutput=append:$BOT_DIR/logs/bot_output.log
StandardError=append:$BOT_DIR/logs/bot_error.log

[Install]
WantedBy=multi-user.target
SERVICEEOF

# Reload systemd
sudo systemctl daemon-reload

echo "✅ Systemd service created"

echo ""
echo "=" * 70
echo "✅ INSTALLATION COMPLETE!"
echo "=" * 70
echo ""
echo "📂 Bot Location: $BOT_DIR"
echo ""
echo "🚀 TO START BOT:"
echo ""
echo "   Option A - Systemd (Recommended for 24/7):"
echo "   sudo systemctl enable trading-bot-v6"
echo "   sudo systemctl start trading-bot-v6"
echo "   sudo systemctl status trading-bot-v6"
echo ""
echo "   Option B - Screen (Manual):"
echo "   cd $BOT_DIR"
echo "   source venv/bin/activate"
echo "   screen -S trading_bot"
echo "   python3 main.py"
echo "   # Detach: Ctrl+A, D"
echo ""
echo "   Option C - Direct (Testing):"
echo "   cd $BOT_DIR"
echo "   source venv/bin/activate"
echo "   python3 main.py"
echo ""
echo "📊 USEFUL COMMANDS:"
echo "   sudo systemctl status trading-bot-v6    # Check status"
echo "   sudo systemctl restart trading-bot-v6   # Restart"
echo "   sudo systemctl stop trading-bot-v6      # Stop"
echo "   tail -f $BOT_DIR/logs/bot_v6.log        # View logs"
echo ""
echo "📚 FULL GUIDE: $BOT_DIR/../UBUNTU_INSTALL_GUIDE.md"
echo ""
echo "🎉 READY TO TRADE WITH V6 ULTIMATE! 🚀"
echo ""
