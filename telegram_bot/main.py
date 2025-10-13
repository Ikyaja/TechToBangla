#!/usr/bin/env python3
"""
AI Future Signal - Advanced Telegram Trading Bot
Premium Market Analysis & Auto Trading Bot
"""

import os
import sys
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
from dotenv import load_dotenv

# Import custom modules
from modules.binance_client import BinanceClient
from modules.technical_analysis import TechnicalAnalyzer
from modules.signal_generator import SignalGenerator
from modules.auto_trader import AutoTrader
from modules.ui_formatter import UIFormatter

# Load environment variables
load_dotenv('config/.env')

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TradingBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.admin_id = os.getenv('ADMIN_USER_ID')
        
        # Initialize components
        self.binance_client = BinanceClient()
        self.technical_analyzer = TechnicalAnalyzer()
        self.signal_generator = SignalGenerator(self.binance_client, self.technical_analyzer)
        self.auto_trader = AutoTrader(self.binance_client)
        self.ui_formatter = UIFormatter()
        
        # Bot state
        self.active_signals = {}
        self.user_settings = {}
        self.auto_trading_users = set()
        
        # Create application
        self.application = Application.builder().token(self.token).build()
        self.setup_handlers()

    def setup_handlers(self):
        """Setup all command and callback handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("signals", self.signals_command))
        self.application.add_handler(CommandHandler("analysis", self.analysis_command))
        
        # Callback query handlers
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command with premium UI"""
        user = update.effective_user
        user_id = user.id
        
        # Initialize user settings
        if user_id not in self.user_settings:
            self.user_settings[user_id] = {
                'notifications': True,
                'auto_trading': False,
                'risk_level': 'medium',
                'preferred_pairs': ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
            }
        
        welcome_message = self.ui_formatter.format_welcome_message(user.first_name)
        keyboard = self.create_main_menu_keyboard()
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )

    def create_main_menu_keyboard(self):
        """Create the main menu keyboard with permanent buttons"""
        keyboard = [
            [
                KeyboardButton("📊 Live Signals"),
                KeyboardButton("📈 Market Analysis")
            ],
            [
                KeyboardButton("🤖 Auto Trading"),
                KeyboardButton("💼 Portfolio")
            ],
            [
                KeyboardButton("⚙️ Settings"),
                KeyboardButton("📚 Education")
            ],
            [
                KeyboardButton("🆘 Support"),
                KeyboardButton("ℹ️ About")
            ]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, persistent=True)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages from menu buttons"""
        text = update.message.text
        user_id = update.effective_user.id
        
        if text == "📊 Live Signals":
            await self.show_live_signals(update, context)
        elif text == "📈 Market Analysis":
            await self.show_market_analysis(update, context)
        elif text == "🤖 Auto Trading":
            await self.show_auto_trading_menu(update, context)
        elif text == "💼 Portfolio":
            await self.show_portfolio(update, context)
        elif text == "⚙️ Settings":
            await self.show_settings_menu(update, context)
        elif text == "📚 Education":
            await self.show_education_menu(update, context)
        elif text == "🆘 Support":
            await self.show_support_info(update, context)
        elif text == "ℹ️ About":
            await self.show_about_info(update, context)
        else:
            # Handle custom symbol analysis
            if text.upper().endswith('USDT') and len(text) <= 10:
                await self.analyze_custom_symbol(update, context, text.upper())

    async def show_live_signals(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show live trading signals with premium formatting"""
        try:
            # Get latest signals
            signals = await self.signal_generator.get_latest_signals()
            
            if not signals:
                message = "🔍 <b>Scanning markets for signals...</b>\n\n"
                message += "⏳ No signals available at the moment.\n"
                message += "💡 Signals are generated every 5 minutes based on technical analysis."
            else:
                message = self.ui_formatter.format_signals_list(signals)
            
            # Create inline keyboard for signal actions
            keyboard = [
                [
                    InlineKeyboardButton("🔄 Refresh", callback_data="refresh_signals"),
                    InlineKeyboardButton("⚙️ Filter", callback_data="filter_signals")
                ],
                [
                    InlineKeyboardButton("📊 Chart Analysis", callback_data="chart_analysis"),
                    InlineKeyboardButton("🔔 Notifications", callback_data="signal_notifications")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                message,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
            
        except Exception as e:
            logger.error(f"Error showing live signals: {e}")
            await update.message.reply_text("❌ Error loading signals. Please try again.")

    async def show_market_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show comprehensive market analysis"""
        try:
            # Get market overview
            market_data = await self.technical_analyzer.get_market_overview()
            
            message = self.ui_formatter.format_market_analysis(market_data)
            
            # Create analysis options keyboard
            keyboard = [
                [
                    InlineKeyboardButton("🔥 Top Gainers", callback_data="top_gainers"),
                    InlineKeyboardButton("📉 Top Losers", callback_data="top_losers")
                ],
                [
                    InlineKeyboardButton("💎 Volume Leaders", callback_data="volume_leaders"),
                    InlineKeyboardButton("⚡ Momentum Plays", callback_data="momentum_plays")
                ],
                [
                    InlineKeyboardButton("📊 Custom Analysis", callback_data="custom_analysis")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                message,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
            
        except Exception as e:
            logger.error(f"Error showing market analysis: {e}")
            await update.message.reply_text("❌ Error loading market analysis. Please try again.")

    async def show_auto_trading_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show auto trading configuration menu"""
        user_id = update.effective_user.id
        is_active = user_id in self.auto_trading_users
        
        message = self.ui_formatter.format_auto_trading_status(is_active, self.user_settings.get(user_id, {}))
        
        # Create auto trading keyboard
        keyboard = []
        if is_active:
            keyboard.append([InlineKeyboardButton("🛑 Stop Auto Trading", callback_data="stop_auto_trading")])
        else:
            keyboard.append([InlineKeyboardButton("🚀 Start Auto Trading", callback_data="start_auto_trading")])
        
        keyboard.extend([
            [
                InlineKeyboardButton("⚙️ Configure", callback_data="configure_auto_trading"),
                InlineKeyboardButton("📊 Performance", callback_data="trading_performance")
            ],
            [
                InlineKeyboardButton("💰 Risk Settings", callback_data="risk_settings"),
                InlineKeyboardButton("🎯 Strategy", callback_data="trading_strategy")
            ]
        ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard callbacks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user_id = query.from_user.id
        
        if data == "refresh_signals":
            await self.refresh_signals(query, context)
        elif data == "start_auto_trading":
            await self.start_auto_trading(query, context)
        elif data == "stop_auto_trading":
            await self.stop_auto_trading(query, context)
        elif data == "top_gainers":
            await self.show_top_gainers(query, context)
        elif data == "custom_analysis":
            await self.show_custom_analysis_prompt(query, context)
        # Add more callback handlers as needed

    async def refresh_signals(self, query, context):
        """Refresh and update signals display"""
        try:
            signals = await self.signal_generator.get_latest_signals()
            message = self.ui_formatter.format_signals_list(signals)
            
            await query.edit_message_text(
                message,
                reply_markup=query.message.reply_markup,
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.error(f"Error refreshing signals: {e}")

    async def start_auto_trading(self, query, context):
        """Start auto trading for user"""
        user_id = query.from_user.id
        
        # Add safety checks and confirmations here
        confirmation_message = (
            "⚠️ <b>Auto Trading Confirmation</b>\n\n"
            "🤖 You are about to enable auto trading.\n"
            "💰 Please ensure you understand the risks.\n\n"
            "✅ Confirm to proceed or ❌ cancel."
        )
        
        keyboard = [
            [
                InlineKeyboardButton("✅ Confirm", callback_data="confirm_auto_trading"),
                InlineKeyboardButton("❌ Cancel", callback_data="cancel_auto_trading")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            confirmation_message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    async def run_signal_monitoring(self):
        """Background task to monitor and generate signals"""
        while True:
            try:
                # Generate new signals
                new_signals = await self.signal_generator.scan_for_signals()
                
                # Send signals to subscribed users
                for signal in new_signals:
                    await self.broadcast_signal(signal)
                
                # Wait for next scan
                await asyncio.sleep(300)  # 5 minutes
                
            except Exception as e:
                logger.error(f"Error in signal monitoring: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error

    async def broadcast_signal(self, signal):
        """Broadcast signal to all subscribed users"""
        message = self.ui_formatter.format_premium_signal(signal)
        
        for user_id, settings in self.user_settings.items():
            if settings.get('notifications', True):
                try:
                    await self.application.bot.send_message(
                        chat_id=user_id,
                        text=message,
                        parse_mode=ParseMode.HTML
                    )
                except Exception as e:
                    logger.error(f"Error sending signal to user {user_id}: {e}")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help information"""
        help_text = self.ui_formatter.format_help_message()
        await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show bot status"""
        status_info = await self.get_bot_status()
        message = self.ui_formatter.format_status_message(status_info)
        await update.message.reply_text(message, parse_mode=ParseMode.HTML)

    async def get_bot_status(self):
        """Get current bot status information"""
        return {
            'active_users': len(self.user_settings),
            'auto_trading_users': len(self.auto_trading_users),
            'active_signals': len(self.active_signals),
            'uptime': datetime.now() - self.start_time if hasattr(self, 'start_time') else timedelta(0),
            'binance_status': await self.binance_client.check_connection()
        }

    def run(self):
        """Start the bot"""
        self.start_time = datetime.now()
        logger.info("🚀 Starting AI Future Signal Bot...")
        
        # Start background tasks
        asyncio.create_task(self.run_signal_monitoring())
        
        # Start the bot
        self.application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Initialize and run bot
    bot = TradingBot()
    bot.run()