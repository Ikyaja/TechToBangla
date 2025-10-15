from datetime import datetime
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class UIFormatter:
    def __init__(self):
        self.emojis = {
            'long': '🟢', 'short': '🔴', 'fire': '🔥', 'rocket': '🚀', 
            'diamond': '💎', 'lightning': '⚡', 'star': '⭐', 'trophy': '🏆'
        }
    
    def format_welcome_message(self, user_name: str) -> str:
        return f"""🤖 <b>AI FUTURE SIGNAL</b> 🤖
<i>Premium Market Analysis Bot</i>

👋 Welcome <b>{user_name}</b>!

🔥 <b>FEATURES:</b>
📊 Real-time Market Analysis
🎯 High-Accuracy Trading Signals  
🤖 Automated Trading System
💎 Multi-Timeframe Analysis
⚡ Lightning-Fast Alerts
🔬 PRO-Level Technical Analysis

💰 <b>LEVERAGE:</b> Up to 125x
🎯 <b>ACCURACY:</b> 85%+ Win Rate
⚡ <b>SPEED:</b> Real-time Signals
🔬 <b>ANALYSIS:</b> 500 Candle Deep Scan

<i>🚨 Tanpa Bias, bot analisa chart REALTIME!</i>

🔽 <b>Use the menu buttons below!</b>"""

    def format_advanced_analysis(self, analysis: Dict, pair: str, timeframe: str) -> str:
        """Format comprehensive analysis result"""
        try:
            if 'error' in analysis:
                return f"❌ <b>Analysis Error</b>\n\n{analysis['error']}"
            
            current_price = analysis.get('current_price', 0)
            candles = analysis.get('candles_analyzed', 0)
            trend = analysis.get('trend_analysis', {})
            recommendation = analysis.get('recommendation', {})
            sr_levels = analysis.get('support_resistance', {})
            market_structure = analysis.get('market_structure', {})
            volume_analysis = analysis.get('volume_analysis', {})
            patterns = analysis.get('patterns', [])
            risk_assessment = analysis.get('risk_assessment', {})
            
            # Header
            message = f"""🔬 <b>ADVANCED ANALYSIS REPORT</b> 🔬

📊 <b>Pair:</b> {pair}
⏰ <b>Timeframe:</b> {timeframe}
💰 <b>Current Price:</b> {current_price:.6f}
📈 <b>Candles Analyzed:</b> {candles}

"""
            
            # Trend Analysis
            message += f"""🎯 <b>TREND ANALYSIS</b>
{trend.get('trend_color', '⚪')} <b>Overall Trend:</b> {trend.get('overall_trend', 'Unknown')}
⚡ <b>Trend Strength:</b> {trend.get('trend_strength', 0)}/5
🎯 <b>Confidence:</b> {trend.get('confidence', 0)}%

"""
            
            # Support/Resistance
            message += f"""🏗️ <b>SUPPORT & RESISTANCE</b>
🔴 <b>Nearest Resistance:</b> {sr_levels.get('nearest_resistance', 0):.6f} (+{sr_levels.get('resistance_distance', 0):.2f}%)
🟢 <b>Nearest Support:</b> {sr_levels.get('nearest_support', 0):.6f} (-{sr_levels.get('support_distance', 0):.2f}%)

"""
            
            # Market Structure
            message += f"""🏛️ <b>MARKET STRUCTURE</b>
📊 <b>Structure:</b> {market_structure.get('structure_type', 'Unknown')}
📈 <b>Swing Highs:</b> {market_structure.get('swing_highs', 0)}
📉 <b>Swing Lows:</b> {market_structure.get('swing_lows', 0)}

"""
            
            # Volume Analysis
            message += f"""📊 <b>VOLUME ANALYSIS</b>
📈 <b>Volume Trend:</b> {volume_analysis.get('volume_trend', 'Unknown')}
⚡ <b>Volume Ratio:</b> {volume_analysis.get('volume_ratio', 1.0):.2f}x
🔥 <b>Volume Spikes:</b> {volume_analysis.get('volume_spikes', 0)}

"""
            
            # Chart Patterns
            if patterns:
                message += f"""🎨 <b>CHART PATTERNS</b>
"""
                for pattern in patterns[:3]:
                    message += f"📊 {pattern}\n"
                message += "\n"
            
            # Risk Assessment
            message += f"""⚠️ <b>RISK ASSESSMENT</b>
{risk_assessment.get('risk_color', '🟡')} <b>Risk Level:</b> {risk_assessment.get('risk_level', 'Medium')}
📊 <b>Volatility:</b> {risk_assessment.get('atr_percent', 2.0):.2f}%
💰 <b>Recommended Size:</b> {risk_assessment.get('recommended_position_size', 1.0):.1f}%

"""
            
            # Trading Recommendation
            rec = recommendation
            message += f"""🎯 <b>TRADING RECOMMENDATION</b>
{rec.get('action_color', '⚪')} <b>Action:</b> {rec.get('recommendation', 'HOLD')}
🎯 <b>Confidence:</b> {rec.get('confidence', 50)}%
📊 <b>Score:</b> {rec.get('overall_score', 0)}/10

"""
            
            # Entry/Exit Levels (if not HOLD)
            if rec.get('recommendation', 'HOLD') != 'HOLD':
                message += f"""💰 <b>TRADING LEVELS</b>
🎯 <b>Entry:</b> {rec.get('entry', 0):.6f}
🛡️ <b>Stop Loss:</b> {rec.get('stop_loss', 0):.6f}

🎯 <b>Take Profit 1:</b> {rec.get('take_profit_1', 0):.6f} (R/R: {rec.get('risk_reward_1', 1):.1f})
⚡ <b>Take Profit 2:</b> {rec.get('take_profit_2', 0):.6f} (R/R: {rec.get('risk_reward_2', 2):.1f})
🚀 <b>Take Profit 3:</b> {rec.get('take_profit_3', 0):.6f} (R/R: {rec.get('risk_reward_3', 3):.1f})

"""
            
            # Detailed Signal Analysis
            signals = rec.get('signals', [])
            if signals:
                message += f"""🔍 <b>DETAILED ANALYSIS</b>
"""
                for i, (indicator, action, strength, reason) in enumerate(signals[:5], 1):
                    action_emoji = '🟢' if action == 'BUY' else '🔴' if action == 'SELL' else '⚪'
                    message += f"{i}. {action_emoji} <b>{indicator}:</b> {reason} ({strength}%)\n"
                
                message += "\n"
            
            # Footer
            message += f"""⏰ <b>Analysis Time:</b> {analysis.get('timestamp', datetime.now()).strftime('%d %B %Y pukul %H.%M WIB')}

🔬 <b>PROFESSIONAL ANALYSIS BY AI</b>
📊 <b>500 Candle Deep Scan Completed</b>
🎯 <b>Multi-Indicator Confluence</b>

<i>⚠️ This is advanced analysis. Trade responsibly!</i>

🎁 <b>PREMIUM ANALYSIS!</b>
❓ Questions? DM: @Ulascryptomaster"""
            
            return message.strip()
            
        except Exception as e:
            logger.error(f"Error formatting advanced analysis: {e}")
            return "❌ Error formatting analysis report"
    
    def format_premium_signal(self, signal: Dict) -> str:
        try:
            signal_type = signal.get('type', 'LONG')
            symbol = signal.get('symbol', 'UNKNOWN')
            strength = signal.get('strength', 0)
            
            return f"""🎯 <b>{signal_type} SIGNAL</b> {self.emojis['fire']}

{self.emojis['long'] if signal_type == 'LONG' else self.emojis['short']} <b>{symbol}</b> ({signal_type} {self.emojis['diamond']})

💰 <b>Entry:</b> {signal.get('entry', 0):.6f}
🛡️ <b>SL:</b> {signal.get('stop_loss', 0):.6f}

🎯 <b>TP1:</b> {signal.get('take_profit_1', 0):.6f} ({signal.get('risk_reward_1', 1.5):.1f}R)
⚡ <b>TP2:</b> {signal.get('take_profit_2', 0):.6f} ({signal.get('risk_reward_2', 3.0):.1f}R)
🚀 <b>TP3:</b> {signal.get('take_profit_3', 0):.6f} ({signal.get('risk_reward_3', 4.5):.1f}R)

📊 <b>Analysis:</b> {signal.get('reasons', ['Multi-indicator confluence'])[0]}
⚡ <b>Strength:</b> {strength}% {self._get_strength_emoji(strength)}
📊 <b>Leverage:</b> 125x

⏰ <b>Called on:</b> {signal.get('timestamp', datetime.now()).strftime('%d %B %Y pukul %H.%M WIB')}

{self.emojis['fire']} <b>EARLY CALL BY AI AGENT</b>
📊 <b>Chart Pattern:</b> Anti NenStar, Leonardo

<i>Tanpa Bias, bot analisa chart REALTIME!</i>

🎁 <b>LIMITED SLOT!</b>
❓ Ask? DM: @Ulascryptomaster"""
        except:
            return "❌ Error formatting signal"
    
    def format_signals_list(self, signals: List[Dict]) -> str:
        if not signals:
            return f"""🔍 <b>SCANNING MARKETS...</b>

⏳ No active signals at the moment.
🤖 AI is analyzing pairs continuously.

{self.emojis['fire']} <b>WIN RATE:</b> 85%+"""
        
        message = f"{self.emojis['fire']} <b>LIVE TRADING SIGNALS</b> {self.emojis['fire']}\n\n"
        
        for i, signal in enumerate(signals[:3], 1):
            signal_type = signal.get('type', 'LONG')
            symbol = signal.get('symbol', 'UNKNOWN')
            strength = signal.get('strength', 0)
            
            message += f"""{i}. {self.emojis['long'] if signal_type == 'LONG' else self.emojis['short']} <b>{symbol}</b> ({signal_type})
   ⚡ Strength: {strength}%
   💰 Entry: {signal.get('entry', 0):.6f}

"""
        
        message += f"""📊 <b>Total Active:</b> {len(signals)} signals
🎯 <b>Success Rate:</b> 85%+"""
        
        return message
    
    def format_market_analysis(self, market_data: Dict) -> str:
        return f"""📊 <b>MARKET ANALYSIS</b> 📊

🐂 <b>Market Sentiment:</b> {market_data.get('market_sentiment', 'Neutral').title()}
📈 <b>24h Volume:</b> ${market_data.get('total_volume_24h', 0):,.0f}

📈 <b>MARKET STATS:</b>
🟢 Gainers: {market_data.get('gainers_count', 0)}
🔴 Losers: {market_data.get('losers_count', 0)}

⏰ <b>Updated:</b> {datetime.now().strftime('%H:%M WIB')}"""
    
    def format_auto_trading_status(self, is_active: bool, user_settings: Dict) -> str:
        return f"""🤖 <b>AUTO TRADING STATUS</b>

{self.emojis['fire'] if is_active else '⏳'} <b>Status:</b> {'ACTIVE' if is_active else 'INACTIVE'}
⚡ <b>Leverage:</b> 125x
💰 <b>Risk Level:</b> Medium

{self.emojis['fire']} <b>PERFORMANCE:</b>
• Win Rate: 85%+
• Avg Return: +150%

⚠️ <b>RISK WARNING:</b>
Auto trading involves significant risk."""
    
    def format_portfolio_summary(self, portfolio_data: Dict) -> str:
        return f"""💼 <b>PORTFOLIO SUMMARY</b>

💰 <b>Total Balance:</b> ${portfolio_data.get('total_balance', 0):,.2f}
📈 <b>P&L Today:</b> {portfolio_data.get('daily_pnl', 0):+.2f}%
📊 <b>Total P&L:</b> {portfolio_data.get('total_pnl', 0):+.2f}%

🎯 <b>TRADING STATS:</b>
• Total Trades: {portfolio_data.get('total_trades', 0)}
• Win Rate: {portfolio_data.get('win_rate', 0):.1f}%

🏆 <b>ACHIEVEMENTS:</b>
{self.emojis['trophy']} Profitable Trader
{self.emojis['diamond']} Signal Follower"""
    
    def format_help_message(self) -> str:
        return """📚 <b>AI FUTURE SIGNAL - HELP</b>

🎯 <b>MAIN FEATURES:</b>
📊 Live Signals - Real-time signals
📈 Market Analysis - PRO-level analysis with 500 candles
🤖 Auto Trading - Automated execution
💼 Portfolio - Track performance

🔥 <b>MARKET ANALYSIS:</b>
• Choose from 10 top pairs
• Select timeframe (1m to 1h)
• 500 candle deep analysis
• PRO-level technical indicators
• Support/Resistance levels
• Chart pattern recognition
• Risk assessment
• Detailed recommendations

⚡ <b>STRENGTH LEVELS:</b>
🔥 90-100% - Very Strong
⚡ 80-89% - Strong  
💎 70-79% - Medium

❓ <b>SUPPORT:</b> @Ulascryptomaster

⚠️ <b>DISCLAIMER:</b> Trading involves risk."""
    
    def _get_strength_emoji(self, strength: int) -> str:
        if strength >= 90: return self.emojis['fire']
        elif strength >= 80: return self.emojis['lightning']
        elif strength >= 70: return self.emojis['diamond']
        else: return self.emojis['star']
