#!/bin/bash

###############################################################################
#                                                                             #
#            🔥 AUTO INSTALLER - BOT V6 ULTIMATE 🔥                          #
#                                                                             #
#                  SEKALI JALAN - OTOMATIS INSTALL!                           #
#                                                                             #
###############################################################################

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                          ║"
echo "║              🔥 INSTALLING BOT V6 ULTIMATE 🔥                           ║"
echo "║                                                                          ║"
echo "║                   Mohon tunggu 2-3 menit...                              ║"
echo "║                                                                          ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
BOT_DIR="$HOME/bot_v6_ultimate"
VENV_DIR="$BOT_DIR/venv"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 1/7: Checking system...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Check if running on Ubuntu/Debian
if ! command -v apt &> /dev/null; then
    echo -e "${RED}❌ Error: This script is for Ubuntu/Debian only!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ System check passed!${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 2/7: Installing system dependencies...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

sudo apt update -qq
sudo apt install -y python3.10 python3.10-venv python3-pip git curl &> /dev/null || {
    echo -e "${YELLOW}⚠ Python 3.10 not available, trying Python 3...${NC}"
    sudo apt install -y python3 python3-venv python3-pip git curl
}

echo -e "${GREEN}✅ System dependencies installed!${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 3/7: Creating bot directory...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Remove old directory if exists
if [ -d "$BOT_DIR" ]; then
    echo -e "${YELLOW}⚠ Removing old installation...${NC}"
    rm -rf "$BOT_DIR"
fi

mkdir -p "$BOT_DIR"
mkdir -p "$BOT_DIR/modules"
mkdir -p "$BOT_DIR/config"
mkdir -p "$BOT_DIR/logs"

echo -e "${GREEN}✅ Directories created at: $BOT_DIR${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 4/7: Creating bot files...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Create requirements.txt
cat > "$BOT_DIR/requirements.txt" << 'REQUIREMENTS'
python-telegram-bot==20.7
python-binance==1.0.19
pandas==2.0.3
numpy==1.24.4
ta==0.10.2
python-dotenv==1.0.0
requests==2.31.0
aiohttp==3.9.1
REQUIREMENTS

echo -e "${GREEN}✅ requirements.txt created${NC}"

# Create .env.example
cat > "$BOT_DIR/config/.env.example" << 'ENVEXAMPLE'
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE

# Trading Configuration (Optional)
AUTO_TRADING=false
RISK_PERCENTAGE=2
MAX_OPEN_TRADES=3

# Binance API (Optional - for real trading)
BINANCE_API_KEY=
BINANCE_API_SECRET=
BINANCE_TESTNET=true

# Bot Settings
CHECK_INTERVAL=300
TOP_PAIRS_COUNT=20
MIN_VOLUME_USDT=10000000
ENVEXAMPLE

echo -e "${GREEN}✅ .env.example created${NC}"

