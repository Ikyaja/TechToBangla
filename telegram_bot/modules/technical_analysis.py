"""
Advanced Technical Analysis Module
Comprehensive technical indicators and market analysis
"""

import pandas as pd
import numpy as np
import ta
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TechnicalAnalyzer:
    def __init__(self):
        self.indicators = {}
        
    def calculate_all_indicators(self, df: pd.DataFrame) -> Dict:
        """Calculate all technical indicators for the given data"""
        try:
            if df is None or df.empty:
                return {}
            
            indicators = {}
            
            # Price-based indicators
            indicators.update(self._calculate_trend_indicators(df))
            indicators.update(self._calculate_momentum_indicators(df))
            indicators.update(self._calculate_volatility_indicators(df))
            indicators.update(self._calculate_volume_indicators(df))
            indicators.update(self._calculate_support_resistance(df))
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return {}
    
    def _calculate_trend_indicators(self, df: pd.DataFrame) -> Dict:
        """Calculate trend-following indicators"""
        indicators = {}
        
        try:
            # Moving Averages
            indicators['sma_20'] = ta.trend.sma_indicator(df['close'], window=20)
            indicators['sma_50'] = ta.trend.sma_indicator(df['close'], window=50)
            indicators['ema_12'] = ta.trend.ema_indicator(df['close'], window=12)
            indicators['ema_26'] = ta.trend.ema_indicator(df['close'], window=26)
            
            # MACD
            macd = ta.trend.MACD(df['close'])
            indicators['macd'] = macd.macd()
            indicators['macd_signal'] = macd.macd_signal()
            indicators['macd_histogram'] = macd.macd_diff()
            
            # ADX (Average Directional Index)
            indicators['adx'] = ta.trend.adx(df['high'], df['low'], df['close'])
            indicators['adx_pos'] = ta.trend.adx_pos(df['high'], df['low'], df['close'])
            indicators['adx_neg'] = ta.trend.adx_neg(df['high'], df['low'], df['close'])
            
            # Parabolic SAR
            indicators['psar'] = ta.trend.psar_down(df['high'], df['low'], df['close'])
            
            # Ichimoku
            ichimoku = ta.trend.IchimokuIndicator(df['high'], df['low'])
            indicators['ichimoku_a'] = ichimoku.ichimoku_a()
            indicators['ichimoku_b'] = ichimoku.ichimoku_b()
            
        except Exception as e:
            logger.error(f"Error calculating trend indicators: {e}")
        
        return indicators
    
    def _calculate_momentum_indicators(self, df: pd.DataFrame) -> Dict:
        """Calculate momentum oscillators"""
        indicators = {}
        
        try:
            # RSI
            indicators['rsi'] = ta.momentum.rsi(df['close'], window=14)
            
            # Stochastic
            stoch = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close'])
            indicators['stoch_k'] = stoch.stoch()
            indicators['stoch_d'] = stoch.stoch_signal()
            
            # Williams %R
            indicators['williams_r'] = ta.momentum.williams_r(df['high'], df['low'], df['close'])
            
            # CCI (Commodity Channel Index)
            indicators['cci'] = ta.trend.cci(df['high'], df['low'], df['close'])
            
            # ROC (Rate of Change)
            indicators['roc'] = ta.momentum.roc(df['close'])
            
            # MFI (Money Flow Index)
            if 'volume' in df.columns:
                indicators['mfi'] = ta.volume.money_flow_index(
                    df['high'], df['low'], df['close'], df['volume']
                )
            
        except Exception as e:
            logger.error(f"Error calculating momentum indicators: {e}")
        
        return indicators
    
    def _calculate_volatility_indicators(self, df: pd.DataFrame) -> Dict:
        """Calculate volatility indicators"""
        indicators = {}
        
        try:
            # Bollinger Bands
            bb = ta.volatility.BollingerBands(df['close'])
            indicators['bb_upper'] = bb.bollinger_hband()
            indicators['bb_middle'] = bb.bollinger_mavg()
            indicators['bb_lower'] = bb.bollinger_lband()
            indicators['bb_width'] = bb.bollinger_wband()
            indicators['bb_percent'] = bb.bollinger_pband()
            
            # Average True Range
            indicators['atr'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'])
            
            # Keltner Channels
            kc = ta.volatility.KeltnerChannel(df['high'], df['low'], df['close'])
            indicators['kc_upper'] = kc.keltner_channel_hband()
            indicators['kc_middle'] = kc.keltner_channel_mband()
            indicators['kc_lower'] = kc.keltner_channel_lband()
            
        except Exception as e:
            logger.error(f"Error calculating volatility indicators: {e}")
        
        return indicators
    
    def _calculate_volume_indicators(self, df: pd.DataFrame) -> Dict:
        """Calculate volume-based indicators"""
        indicators = {}
        
        try:
            if 'volume' not in df.columns:
                return indicators
            
            # On-Balance Volume
            indicators['obv'] = ta.volume.on_balance_volume(df['close'], df['volume'])
            
            # Volume SMA
            indicators['volume_sma'] = ta.trend.sma_indicator(df['volume'], window=20)
            
            # Accumulation/Distribution Line
            indicators['ad_line'] = ta.volume.acc_dist_index(df['high'], df['low'], df['close'], df['volume'])
            
            # Chaikin Money Flow
            indicators['cmf'] = ta.volume.chaikin_money_flow(df['high'], df['low'], df['close'], df['volume'])
            
            # Volume Price Trend
            indicators['vpt'] = ta.volume.volume_price_trend(df['close'], df['volume'])
            
        except Exception as e:
            logger.error(f"Error calculating volume indicators: {e}")
        
        return indicators
    
    def _calculate_support_resistance(self, df: pd.DataFrame) -> Dict:
        """Calculate support and resistance levels"""
        indicators = {}
        
        try:
            # Pivot Points
            high = df['high'].iloc[-1]
            low = df['low'].iloc[-1]
            close = df['close'].iloc[-1]
            
            pivot = (high + low + close) / 3
            indicators['pivot'] = pivot
            indicators['r1'] = 2 * pivot - low
            indicators['s1'] = 2 * pivot - high
            indicators['r2'] = pivot + (high - low)
            indicators['s2'] = pivot - (high - low)
            indicators['r3'] = high + 2 * (pivot - low)
            indicators['s3'] = low - 2 * (high - pivot)
            
            # Dynamic Support/Resistance using moving averages
            indicators['dynamic_support'] = min(
                indicators.get('sma_20', close).iloc[-1] if hasattr(indicators.get('sma_20', close), 'iloc') else close,
                indicators.get('ema_12', close).iloc[-1] if hasattr(indicators.get('ema_12', close), 'iloc') else close
            )
            indicators['dynamic_resistance'] = max(
                indicators.get('sma_50', close).iloc[-1] if hasattr(indicators.get('sma_50', close), 'iloc') else close,
                indicators.get('ema_26', close).iloc[-1] if hasattr(indicators.get('ema_26', close), 'iloc') else close
            )
            
        except Exception as e:
            logger.error(f"Error calculating support/resistance: {e}")
        
        return indicators
    
    def analyze_trend(self, indicators: Dict, current_price: float) -> Dict:
        """Analyze overall trend direction and strength"""
        try:
            trend_signals = []
            trend_strength = 0
            
            # MACD Analysis
            if 'macd' in indicators and 'macd_signal' in indicators:
                macd_current = indicators['macd'].iloc[-1] if hasattr(indicators['macd'], 'iloc') else 0
                macd_signal_current = indicators['macd_signal'].iloc[-1] if hasattr(indicators['macd_signal'], 'iloc') else 0
                
                if macd_current > macd_signal_current:
                    trend_signals.append('bullish')
                    trend_strength += 1
                else:
                    trend_signals.append('bearish')
                    trend_strength -= 1
            
            # Moving Average Analysis
            if 'sma_20' in indicators and 'sma_50' in indicators:
                sma20 = indicators['sma_20'].iloc[-1] if hasattr(indicators['sma_20'], 'iloc') else current_price
                sma50 = indicators['sma_50'].iloc[-1] if hasattr(indicators['sma_50'], 'iloc') else current_price
                
                if sma20 > sma50 and current_price > sma20:
                    trend_signals.append('bullish')
                    trend_strength += 2
                elif sma20 < sma50 and current_price < sma20:
                    trend_signals.append('bearish')
                    trend_strength -= 2
            
            # ADX Analysis
            if 'adx' in indicators:
                adx_current = indicators['adx'].iloc[-1] if hasattr(indicators['adx'], 'iloc') else 0
                if adx_current > 25:
                    trend_strength += 1 if trend_strength > 0 else -1
            
            # Determine overall trend
            if trend_strength >= 2:
                overall_trend = 'strong_bullish'
            elif trend_strength == 1:
                overall_trend = 'weak_bullish'
            elif trend_strength == -1:
                overall_trend = 'weak_bearish'
            elif trend_strength <= -2:
                overall_trend = 'strong_bearish'
            else:
                overall_trend = 'sideways'
            
            return {
                'trend': overall_trend,
                'strength': abs(trend_strength),
                'signals': trend_signals,
                'confidence': min(abs(trend_strength) * 20, 100)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing trend: {e}")
            return {'trend': 'unknown', 'strength': 0, 'signals': [], 'confidence': 0}
    
    def detect_signals(self, indicators: Dict, current_price: float) -> List[Dict]:
        """Detect trading signals based on technical analysis"""
        signals = []
        
        try:
            # RSI Signals
            if 'rsi' in indicators:
                rsi_current = indicators['rsi'].iloc[-1] if hasattr(indicators['rsi'], 'iloc') else 50
                
                if rsi_current < 30:
                    signals.append({
                        'type': 'buy',
                        'indicator': 'RSI',
                        'strength': 'strong',
                        'reason': f'RSI oversold at {rsi_current:.2f}',
                        'confidence': 80
                    })
                elif rsi_current > 70:
                    signals.append({
                        'type': 'sell',
                        'indicator': 'RSI',
                        'strength': 'strong',
                        'reason': f'RSI overbought at {rsi_current:.2f}',
                        'confidence': 80
                    })
            
            # Bollinger Bands Signals
            if all(key in indicators for key in ['bb_upper', 'bb_lower', 'bb_percent']):
                bb_percent = indicators['bb_percent'].iloc[-1] if hasattr(indicators['bb_percent'], 'iloc') else 0.5
                
                if bb_percent < 0.1:
                    signals.append({
                        'type': 'buy',
                        'indicator': 'Bollinger Bands',
                        'strength': 'medium',
                        'reason': 'Price near lower Bollinger Band',
                        'confidence': 65
                    })
                elif bb_percent > 0.9:
                    signals.append({
                        'type': 'sell',
                        'indicator': 'Bollinger Bands',
                        'strength': 'medium',
                        'reason': 'Price near upper Bollinger Band',
                        'confidence': 65
                    })
            
            # MACD Crossover Signals
            if all(key in indicators for key in ['macd', 'macd_signal']):
                macd_current = indicators['macd'].iloc[-1] if hasattr(indicators['macd'], 'iloc') else 0
                macd_signal_current = indicators['macd_signal'].iloc[-1] if hasattr(indicators['macd_signal'], 'iloc') else 0
                macd_prev = indicators['macd'].iloc[-2] if hasattr(indicators['macd'], 'iloc') and len(indicators['macd']) > 1 else 0
                macd_signal_prev = indicators['macd_signal'].iloc[-2] if hasattr(indicators['macd_signal'], 'iloc') and len(indicators['macd_signal']) > 1 else 0
                
                # Bullish crossover
                if macd_prev <= macd_signal_prev and macd_current > macd_signal_current:
                    signals.append({
                        'type': 'buy',
                        'indicator': 'MACD',
                        'strength': 'strong',
                        'reason': 'MACD bullish crossover',
                        'confidence': 75
                    })
                # Bearish crossover
                elif macd_prev >= macd_signal_prev and macd_current < macd_signal_current:
                    signals.append({
                        'type': 'sell',
                        'indicator': 'MACD',
                        'strength': 'strong',
                        'reason': 'MACD bearish crossover',
                        'confidence': 75
                    })
            
            # Stochastic Signals
            if 'stoch_k' in indicators:
                stoch_k = indicators['stoch_k'].iloc[-1] if hasattr(indicators['stoch_k'], 'iloc') else 50
                
                if stoch_k < 20:
                    signals.append({
                        'type': 'buy',
                        'indicator': 'Stochastic',
                        'strength': 'medium',
                        'reason': f'Stochastic oversold at {stoch_k:.2f}',
                        'confidence': 60
                    })
                elif stoch_k > 80:
                    signals.append({
                        'type': 'sell',
                        'indicator': 'Stochastic',
                        'strength': 'medium',
                        'reason': f'Stochastic overbought at {stoch_k:.2f}',
                        'confidence': 60
                    })
            
        except Exception as e:
            logger.error(f"Error detecting signals: {e}")
        
        return signals
    
    def calculate_signal_strength(self, signals: List[Dict]) -> int:
        """Calculate overall signal strength (0-100)"""
        try:
            if not signals:
                return 0
            
            buy_signals = [s for s in signals if s['type'] == 'buy']
            sell_signals = [s for s in signals if s['type'] == 'sell']
            
            buy_strength = sum(s['confidence'] for s in buy_signals)
            sell_strength = sum(s['confidence'] for s in sell_signals)
            
            # Normalize to 0-100 scale
            max_strength = max(buy_strength, sell_strength)
            if max_strength == 0:
                return 0
            
            return min(int(max_strength / len(signals)), 100)
            
        except Exception as e:
            logger.error(f"Error calculating signal strength: {e}")
            return 0
    
    def get_entry_exit_levels(self, indicators: Dict, current_price: float, signal_type: str) -> Dict:
        """Calculate entry, stop loss, and take profit levels"""
        try:
            atr = indicators.get('atr', pd.Series([current_price * 0.02])).iloc[-1] if 'atr' in indicators else current_price * 0.02
            
            if signal_type == 'buy':
                entry = current_price
                stop_loss = entry - (2 * atr)
                take_profit_1 = entry + (1.5 * atr)
                take_profit_2 = entry + (3 * atr)
                take_profit_3 = entry + (4.5 * atr)
            else:  # sell
                entry = current_price
                stop_loss = entry + (2 * atr)
                take_profit_1 = entry - (1.5 * atr)
                take_profit_2 = entry - (3 * atr)
                take_profit_3 = entry - (4.5 * atr)
            
            return {
                'entry': round(entry, 8),
                'stop_loss': round(stop_loss, 8),
                'take_profit_1': round(take_profit_1, 8),
                'take_profit_2': round(take_profit_2, 8),
                'take_profit_3': round(take_profit_3, 8),
                'risk_reward_1': round(abs(take_profit_1 - entry) / abs(entry - stop_loss), 2),
                'risk_reward_2': round(abs(take_profit_2 - entry) / abs(entry - stop_loss), 2),
                'risk_reward_3': round(abs(take_profit_3 - entry) / abs(entry - stop_loss), 2)
            }
            
        except Exception as e:
            logger.error(f"Error calculating entry/exit levels: {e}")
            return {}
    
    async def get_market_overview(self) -> Dict:
        """Get comprehensive market overview"""
        try:
            # This would typically fetch data from multiple sources
            # For now, return a basic structure
            return {
                'market_sentiment': 'neutral',
                'volatility': 'medium',
                'volume_trend': 'increasing',
                'major_levels': {
                    'support': [],
                    'resistance': []
                },
                'sector_performance': {},
                'fear_greed_index': 50,
                'timestamp': datetime.now()
            }
        except Exception as e:
            logger.error(f"Error getting market overview: {e}")
            return {}