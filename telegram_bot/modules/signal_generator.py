"""
Advanced Signal Generation System
Generates high-quality trading signals based on technical analysis
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
import numpy as np

from .binance_client import BinanceClient
from .technical_analysis import TechnicalAnalyzer

logger = logging.getLogger(__name__)

class SignalGenerator:
    def __init__(self, binance_client: BinanceClient, technical_analyzer: TechnicalAnalyzer):
        self.binance_client = binance_client
        self.technical_analyzer = technical_analyzer
        self.active_signals = {}
        self.signal_history = []
        
        # Signal configuration
        self.min_signal_strength = 70
        self.max_signals_per_hour = 5
        self.timeframes = ['1h', '4h', '1d']
        
        # Top symbols to monitor
        self.monitored_symbols = [
            'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'XRPUSDT',
            'SOLUSDT', 'DOTUSDT', 'AVAXUSDT', 'MATICUSDT', 'LINKUSDT',
            'UNIUSDT', 'LTCUSDT', 'BCHUSDT', 'FILUSDT', 'TRXUSDT',
            'ETCUSDT', 'XLMUSDT', 'VETUSDT', 'ICPUSDT', 'FTMUSDT'
        ]
    
    async def scan_for_signals(self) -> List[Dict]:
        """Scan all monitored symbols for trading signals"""
        new_signals = []
        
        try:
            # Check rate limiting
            if self._is_rate_limited():
                logger.info("Signal generation rate limited")
                return []
            
            # Scan each symbol
            for symbol in self.monitored_symbols:
                try:
                    signal = await self._analyze_symbol_for_signals(symbol)
                    if signal and signal['strength'] >= self.min_signal_strength:
                        new_signals.append(signal)
                        
                    # Add small delay to avoid rate limits
                    await asyncio.sleep(0.1)
                    
                except Exception as e:
                    logger.error(f"Error analyzing {symbol}: {e}")
                    continue
            
            # Sort by signal strength
            new_signals.sort(key=lambda x: x['strength'], reverse=True)
            
            # Limit number of signals
            new_signals = new_signals[:self.max_signals_per_hour]
            
            # Update signal history
            for signal in new_signals:
                self.signal_history.append(signal)
                self.active_signals[signal['id']] = signal
            
            # Clean old signals
            self._clean_old_signals()
            
            logger.info(f"Generated {len(new_signals)} new signals")
            return new_signals
            
        except Exception as e:
            logger.error(f"Error scanning for signals: {e}")
            return []
    
    async def _analyze_symbol_for_signals(self, symbol: str) -> Optional[Dict]:
        """Analyze a single symbol for trading signals"""
        try:
            # Get market data for multiple timeframes
            signal_data = {}
            
            for timeframe in self.timeframes:
                df = await self.binance_client.get_klines(symbol, timeframe, 100)
                if df is None or df.empty:
                    continue
                
                # Calculate technical indicators
                indicators = self.technical_analyzer.calculate_all_indicators(df)
                current_price = df['close'].iloc[-1]
                
                # Analyze trend
                trend_analysis = self.technical_analyzer.analyze_trend(indicators, current_price)
                
                # Detect signals
                signals = self.technical_analyzer.detect_signals(indicators, current_price)
                
                signal_data[timeframe] = {
                    'indicators': indicators,
                    'trend': trend_analysis,
                    'signals': signals,
                    'price': current_price
                }
            
            # Combine multi-timeframe analysis
            combined_signal = self._combine_timeframe_signals(symbol, signal_data)
            
            return combined_signal
            
        except Exception as e:
            logger.error(f"Error analyzing {symbol}: {e}")
            return None
    
    def _combine_timeframe_signals(self, symbol: str, signal_data: Dict) -> Optional[Dict]:
        """Combine signals from multiple timeframes"""
        try:
            if not signal_data:
                return None
            
            # Get the most recent price
            current_price = None
            for timeframe in self.timeframes:
                if timeframe in signal_data:
                    current_price = signal_data[timeframe]['price']
                    break
            
            if current_price is None:
                return None
            
            # Analyze signal consensus across timeframes
            buy_votes = 0
            sell_votes = 0
            total_confidence = 0
            signal_reasons = []
            
            for timeframe, data in signal_data.items():
                signals = data.get('signals', [])
                trend = data.get('trend', {})
                
                # Weight signals by timeframe (longer timeframes have more weight)
                weight = {'1h': 1, '4h': 2, '1d': 3}.get(timeframe, 1)
                
                for signal in signals:
                    if signal['type'] == 'buy':
                        buy_votes += weight
                        total_confidence += signal['confidence'] * weight
                    else:
                        sell_votes += weight
                        total_confidence += signal['confidence'] * weight
                    
                    signal_reasons.append(f"{timeframe}: {signal['reason']}")
                
                # Add trend analysis
                trend_type = trend.get('trend', 'sideways')
                if 'bullish' in trend_type:
                    buy_votes += weight * 0.5
                elif 'bearish' in trend_type:
                    sell_votes += weight * 0.5
            
            # Determine signal direction and strength
            if buy_votes > sell_votes and buy_votes >= 3:
                signal_type = 'LONG'
                signal_strength = min(int(total_confidence / max(buy_votes + sell_votes, 1)), 100)
            elif sell_votes > buy_votes and sell_votes >= 3:
                signal_type = 'SHORT'
                signal_strength = min(int(total_confidence / max(buy_votes + sell_votes, 1)), 100)
            else:
                return None  # No clear signal
            
            # Calculate entry and exit levels
            main_indicators = signal_data.get('1h', {}).get('indicators', {})
            levels = self.technical_analyzer.get_entry_exit_levels(
                main_indicators, current_price, signal_type.lower()
            )
            
            # Generate signal ID
            signal_id = f"{symbol}_{signal_type}_{int(datetime.now().timestamp())}"
            
            # Create signal object
            signal = {
                'id': signal_id,
                'symbol': symbol,
                'type': signal_type,
                'strength': signal_strength,
                'price': current_price,
                'entry': levels.get('entry', current_price),
                'stop_loss': levels.get('stop_loss', current_price * 0.98 if signal_type == 'LONG' else current_price * 1.02),
                'take_profit_1': levels.get('take_profit_1', current_price * 1.02 if signal_type == 'LONG' else current_price * 0.98),
                'take_profit_2': levels.get('take_profit_2', current_price * 1.04 if signal_type == 'LONG' else current_price * 0.96),
                'take_profit_3': levels.get('take_profit_3', current_price * 1.06 if signal_type == 'LONG' else current_price * 0.94),
                'risk_reward_1': levels.get('risk_reward_1', 1.5),
                'risk_reward_2': levels.get('risk_reward_2', 2.0),
                'risk_reward_3': levels.get('risk_reward_3', 2.5),
                'reasons': signal_reasons[:3],  # Top 3 reasons
                'timeframes': list(signal_data.keys()),
                'timestamp': datetime.now(),
                'status': 'active'
            }
            
            return signal
            
        except Exception as e:
            logger.error(f"Error combining timeframe signals: {e}")
            return None
    
    async def get_latest_signals(self, limit: int = 10) -> List[Dict]:
        """Get the latest active signals"""
        try:
            # Filter active signals from last 24 hours
            cutoff_time = datetime.now() - timedelta(hours=24)
            recent_signals = [
                signal for signal in self.signal_history
                if signal['timestamp'] > cutoff_time and signal['status'] == 'active'
            ]
            
            # Sort by timestamp (newest first)
            recent_signals.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return recent_signals[:limit]
            
        except Exception as e:
            logger.error(f"Error getting latest signals: {e}")
            return []
    
    async def update_signal_status(self, signal_id: str, status: str, hit_level: Optional[str] = None):
        """Update the status of a signal"""
        try:
            if signal_id in self.active_signals:
                self.active_signals[signal_id]['status'] = status
                if hit_level:
                    self.active_signals[signal_id]['hit_level'] = hit_level
                    self.active_signals[signal_id]['hit_time'] = datetime.now()
                
                # Update in history as well
                for signal in self.signal_history:
                    if signal['id'] == signal_id:
                        signal['status'] = status
                        if hit_level:
                            signal['hit_level'] = hit_level
                            signal['hit_time'] = datetime.now()
                        break
                
                logger.info(f"Updated signal {signal_id} status to {status}")
                
        except Exception as e:
            logger.error(f"Error updating signal status: {e}")
    
    def _is_rate_limited(self) -> bool:
        """Check if signal generation is rate limited"""
        try:
            current_time = datetime.now()
            hour_ago = current_time - timedelta(hours=1)
            
            recent_signals = [
                signal for signal in self.signal_history
                if signal['timestamp'] > hour_ago
            ]
            
            return len(recent_signals) >= self.max_signals_per_hour
            
        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
            return False
    
    def _clean_old_signals(self):
        """Clean up old signals from memory"""
        try:
            cutoff_time = datetime.now() - timedelta(days=7)
            
            # Remove old signals from history
            self.signal_history = [
                signal for signal in self.signal_history
                if signal['timestamp'] > cutoff_time
            ]
            
            # Remove old active signals
            old_signal_ids = [
                signal_id for signal_id, signal in self.active_signals.items()
                if signal['timestamp'] < cutoff_time
            ]
            
            for signal_id in old_signal_ids:
                del self.active_signals[signal_id]
            
            logger.info(f"Cleaned {len(old_signal_ids)} old signals")
            
        except Exception as e:
            logger.error(f"Error cleaning old signals: {e}")
    
    async def get_signal_performance(self) -> Dict:
        """Calculate performance statistics of generated signals"""
        try:
            if not self.signal_history:
                return {'total_signals': 0, 'win_rate': 0, 'avg_return': 0}
            
            completed_signals = [
                signal for signal in self.signal_history
                if signal.get('status') in ['hit_tp1', 'hit_tp2', 'hit_tp3', 'hit_sl']
            ]
            
            if not completed_signals:
                return {'total_signals': len(self.signal_history), 'win_rate': 0, 'avg_return': 0}
            
            winning_signals = [
                signal for signal in completed_signals
                if signal.get('status').startswith('hit_tp')
            ]
            
            win_rate = len(winning_signals) / len(completed_signals) * 100
            
            # Calculate average return (simplified)
            total_return = 0
            for signal in completed_signals:
                if signal.get('status') == 'hit_tp1':
                    total_return += signal.get('risk_reward_1', 1.5)
                elif signal.get('status') == 'hit_tp2':
                    total_return += signal.get('risk_reward_2', 2.0)
                elif signal.get('status') == 'hit_tp3':
                    total_return += signal.get('risk_reward_3', 2.5)
                else:  # Stop loss
                    total_return -= 1.0
            
            avg_return = total_return / len(completed_signals)
            
            return {
                'total_signals': len(self.signal_history),
                'completed_signals': len(completed_signals),
                'winning_signals': len(winning_signals),
                'win_rate': round(win_rate, 2),
                'avg_return': round(avg_return, 2),
                'active_signals': len([s for s in self.signal_history if s.get('status') == 'active'])
            }
            
        except Exception as e:
            logger.error(f"Error calculating signal performance: {e}")
            return {'total_signals': 0, 'win_rate': 0, 'avg_return': 0}