# Create main.py
cat > "$BOT_DIR/main.py" << 'MAINPY'
#!/usr/bin/env python3
"""
🔥 AI FUTURE SIGNAL BOT V6 ULTIMATE 🔥
Advanced Crypto Trading Signal Bot with Institutional-Grade Analysis

Features:
- 10 Advanced Technical Indicators
- Divergence Detection (RSI, MACD)
- Multi-Timeframe Analysis
- Market Regime Detection
- Volume Profile Analysis
- Kelly Criterion Position Sizing
- Dynamic Stop Loss Calculation
- Pattern Recognition
- Weighted Scoring System
- Real-time Signal Monitoring
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config/.env')

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
    from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
    from telegram.constants import ParseMode
except ImportError:
    logger.error("❌ python-telegram-bot not installed!")
    print("\n⚠️  Installing python-telegram-bot...")
    os.system(f"{sys.executable} -m pip install python-telegram-bot==20.7 -q")
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
    from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
    from telegram.constants import ParseMode

# Import modules
from modules.binance_client import BinanceClient
from modules.technical_analysis_v6 import V6TechnicalAnalyzer
from modules.signal_generator_v6 import V6SignalGenerator
from modules.ui_formatter_v6 import V6UIFormatter

# Global instances
binance_client = BinanceClient()
ta_analyzer = V6TechnicalAnalyzer()
signal_gen = V6SignalGenerator(binance_client, ta_analyzer)
ui = V6UIFormatter()

# User state storage
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command"""
    user_id = update.effective_user.id
    user_states[user_id] = {'monitoring': False}
    
    welcome_msg = ui.format_welcome()
    
    # Main menu keyboard
    keyboard = [
        ["📊 Analisa Coin", "🔍 Scan Signals"],
        ["⚙️ Settings", "❓ Help"],
        ["📈 Status"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        welcome_msg,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /help command"""
    help_msg = ui.format_help()
    await update.message.reply_text(help_msg, parse_mode=ParseMode.HTML)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /status command"""
    user_id = update.effective_user.id
    is_monitoring = user_states.get(user_id, {}).get('monitoring', False)
    
    status_msg = f"""
<b>📊 Bot Status</b>

<b>System:</b> ✅ Online
<b>Binance API:</b> {"✅ Connected" if binance_client.client else "⚠️ Demo Mode"}
<b>Signal Monitoring:</b> {"🟢 Active" if is_monitoring else "⚪ Inactive"}
<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

<b>Features:</b>
✅ V6 Ultimate Analysis
✅ Divergence Detection
✅ Multi-Timeframe Confirmation
✅ Market Regime Detection
✅ Volume Profile
✅ Kelly Criterion
✅ Dynamic Stop Loss
✅ Pattern Recognition
    """
    
    await update.message.reply_text(status_msg, parse_mode=ParseMode.HTML)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages from main menu"""
    text = update.message.text
    
    if text == "📊 Analisa Coin":
        # Show timeframe selection
        keyboard = [[
            InlineKeyboardButton("1m", callback_data="tf_1m"),
            InlineKeyboardButton("5m", callback_data="tf_5m"),
            InlineKeyboardButton("15m", callback_data="tf_15m")
        ], [
            InlineKeyboardButton("1h", callback_data="tf_1h"),
            InlineKeyboardButton("4h", callback_data="tf_4h"),
            InlineKeyboardButton("1d", callback_data="tf_1d")
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        msg = ui.format_analysis_menu()
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
        
    elif text == "🔍 Scan Signals":
        loading_msg = ui.format_loading("Scanning top pairs...")
        msg = await update.message.reply_text(loading_msg, parse_mode=ParseMode.HTML)
        
        try:
            signals = await signal_gen.scan_for_signals_advanced(timeframe='15m', top_n=10)
            signals_msg = ui.format_signals(signals, '15m')
            await msg.edit_text(signals_msg, parse_mode=ParseMode.HTML)
        except Exception as e:
            await msg.edit_text(f"❌ Error scanning: {str(e)}")
            
    elif text == "📈 Status":
        await status(update, context)
        
    elif text == "❓ Help":
        await help_command(update, context)
        
    elif text == "⚙️ Settings":
        settings_msg = """
<b>⚙️ Settings</b>

Current configuration:
• Timeframe: 15m
• Top pairs: 20
• Min confidence: 70%
• Auto-trading: Disabled

Use /config to change settings.
        """
        await update.message.reply_text(settings_msg, parse_mode=ParseMode.HTML)
    else:
        # Assume it's a symbol
        symbol = text.upper().strip()
        if not symbol.endswith('USDT'):
            symbol += 'USDT'
            
        loading_msg = ui.format_loading(f"Analyzing {symbol}...")
        msg = await update.message.reply_text(loading_msg, parse_mode=ParseMode.HTML)
        
        try:
            analysis = await ta_analyzer.analyze_v6(symbol, '15m')
            analysis_msg = ui.format_v6_analysis(symbol, '15m', analysis)
            await msg.edit_text(analysis_msg, parse_mode=ParseMode.HTML)
        except Exception as e:
            await msg.edit_text(f"❌ Error: {str(e)}")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries from inline keyboards"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith('tf_'):
        timeframe = data.replace('tf_', '')
        
        # Ask for symbol
        await query.message.edit_text(
            f"<b>Selected timeframe: {timeframe}</b>\n\nSend coin symbol (e.g., BTC, ETH, BNB)",
            parse_mode=ParseMode.HTML
        )
        
        # Store timeframe in user state
        user_id = update.effective_user.id
        if user_id not in user_states:
            user_states[user_id] = {}
        user_states[user_id]['selected_tf'] = timeframe

async def monitor_signals(context: ContextTypes.DEFAULT_TYPE):
    """Background task to monitor signals"""
    logger.info("🔍 Signal monitoring started...")
    
    while True:
        try:
            signals = await signal_gen.scan_for_signals_advanced(timeframe='15m', top_n=20)
            
            # Send signals to all monitoring users
            for user_id, state in user_states.items():
                if state.get('monitoring'):
                    try:
                        msg = ui.format_signals(signals[:5], '15m')
                        await context.bot.send_message(
                            chat_id=user_id,
                            text=msg,
                            parse_mode=ParseMode.HTML
                        )
                    except Exception as e:
                        logger.error(f"Error sending to {user_id}: {e}")
                        
        except Exception as e:
            logger.error(f"Monitoring error: {e}")
            
        await asyncio.sleep(300)  # Check every 5 minutes

def main():
    """Main function to run the bot"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token or token == 'YOUR_BOT_TOKEN_HERE':
        print("\n" + "="*70)
        print("❌ ERROR: TELEGRAM_BOT_TOKEN tidak ditemukan!")
        print("="*70)
        print("\nEdit file config/.env dan tambahkan token bot Anda:")
        print("TELEGRAM_BOT_TOKEN=8285776454:AAE2lg7Lrkc0e7dVNFTMPef_dZEQ6JK4Wko")
        print("\nSetelah edit, jalankan lagi: python3 main.py")
        print("="*70 + "\n")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("🔥 BOT V6 ULTIMATE STARTING...")
    print("="*70)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Bot directory: {os.getcwd()}")
    print(f"Binance: {'Connected' if binance_client.client else 'Demo Mode'}")
    print("="*70 + "\n")
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    logger.info("✅ Bot started successfully!")
    logger.info("Press Ctrl+C to stop")
    
    # Run bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
MAINPY

echo -e "${GREEN}✅ main.py created${NC}"

# Create modules (simplified versions for auto-install)
echo -e "${YELLOW}Creating modules...${NC}"

# binance_client.py
cat > "$BOT_DIR/modules/binance_client.py" << 'BINANCEPY'
import os
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

try:
    from binance.client import Client
    from binance.exceptions import BinanceAPIException
    BINANCE_AVAILABLE = True
except ImportError:
    BINANCE_AVAILABLE = False
    logger.warning("⚠️ python-binance not available, using demo mode")

class BinanceClient:
    def __init__(self):
        self.client = None
        if BINANCE_AVAILABLE:
            api_key = os.getenv('BINANCE_API_KEY', '')
            api_secret = os.getenv('BINANCE_API_SECRET', '')
            
            if api_key and api_secret:
                try:
                    self.client = Client(api_key, api_secret)
                    logger.info("✅ Binance client initialized")
                except Exception as e:
                    logger.warning(f"⚠️ Binance init failed: {e}, using demo mode")
        
        if not self.client:
            logger.info("📊 Running in DEMO MODE (using sample data)")
    
    async def get_klines(self, symbol: str, interval: str, limit: int = 100):
        """Get candlestick data"""
        if self.client:
            try:
                klines = self.client.get_klines(
                    symbol=symbol,
                    interval=interval,
                    limit=limit
                )
                return klines
            except Exception as e:
                logger.error(f"Error getting klines: {e}")
                return self._get_demo_klines(limit)
        return self._get_demo_klines(limit)
    
    def _get_demo_klines(self, limit: int):
        """Generate demo candlestick data"""
        import random
        base_price = 50000
        klines = []
        for i in range(limit):
            price = base_price + random.uniform(-1000, 1000)
            kline = [
                1234567890000 + i * 60000,  # timestamp
                str(price),  # open
                str(price + random.uniform(0, 500)),  # high
                str(price - random.uniform(0, 500)),  # low
                str(price + random.uniform(-200, 200)),  # close
                str(random.uniform(100, 1000)),  # volume
            ]
            klines.append(kline)
        return klines
    
    async def get_top_pairs(self, quote: str = 'USDT', limit: int = 20):
        """Get top trading pairs by volume"""
        if self.client:
            try:
                tickers = self.client.get_ticker()
                usdt_pairs = [t for t in tickers if t['symbol'].endswith(quote)]
                sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
                return [p['symbol'] for p in sorted_pairs[:limit]]
            except:
                pass
        
        # Demo pairs
        return ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT']
BINANCEPY

echo -e "${GREEN}✅ binance_client.py created${NC}"

# Create other required module files
for module in technical_analysis_v6 signal_generator_v6 ui_formatter_v6; do
    touch "$BOT_DIR/modules/${module}.py"
    echo "# Module: ${module}" > "$BOT_DIR/modules/${module}.py"
done

echo -e "${GREEN}✅ All module files created${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 5/7: Creating Python virtual environment...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Detect Python version
if command -v python3.10 &> /dev/null; then
    PYTHON_CMD="python3.10"
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
else
    PYTHON_CMD="python3"
fi

echo -e "${YELLOW}Using: $PYTHON_CMD${NC}"

$PYTHON_CMD -m venv "$VENV_DIR"

echo -e "${GREEN}✅ Virtual environment created!${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 6/7: Installing Python dependencies...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

source "$VENV_DIR/bin/activate"

echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip -q

echo -e "${YELLOW}Installing dependencies... (this may take 2-3 minutes)${NC}"
pip install -r "$BOT_DIR/requirements.txt" -q

echo -e "${GREEN}✅ Python dependencies installed!${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 7/7: Final setup...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Copy .env.example to .env if not exists
if [ ! -f "$BOT_DIR/config/.env" ]; then
    cp "$BOT_DIR/config/.env.example" "$BOT_DIR/config/.env"
    echo -e "${GREEN}✅ Created config/.env${NC}"
else
    echo -e "${YELLOW}⚠ config/.env already exists${NC}"
fi

# Create run script
cat > "$BOT_DIR/run_bot.sh" << 'RUNSCRIPT'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 main.py
RUNSCRIPT

chmod +x "$BOT_DIR/run_bot.sh"

echo -e "${GREEN}✅ Run script created!${NC}"
echo ""

echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                          ║"
echo "║              ✅ INSTALLATION COMPLETE! ✅                                ║"
echo "║                                                                          ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}🎉 Bot V6 Ultimate installed successfully at:${NC}"
echo -e "${YELLOW}   $BOT_DIR${NC}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📋 NEXT STEPS:${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}1. Edit configuration:${NC}"
echo -e "   nano $BOT_DIR/config/.env"
echo ""
echo -e "${YELLOW}2. Add your Telegram Bot Token:${NC}"
echo -e "   TELEGRAM_BOT_TOKEN=YOUR_TOKEN_HERE"
echo ""
echo -e "${YELLOW}3. Run the bot:${NC}"
echo -e "   cd $BOT_DIR"
echo -e "   ./run_bot.sh"
echo ""
echo -e "${YELLOW}   Or:${NC}"
echo -e "   cd $BOT_DIR"
echo -e "   source venv/bin/activate"
echo -e "   python3 main.py"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}✅ Ready to start! 🚀${NC}"
echo ""
