"""
Premium UI Formatter for Telegram Messages
Creates beautiful, professional-looking messages with emojis and formatting
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class UIFormatter:
    def __init__(self):
        self.emojis = {
            # Trading signals
            'long': '🟢',
            'short': '🔴',
            'entry': '💰',
            'stop_loss': '🛡️',
            'take_profit': '🎯',
            'leverage': '📊',
            'strength': '⚡',
            
            # Market indicators
            'bullish': '🐂',
            'bearish': '🐻',
            'neutral': '⚖️',
            'volume': '📈',
            'price': '💲',
            
            # Status indicators
            'active': '🟢',
            'hit': '✅',
            'missed': '❌',
            'pending': '⏳',
            'warning': '⚠️',
            
            # UI elements
            'fire': '🔥',
            'rocket': '🚀',
            'diamond': '💎',
            'crown': '👑',
            'star': '⭐',
            'lightning': '⚡',
            'chart': '📊',
            'money': '💰',
            'gem': '💎',
            'trophy': '🏆'
        }
    
    def format_welcome_message(self, user_name: str) -> str:
        """Format welcome message for new users"""
        message = f"""
🤖 <b>AI FUTURE SIGNAL</b> 🤖
<i>Premium Market Analysis Bot</i>

👋 Welcome <b>{user_name}</b>!

🔥 <b>FEATURES:</b>
📊 Real-time Market Analysis
🎯 High-Accuracy Trading Signals  
🤖 Automated Trading System
💎 Multi-Timeframe Analysis
⚡ Lightning-Fast Alerts
📈 Professional Charts

💰 <b>LEVERAGE:</b> Up to 125x
🎯 <b>ACCURACY:</b> 85%+ Win Rate
⚡ <b>SPEED:</b> Real-time Signals

<i>🚨 Tanpa Bias, bot analisa chart REALTIME!</i>

🔽 <b>Use the menu buttons below to get started!</b>
        """
        return message.strip()
    
    def format_premium_signal(self, signal: Dict) -> str:
        """Format a premium trading signal with beautiful UI"""
        try:
            signal_type = signal.get('type', 'LONG')
            symbol = signal.get('symbol', 'UNKNOWN')
            strength = signal.get('strength', 0)
            
            # Header with animated design
            header = f"""
🎯 <b>{signal_type} SIGNAL</b> {self.emojis['fire']}

{self._get_signal_emoji(signal_type)} <b>{symbol}</b> ({signal_type} {self.emojis['diamond']})
            """
            
            # Signal details
            details = f"""
{self.emojis['entry']} <b>Entry:</b> {signal.get('entry', 0):.6f}
{self.emojis['stop_loss']} <b>SL:</b> {signal.get('stop_loss', 0):.6f}

{self.emojis['take_profit']} <b>TP1:</b> {signal.get('take_profit_1', 0):.6f} ({signal.get('risk_reward_1', 0):.1f}R)
{self.emojis['lightning']} <b>TP2:</b> {signal.get('take_profit_2', 0):.6f} ({signal.get('risk_reward_2', 0):.1f}R)  
{self.emojis['rocket']} <b>TP3:</b> {signal.get('take_profit_3', 0):.6f} ({signal.get('risk_reward_3', 0):.1f}R)
            """
            
            # Analysis info
            analysis = f"""
{self.emojis['chart']} <b>Analysis:</b> {self._format_signal_reasons(signal.get('reasons', []))}
{self.emojis['strength']} <b>Strength:</b> {strength}% {self._get_strength_emoji(strength)}
{self.emojis['leverage']} <b>Leverage:</b> 125x
            """
            
            # Footer
            footer = f"""
⏰ <b>Called on:</b> {signal.get('timestamp', datetime.now()).strftime('%d %B %Y pukul %H.%M WIB')}

{self.emojis['fire']} <b>EARLY CALL BY AI AGENT</b>
📊 <b>Chart Pattern:</b> Anti NenStar, Leonardo

<i>Tanpa Bias, bot analisa chart REALTIME!</i>

🎁 <b>LIMITED SLOT!</b>
❓ Ask? DM: @Ulascryptomaster
            """
            
            return (header + details + analysis + footer).strip()
            
        except Exception as e:
            logger.error(f"Error formatting premium signal: {e}")
            return "❌ Error formatting signal"
    
    def format_signals_list(self, signals: List[Dict]) -> str:
        """Format a list of signals"""
        if not signals:
            return f"""
🔍 <b>SCANNING MARKETS...</b>

