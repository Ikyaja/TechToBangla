#!/bin/bash

# ==================================================================================
# 🚀 QUICK START V6 ULTIMATE - Ubuntu
# Super simple installation
# ==================================================================================

cat << "BANNER"
🔥 AI FUTURE SIGNAL BOT V6 ULTIMATE
    QUICK START INSTALLER
BANNER

echo ""
echo "This will install V6 Ultimate bot in ~/bot_v6/"
echo ""

# One-liner commands
echo "📦 Installing (this may take 3-5 minutes)..."
echo ""

# Update & install in one go
sudo apt update && \
sudo apt install -y python3.10 python3.10-venv python3-pip screen && \
mkdir -p ~/bot_v6/{modules,config,logs} && \
cd ~/bot_v6 && \
python3.10 -m venv venv && \
source venv/bin/activate && \
pip install --upgrade pip --quiet && \
pip install python-telegram-bot==20.7 --quiet && \
pip install python-binance==1.0.19 --quiet && \
pip install python-dotenv==1.0.0 --quiet && \
pip install aiohttp==3.9.1 --quiet && \
pip install pandas==2.0.3 numpy==1.24.4 --quiet 2>/dev/null || true && \
touch __init__.py modules/__init__.py && \
cat > config/.env << 'ENVEOF'
TELEGRAM_BOT_TOKEN=8285776454:AAE2lg7Lrkc0e7dVNFTMPef_dZEQ6JK4Wko
BINANCE_API_KEY=8a81A0t9zsXIRtaPHBhK9nHw9oezbZZHhepnvcJVoiDu0obJ3DaOQl5tcEm20jpS
BINANCE_SECRET_KEY=8ZrwXhPRyPB0YGKkFIyba1ajoD90eAccHzd0nV1u2qTbMvMip4VQ0OXdp38mukva
BOT_NAME=AI FUTURE SIGNAL V6 ULTIMATE
ENVEOF

echo ""
echo "✅ Quick install complete!"
echo ""
echo "📂 Bot directory: ~/bot_v6/"
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "1. Copy bot files ke ~/bot_v6/"
echo "   - main.py"
echo "   - modules/*.py (5 files)"
echo ""
echo "2. Run bot:"
echo "   cd ~/bot_v6"
echo "   source venv/bin/activate"
echo "   python3 main.py"
echo ""
echo "📚 Full guide: ~/UBUNTU_INSTALL_GUIDE.md"
echo ""
