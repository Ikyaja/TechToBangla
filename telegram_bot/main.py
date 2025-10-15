#!/usr/bin/env python3
import os
import sys
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import signal

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
from dotenv import load_dotenv

from modules.binance_client import BinanceClient
from modules.technical_analysis import TechnicalAnalyzer
from modules.signal_generator import SignalGenerator
from modules.auto_trader import AutoTrader
from modules.ui_formatter import UIFormatter

load_dotenv('config/.env')

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
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
        self.running = False
        
        # User states for conversation flow
        self.user_states = {}
        
        try:
            self.binance_client = BinanceClient()
            self.technical_analyzer = TechnicalAnalyzer()
            self.signal_generator = SignalGenerator(self.binance_client, self.technical_analyzer)
            self.auto_trader = AutoTrader(self.binance_client)
            self.ui_formatter = UIFormatter()
            
            self.user_settings = {}
            self.auto_trading_users = set()
            
            # Top 10 tradeable pairs
            self.top_pairs = [
                'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'XRPUSDT',
                'SOLUSDT', 'DOTUSDT', 'AVAXUSDT', 'MATICUSDT', 'LINKUSDT'
            ]
            
            # Available timeframes
            self.timeframes = {
                '1m': '1 Minute',
                '5m': '5 Minutes', 
                '15m': '15 Minutes',
                '30m': '30 Minutes',
                '1h': '1 Hour'
            }
            
            self.application = Application.builder().token(self.token).build()
            self.setup_handlers()
            
            logger.info("✅ Bot initialized successfully")
        except Exception as e:
            logger.error(f"❌ Bot initialization failed: {e}")
            raise

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            user = update.effective_user
            if user.id not in self.user_settings:
                self.user_settings[user.id] = {'notifications': True, 'auto_trading': False}
            
            welcome = self.ui_formatter.format_welcome_message(user.first_name)
            
            keyboard = ReplyKeyboardMarkup([
                [KeyboardButton("📊 Live Signals"), KeyboardButton("📈 Market Analysis")],
                [KeyboardButton("🤖 Auto Trading"), KeyboardButton("💼 Portfolio")],
                [KeyboardButton("⚙️ Settings"), KeyboardButton("🆘 Support")]
            ], resize_keyboard=True)
            
            await update.message.reply_text(welcome, reply_markup=keyboard, parse_mode=ParseMode.HTML)
            logger.info(f"✅ User {user.first_name} ({user.id}) started the bot")
            
        except Exception as e:
            logger.error(f"Error in start_command: {e}")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            text = update.message.text
            user_id = update.effective_user.id
            
            logger.info(f"📨 Received: {text} from user {user_id}")
            
            if text == "📊 Live Signals":
                await self.show_live_signals(update, context)
            elif text == "📈 Market Analysis":
                await self.show_market_analysis_menu(update, context)
            elif text == "🤖 Auto Trading":
                await self.show_auto_trading_menu(update, context)
            elif text == "💼 Portfolio":
                await self.show_portfolio(update, context)
            elif text == "⚙️ Settings":
                await self.show_settings(update, context)
            elif text == "🆘 Support":
                await self.show_support(update, context)
            else:
                await update.message.reply_text("❓ Unknown command. Use the menu buttons or /help for available commands.")
                
        except Exception as e:
            logger.error(f"Error in handle_message: {e}")

    async def show_market_analysis_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show market analysis with pair selection"""
        try:
            message = f"""📈 <b>ADVANCED MARKET ANALYSIS</b> 📈
<i>Professional Technical Analysis</i>

🎯 <b>Select a trading pair for deep analysis:</b>

📊 <b>TOP 10 RECOMMENDED PAIRS:</b>
• High liquidity & volume
• Best for technical analysis
• Suitable for all timeframes

🔥 <b>Analysis Features:</b>
• 500 candle deep analysis
• Multi-indicator confluence
• Support/Resistance levels
• Entry/Exit recommendations
• Risk management advice

👇 <b>Choose a pair below:</b>"""

            # Create keyboard with top 10 pairs
            keyboard = []
            for i in range(0, len(self.top_pairs), 2):
                row = []
                for j in range(2):
                    if i + j < len(self.top_pairs):
                        pair = self.top_pairs[i + j]
                        row.append(InlineKeyboardButton(f"📊 {pair}", callback_data=f"analyze_pair_{pair}"))
                keyboard.append(row)
            
            # Add back button
            keyboard.append([InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_main")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(message, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            logger.error(f"Error in show_market_analysis_menu: {e}")
            await update.message.reply_text("❌ Error loading market analysis menu.")

    async def show_timeframe_selection(self, query, pair: str):
        """Show timeframe selection for chosen pair"""
        try:
            message = f"""⏰ <b>SELECT TIMEFRAME</b>

📊 <b>Pair Selected:</b> {pair}

🎯 <b>Choose your trading timeframe:</b>