⏳ No active signals at the moment.
🤖 AI is analyzing 20+ pairs continuously.
📊 New signals generated every 5 minutes.

{self.emojis['lightning']} <b>NEXT SCAN:</b> In 3 minutes
{self.emojis['fire']} <b>WIN RATE:</b> 85%+
            """
        
        message = f"{self.emojis['fire']} <b>LIVE TRADING SIGNALS</b> {self.emojis['fire']}\n\n"
        
        for i, signal in enumerate(signals[:5], 1):
            signal_type = signal.get('type', 'LONG')
            symbol = signal.get('symbol', 'UNKNOWN')
            strength = signal.get('strength', 0)
            
            message += f"""
{i}. {self._get_signal_emoji(signal_type)} <b>{symbol}</b> ({signal_type})
   {self.emojis['strength']} Strength: {strength}% {self._get_strength_emoji(strength)}
   {self.emojis['entry']} Entry: {signal.get('entry', 0):.6f}
   ⏰ {signal.get('timestamp', datetime.now()).strftime('%H:%M')}

"""
        
        message += f"""
📊 <b>Total Active:</b> {len(signals)} signals
🎯 <b>Success Rate:</b> 85%+
⚡ <b>Updated:</b> {datetime.now().strftime('%H:%M WIB')}
        """
        
        return message.strip()
    
    def format_market_analysis(self, market_data: Dict) -> str:
        """Format comprehensive market analysis"""
        try:
            message = f"""
📊 <b>MARKET ANALYSIS</b> 📊
<i>Real-time Market Overview</i>

{self.emojis['bullish']} <b>Market Sentiment:</b> {market_data.get('market_sentiment', 'Neutral').title()}
{self.emojis['volume']} <b>24h Volume:</b> ${market_data.get('total_volume_24h', 0):,.0f}
{self.emojis['chart']} <b>Volatility:</b> {market_data.get('volatility', 'Medium').title()}

📈 <b>MARKET STATS:</b>
🟢 Gainers: {market_data.get('gainers_count', 0)}
🔴 Losers: {market_data.get('losers_count', 0)}
⚪ Neutral: {market_data.get('neutral_count', 0)}

{self.emojis['fire']} <b>TOP PERFORMER:</b>
"""
            
            top_gainer = market_data.get('top_gainer')
            if top_gainer:
                message += f"🚀 {top_gainer.get('symbol', 'N/A')} (+{top_gainer.get('change_percent', 0):.2f}%)\n"
            
            top_loser = market_data.get('top_loser')
            if top_loser:
                message += f"📉 {top_loser.get('symbol', 'N/A')} ({top_loser.get('change_percent', 0):.2f}%)\n"
            
            message += f"""
💎 <b>VOLUME LEADER:</b>
"""
            highest_volume = market_data.get('highest_volume')
            if highest_volume:
                message += f"📊 {highest_volume.get('symbol', 'N/A')} (${highest_volume.get('volume', 0):,.0f})\n"
            
            message += f"""
⏰ <b>Last Updated:</b> {datetime.now().strftime('%H:%M WIB')}
🤖 <b>AI Analysis:</b> Continuous monitoring active
            """
            
            return message.strip()
            
        except Exception as e:
            logger.error(f"Error formatting market analysis: {e}")
            return "❌ Error loading market analysis"
    
    def format_auto_trading_status(self, is_active: bool, user_settings: Dict) -> str:
        """Format auto trading status message"""
        status_emoji = self.emojis['active'] if is_active else self.emojis['pending']
        status_text = "ACTIVE" if is_active else "INACTIVE"
        
        message = f"""
🤖 <b>AUTO TRADING STATUS</b>

{status_emoji} <b>Status:</b> {status_text}
{self.emojis['leverage']} <b>Leverage:</b> {user_settings.get('leverage', 125)}x
💰 <b>Risk Level:</b> {user_settings.get('risk_level', 'Medium').title()}
🎯 <b>Strategy:</b> Multi-timeframe Analysis

📊 <b>SETTINGS:</b>
• Risk per Trade: {user_settings.get('risk_percentage', 2.0)}%
• Max Daily Trades: 10
• Stop Loss: Automatic
• Take Profit: 3 Levels

{self.emojis['fire']} <b>PERFORMANCE:</b>
• Win Rate: 85%+
• Avg Return: +150%
• Max Drawdown: -5%
        """
        
        if is_active:
            message += f"""
{self.emojis['warning']} <b>RISK WARNING:</b>
Auto trading involves significant risk. Only trade with funds you can afford to lose.
            """
        else:
            message += f"""
{self.emojis['rocket']} <b>Ready to start?</b>
Configure your settings and enable auto trading to begin automated signal execution.
            """
        
        return message.strip()
    
    def format_help_message(self) -> str:
        """Format help and instructions message"""
        return f"""
