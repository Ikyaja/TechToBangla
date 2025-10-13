#!/bin/bash

# Telegram Trading Bot Setup Script for Termux
# This script prepares everything needed to run the bot

echo "🚀 Setting up Telegram Trading Bot for Termux..."

# Update packages
echo "📦 Updating packages..."
pkg update -y
pkg upgrade -y

# Install required packages
echo "🔧 Installing required packages..."
pkg install -y python python-pip git curl wget nodejs npm

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip
pip install python-telegram-bot==20.7
pip install python-binance==1.0.19
pip install pandas==2.1.4
pip install numpy==1.24.4
pip install ta==0.10.2
pip install requests==2.31.0
pip install asyncio
pip install aiohttp==3.9.1
pip install python-dotenv==1.0.0
pip install matplotlib==3.8.2
pip install plotly==5.17.0
pip install websocket-client==1.6.4
pip install schedule==1.2.0

# Create bot directory structure
echo "📁 Creating bot directory structure..."
mkdir -p telegram_bot
mkdir -p telegram_bot/config
mkdir -p telegram_bot/modules
mkdir -p telegram_bot/data
mkdir -p telegram_bot/logs
mkdir -p telegram_bot/charts

# Set permissions
chmod +x telegram_bot/

echo "✅ Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Configure your API keys in config/.env"
echo "2. Run the bot with: python telegram_bot/main.py"
echo ""
echo "🔑 Don't forget to set your API keys!"