⚡ <b>Scalping:</b> 1m, 5m
📈 <b>Day Trading:</b> 15m, 30m  
🏆 <b>Swing Trading:</b> 1h

💡 <b>Recommendation:</b>
• Beginners: 15m or 30m
• Experienced: 5m or 1h
• Scalpers: 1m or 5m

👇 <b>Select timeframe:</b>"""

            keyboard = [
                [InlineKeyboardButton("⚡ 1 Minute", callback_data=f"tf_{pair}_1m"), InlineKeyboardButton("🔥 5 Minutes", callback_data=f"tf_{pair}_5m")],
                [InlineKeyboardButton("📈 15 Minutes", callback_data=f"tf_{pair}_15m"), InlineKeyboardButton("💎 30 Minutes", callback_data=f"tf_{pair}_30m")],
                [InlineKeyboardButton("🏆 1 Hour", callback_data=f"tf_{pair}_1h")],
                [InlineKeyboardButton("🔙 Back to Pairs", callback_data="back_pairs")]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(message, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            logger.error(f"Error in show_timeframe_selection: {e}")

    async def perform_advanced_analysis(self, query, pair: str, timeframe: str):
        """Perform advanced 500-candle analysis"""
        try:
            # Show loading message
            loading_msg = f"""🔄 <b>ANALYZING {pair}</b>

⏳ <b>Processing 500 candles...</b>
📊 Timeframe: {self.timeframes.get(timeframe, timeframe)}
🤖 Running PRO-level analysis...

Please wait 10-15 seconds..."""

            await query.edit_message_text(loading_msg, parse_mode=ParseMode.HTML)
            
            # Get 500 candles data
            df = await self.binance_client.get_klines(pair, timeframe, 500)
            
            if df is None or df.empty:
                await query.edit_message_text("❌ Error getting market data. Please try again.", parse_mode=ParseMode.HTML)
                return
            
            # Perform advanced technical analysis
            analysis_result = await self.technical_analyzer.perform_advanced_analysis(df, pair, timeframe)
            
            # Format the comprehensive analysis
            message = self.ui_formatter.format_advanced_analysis(analysis_result, pair, timeframe)
            
            # Create action buttons
            keyboard = [
                [InlineKeyboardButton("🔄 Refresh Analysis", callback_data=f"tf_{pair}_{timeframe}")],
                [InlineKeyboardButton("📊 Different Timeframe", callback_data=f"analyze_pair_{pair}"), InlineKeyboardButton("🔙 Different Pair", callback_data="back_pairs")]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(message, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            logger.error(f"Error in perform_advanced_analysis: {e}")
            await query.edit_message_text("❌ Error performing analysis. Please try again.", parse_mode=ParseMode.HTML)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        try:
            data = query.data
            logger.info(f"🔘 Callback: {data} from user {query.from_user.id}")
            
            if data == "refresh":
                signals = await self.signal_generator.get_latest_signals()
                message = self.ui_formatter.format_signals_list(signals)
                await query.edit_message_text(message, parse_mode=ParseMode.HTML)
                
            elif data.startswith("analyze_pair_"):
                pair = data.replace("analyze_pair_", "")
                await self.show_timeframe_selection(query, pair)
                
            elif data.startswith("tf_"):
                parts = data.split("_")
                if len(parts) >= 3:
                    pair = parts[1]
                    timeframe = parts[2]
                    await self.perform_advanced_analysis(query, pair, timeframe)
                    
            elif data == "back_pairs":
                # Recreate the pair selection menu
                message = f"""📈 <b>ADVANCED MARKET ANALYSIS</b> 📈

🎯 <b>Select a trading pair for deep analysis:</b>