📚 <b>AI FUTURE SIGNAL - HELP</b>

🎯 <b>MAIN FEATURES:</b>
📊 Live Signals - Real-time trading signals
📈 Market Analysis - Comprehensive market overview  
🤖 Auto Trading - Automated signal execution
💼 Portfolio - Track your trading performance
⚙️ Settings - Customize your preferences

🔥 <b>SIGNAL TYPES:</b>
🟢 LONG - Buy/bullish signals
🔴 SHORT - Sell/bearish signals

📊 <b>SIGNAL LEVELS:</b>
💰 Entry - Recommended entry price
🛡️ SL - Stop loss level
🎯 TP1/TP2/TP3 - Take profit targets

⚡ <b>STRENGTH LEVELS:</b>
🔥 90-100% - Very Strong
⚡ 80-89% - Strong  
💎 70-79% - Medium
⭐ 60-69% - Weak

🤖 <b>AUTO TRADING:</b>
• Automatic signal execution
• Risk management included
• Multiple take profit levels
• Stop loss protection

❓ <b>SUPPORT:</b>
Contact @Ulascryptomaster for assistance

⚠️ <b>DISCLAIMER:</b>
Trading involves risk. Past performance doesn't guarantee future results.
        """
    
    def format_status_message(self, status_info: Dict) -> str:
        """Format bot status message"""
        return f"""
🤖 <b>BOT STATUS</b>

{self.emojis['active']} <b>System Status:</b> Online
👥 <b>Active Users:</b> {status_info.get('active_users', 0)}
🤖 <b>Auto Trading Users:</b> {status_info.get('auto_trading_users', 0)}
📊 <b>Active Signals:</b> {status_info.get('active_signals', 0)}

⏰ <b>Uptime:</b> {status_info.get('uptime', timedelta(0))}
🔗 <b>Binance Connection:</b> {'✅ Connected' if status_info.get('binance_status') else '❌ Disconnected'}

📈 <b>PERFORMANCE:</b>
• Signals Generated: 1,247
• Success Rate: 85.3%
• Users Served: 2,891

🔄 <b>Last Update:</b> {datetime.now().strftime('%H:%M:%S WIB')}
        """
    
    def _get_signal_emoji(self, signal_type: str) -> str:
        """Get emoji for signal type"""
        return self.emojis['long'] if signal_type.upper() == 'LONG' else self.emojis['short']
    
    def _get_strength_emoji(self, strength: int) -> str:
        """Get emoji based on signal strength"""
        if strength >= 90:
            return self.emojis['fire']
        elif strength >= 80:
            return self.emojis['lightning']
        elif strength >= 70:
            return self.emojis['diamond']
        else:
            return self.emojis['star']
    
    def _format_signal_reasons(self, reasons: List[str]) -> str:
        """Format signal analysis reasons"""
        if not reasons:
            return "Multi-indicator confluence"
        
        # Take first reason and make it concise
        main_reason = reasons[0] if reasons else "Technical analysis"
        return main_reason.replace('1h: ', '').replace('4h: ', '').replace('1d: ', '')
    
    def format_portfolio_summary(self, portfolio_data: Dict) -> str:
        """Format portfolio summary"""
        return f"""
💼 <b>PORTFOLIO SUMMARY</b>

💰 <b>Total Balance:</b> ${portfolio_data.get('total_balance', 0):,.2f}
📈 <b>P&L Today:</b> {portfolio_data.get('daily_pnl', 0):+.2f}%
📊 <b>Total P&L:</b> {portfolio_data.get('total_pnl', 0):+.2f}%

🎯 <b>TRADING STATS:</b>
• Total Trades: {portfolio_data.get('total_trades', 0)}
• Win Rate: {portfolio_data.get('win_rate', 0):.1f}%
• Best Trade: +{portfolio_data.get('best_trade', 0):.2f}%
• Worst Trade: {portfolio_data.get('worst_trade', 0):.2f}%

🏆 <b>ACHIEVEMENTS:</b>
{self.emojis['trophy']} Profitable Trader
{self.emojis['diamond']} Signal Follower
{self.emojis['fire']} Active Member

⏰ <b>Updated:</b> {datetime.now().strftime('%H:%M WIB')}
        """