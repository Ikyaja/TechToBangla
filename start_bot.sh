#!/bin/bash

# AI Future Signal Bot Startup Script
echo "🚀 Starting AI Future Signal Bot..."

# Check if we're in Termux
if [ -n "$TERMUX_VERSION" ]; then
    echo "📱 Detected Termux environment"
    
    # Make sure we're in the right directory
    cd /data/data/com.termux/files/home/telegram_bot 2>/dev/null || cd ~/telegram_bot 2>/dev/null || {
        echo "❌ Bot directory not found. Please run setup_termux.sh first."
        exit 1
    }
else
    echo "💻 Detected standard Linux environment"
    cd telegram_bot 2>/dev/null || {
        echo "❌ Bot directory not found. Please run setup first."
        exit 1
    }
fi

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python first."
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# Check if required files exist
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found in current directory"
    exit 1
fi

if [ ! -f "config/.env" ]; then
    echo "❌ Configuration file not found. Please check config/.env"
    exit 1
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

echo "🔧 Checking dependencies..."

# Check if required Python packages are installed
$PYTHON_CMD -c "
import sys
required_packages = [
    'telegram', 'binance', 'pandas', 'numpy', 'ta', 
    'requests', 'aiohttp', 'python-dotenv', 'matplotlib'
]

missing_packages = []
for package in required_packages:
    try:
        if package == 'telegram':
            import telegram
        elif package == 'binance':
            import binance
        elif package == 'python-dotenv':
            import dotenv
        else:
            __import__(package)
    except ImportError:
        missing_packages.append(package)

if missing_packages:
    print(f'❌ Missing packages: {missing_packages}')
    print('📦 Please install them using: pip install -r requirements.txt')
    sys.exit(1)
else:
    print('✅ All dependencies are installed')
" || exit 1

echo "🤖 Starting the bot..."
echo "📊 AI Future Signal Bot is initializing..."
echo ""
echo "🔑 Bot Features:"
echo "   📊 Real-time market analysis"
echo "   🎯 High-accuracy trading signals"
echo "   🤖 Automated trading system"
echo "   💎 Multi-timeframe analysis"
echo "   ⚡ Lightning-fast alerts"
echo ""
echo "⏰ Starting at $(date)"
echo "🔄 Press Ctrl+C to stop the bot"
echo ""

# Start the bot with error handling
$PYTHON_CMD main.py 2>&1 | tee logs/bot_$(date +%Y%m%d_%H%M%S).log

echo ""
echo "🛑 Bot stopped at $(date)"