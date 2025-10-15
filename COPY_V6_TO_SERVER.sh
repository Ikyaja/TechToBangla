#!/bin/bash

# ==================================================================================
# 📦 COPY V6 ULTIMATE FILES TO SERVER
# Script untuk copy semua file V6 via SCP
# ==================================================================================

echo "📦 AI FUTURE SIGNAL V6 - File Transfer Script"
echo ""

# Prompt for server details
read -p "Enter server IP: " SERVER_IP
read -p "Enter username (default: ubuntu): " USERNAME
USERNAME=${USERNAME:-ubuntu}

echo ""
echo "📋 Will copy V6 files to: $USERNAME@$SERVER_IP:~/bot_v6/"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 0
fi

echo ""
echo "🔄 Copying files..."
echo ""

# Create directory on server
echo "1/2 Creating directory on server..."
ssh $USERNAME@$SERVER_IP "mkdir -p ~/bot_v6/{modules,config,logs}"

# Copy all files
echo "2/2 Copying bot files..."
scp -r bot_v6_ultimate/* $USERNAME@$SERVER_IP:~/bot_v6/

echo ""
echo "✅ Files copied successfully!"
echo ""
echo "📋 NEXT STEPS (on server):"
echo ""
echo "1. SSH to server:"
echo "   ssh $USERNAME@$SERVER_IP"
echo ""
echo "2. Setup virtual environment:"
echo "   cd ~/bot_v6"
echo "   python3.10 -m venv venv"
echo "   source venv/bin/activate"
echo ""
echo "3. Install dependencies:"
echo "   pip install --upgrade pip"
echo "   pip install python-telegram-bot==20.7 python-binance==1.0.19"
echo "   pip install python-dotenv aiohttp pandas==2.0.3 numpy==1.24.4"
echo ""
echo "4. Run bot:"
echo "   python3 main.py"
echo ""
echo "📚 Or read: ~/bot_v6/UBUNTU_INSTALL_GUIDE.md"
echo ""