👇 <b>Choose a pair below:</b>"""

                keyboard = []
                for i in range(0, len(self.top_pairs), 2):
                    row = []
                    for j in range(2):
                        if i + j < len(self.top_pairs):
                            pair = self.top_pairs[i + j]
                            row.append(InlineKeyboardButton(f"📊 {pair}", callback_data=f"analyze_pair_{pair}"))
                    keyboard.append(row)
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(message, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
                
            elif data == "start_auto":
                user_id = query.from_user.id
                self.auto_trading_users.add(user_id)
                await query.edit_message_text("🚀 <b>Auto Trading Enabled!</b>\n\n✅ Auto trading activated.", parse_mode=ParseMode.HTML)
                
            elif data == "stop_auto":
                user_id = query.from_user.id
                self.auto_trading_users.discard(user_id)
                await query.edit_message_text("🛑 <b>Auto Trading Stopped!</b>\n\n✅ Auto trading disabled.", parse_mode=ParseMode.HTML)
                
        except Exception as e:
            logger.error(f"Error in handle_callback: {e}")

    async def show_live_signals(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            signals = await self.signal_generator.get_latest_signals()
            if signals:
                message = self.ui_formatter.format_signals_list(signals)
            else:
                message = "🔍 <b>Scanning markets for signals...</b>\n\n⏳ No signals available at the moment.\n💡 Signals are generated every 5 minutes."
            
            keyboard = [[InlineKeyboardButton("🔄 Refresh", callback_data="refresh")]]
            await update.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
            
        except Exception as e:
            logger.error(f"Error in show_live_signals: {e}")
            await update.message.reply_text("❌ Error loading signals.")

    async def show_auto_trading_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            user_id = update.effective_user.id
            is_active = user_id in self.auto_trading_users
            message = self.ui_formatter.format_auto_trading_status(is_active, self.user_settings.get(user_id, {}))
            
            keyboard = []
            if is_active:
                keyboard.append([InlineKeyboardButton("🛑 Stop Auto Trading", callback_data="stop_auto")])
            else:
                keyboard.append([InlineKeyboardButton("🚀 Start Auto Trading", callback_data="start_auto")])
            
            await update.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
            
        except Exception as e:
            logger.error(f"Error in show_auto_trading_menu: {e}")

    async def show_portfolio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            portfolio_data = {
                'total_balance': 1250.75, 'daily_pnl': 5.2, 'total_pnl': 15.8,
                'total_trades': 47, 'win_rate': 85.1, 'best_trade': 12.5, 'worst_trade': -3.2
            }
            message = self.ui_formatter.format_portfolio_summary(portfolio_data)
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            logger.error(f"Error in show_portfolio: {e}")

    async def show_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = "⚙️ <b>SETTINGS</b>\n\n🔧 Configure your bot preferences here.\n\n📊 Coming soon: Advanced settings panel"
        await update.message.reply_text(message, parse_mode=ParseMode.HTML)

    async def show_support(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = "🆘 <b>SUPPORT</b>\n\n❓ Need help? Contact:\n\n📧 Support: @Ulascryptomaster\n💬 Community: t.me/aifuturesignal"
        await update.message.reply_text(message, parse_mode=ParseMode.HTML)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            help_text = self.ui_formatter.format_help_message()
            await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.error(f"Error in help_command: {e}")

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            status_info = {
                'active_users': len(self.user_settings),
                'auto_trading_users': len(self.auto_trading_users),
                'binance_status': await self.binance_client.check_connection()
            }
            message = f"""🤖 <b>BOT STATUS</b>

🟢 <b>System Status:</b> Online
👥 <b>Active Users:</b> {status_info['active_users']}
🤖 <b>Auto Trading Users:</b> {status_info['auto_trading_users']}
🔗 <b>Binance:</b> {'✅ Connected' if status_info['binance_status'] else '📊 Demo Mode'}

⏰ <b>Last Update:</b> {datetime.now().strftime('%H:%M:%S WIB')}"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.error(f"Error in status_command: {e}")

    async def run_signal_monitoring(self):
        """Background signal monitoring"""
        logger.info("📊 Starting signal monitoring...")
        
        while self.running:
            try:
                new_signals = await self.signal_generator.scan_for_signals()
                if new_signals:
                    logger.info(f"📈 Generated {len(new_signals)} signals")
                    
                    for signal in new_signals:
                        message = self.ui_formatter.format_premium_signal(signal)
                        
                        for user_id in list(self.user_settings.keys()):
                            try:
                                await self.application.bot.send_message(
                                    chat_id=user_id, 
                                    text=message, 
                                    parse_mode=ParseMode.HTML
                                )
                            except Exception as e:
                                logger.error(f"Error sending signal to user {user_id}: {e}")
                
                for i in range(300):
                    if not self.running:
                        break
                    await asyncio.sleep(1)
                        
            except Exception as e:
                logger.error(f"Signal monitoring error: {e}")
                await asyncio.sleep(60)

    def signal_handler(self, signum, frame):
        logger.info("🛑 Shutdown signal received")
        self.running = False

    async def start_bot(self):
        try:
            self.running = True
            
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)
            
            monitoring_task = asyncio.create_task(self.run_signal_monitoring())
            
            logger.info("🚀 Starting Telegram bot...")
            
            async with self.application:
                await self.application.initialize()
                await self.application.start()
                await self.application.updater.start_polling(drop_pending_updates=True)
                
                logger.info("✅ Bot is running! Press Ctrl+C to stop.")
                
                try:
                    while self.running:
                        await asyncio.sleep(1)
                except KeyboardInterrupt:
                    self.running = False
                
                await self.application.updater.stop()
                await self.application.stop()
                await self.application.shutdown()
                
                monitoring_task.cancel()
                try:
                    await monitoring_task
                except asyncio.CancelledError:
                    pass
                
        except Exception as e:
            logger.error(f"❌ Error starting bot: {e}")
            raise

    def run(self):
        try:
            logger.info("🚀 Starting AI Future Signal Bot...")
            asyncio.run(self.start_bot())
        except KeyboardInterrupt:
            logger.info("🛑 Bot stopped by user")
        except Exception as e:
            logger.error(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    try:
        os.makedirs('logs', exist_ok=True)
        bot = TradingBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
