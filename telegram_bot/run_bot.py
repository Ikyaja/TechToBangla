#!/usr/bin/env python3
"""
Alternative bot runner with enhanced error handling and logging
"""

import os
import sys
import logging
import signal
import asyncio
from datetime import datetime

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def setup_logging():
    """Setup comprehensive logging"""
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # File handler
    file_handler = logging.FileHandler(
        f'logs/bot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format))
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = {
        'telegram': 'python-telegram-bot',
        'binance': 'python-binance',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'ta': 'ta',
        'requests': 'requests',
        'aiohttp': 'aiohttp',
        'dotenv': 'python-dotenv'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            if package == 'telegram':
                import telegram
            elif package == 'binance':
                import binance
            elif package == 'dotenv':
                import dotenv
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Install them using: pip install " + " ".join(missing_packages))
        return False
    
    return True

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print(f"\n🛑 Received signal {signum}. Shutting down gracefully...")
    sys.exit(0)

def main():
    """Main function to run the bot"""
    print("🚀 AI Future Signal Bot - Starting...")
    print("=" * 50)
    
    # Setup logging
    logger = setup_logging()
    logger.info("Bot startup initiated")
    
    # Check dependencies
    print("🔧 Checking dependencies...")
    if not check_dependencies():
        logger.error("Missing dependencies")
        sys.exit(1)
    
    print("✅ All dependencies are installed")
    
    # Check configuration
    if not os.path.exists('config/.env'):
        logger.error("Configuration file config/.env not found")
        print("❌ Configuration file config/.env not found")
        sys.exit(1)
    
    print("✅ Configuration file found")
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Import and run the bot
        from main import TradingBot
        
        print("🤖 Initializing AI Future Signal Bot...")
        print("📊 Features: Real-time Analysis | Trading Signals | Auto Trading")
        print("⚡ Starting bot services...")
        print("🔄 Press Ctrl+C to stop")
        print("=" * 50)
        
        # Create and run bot
        bot = TradingBot()
        logger.info("Bot initialized successfully")
        
        bot.run()
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
        logger.info("Bot stopped by user interrupt")
    except Exception as e:
        print(f"❌ Error running bot: {e}")
        logger.error(f"Bot error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        print("👋 AI Future Signal Bot shutdown complete")
        logger.info("Bot shutdown complete")

if __name__ == "__main__":
    main()