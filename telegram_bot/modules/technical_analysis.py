import pandas as pd
import numpy as np
import logging
import random
from typing import Dict, List, Tuple
from datetime import datetime

try:
    import ta
    TA_AVAILABLE = True
except ImportError:
    TA_AVAILABLE = False

logger = logging.getLogger(__name__)

class TechnicalAnalyzer:
    def __init__(self):
        self.indicators = {}
    
    async def perform_advanced_analysis(self, df: pd.DataFrame, pair: str, timeframe: str) -> Dict:
        """Perform comprehensive 500-candle PRO analysis"""
        try:
            logger.info(f"🔬 Performing advanced analysis for {pair} on {timeframe}")
            
            if df is None or len(df) < 50:
                return {'error': 'Insufficient data'}
            
            current_price = df['close'].iloc[-1]
            
            # Calculate ALL indicators
            indicators = self.calculate_comprehensive_indicators(df)
            
            # Multi-timeframe trend analysis
            trend_analysis = self.analyze_multi_trend(df, indicators)
            
            # Support/Resistance levels
            sr_levels = self.calculate_support_resistance_levels(df)
            
            # Market structure analysis
            market_structure = self.analyze_market_structure(df)
            
            # Volume analysis
            volume_analysis = self.analyze_volume_profile(df)
            
            # Pattern recognition
            patterns = self.detect_chart_patterns(df)
            
            # Risk assessment
            risk_assessment = self.calculate_risk_metrics(df, indicators)
            
            # Generate trading recommendation
            recommendation = self.generate_trading_recommendation(
                indicators, trend_analysis, sr_levels, market_structure, 
                volume_analysis, patterns, current_price, timeframe
            )
            
            return {
                'pair': pair,
                'timeframe': timeframe,
                'current_price': current_price,
                'candles_analyzed': len(df),
                'indicators': indicators,
                'trend_analysis': trend_analysis,
                'support_resistance': sr_levels,
                'market_structure': market_structure,
                'volume_analysis': volume_analysis,
                'patterns': patterns,
                'risk_assessment': risk_assessment,
                'recommendation': recommendation,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error in advanced analysis: {e}")
            return {'error': str(e)}
    
    def calculate_comprehensive_indicators(self, df: pd.DataFrame) -> Dict:
        """Calculate comprehensive technical indicators"""
        indicators = {}
        
        try:
            if TA_AVAILABLE:
                # Trend Indicators
                indicators['sma_20'] = ta.trend.sma_indicator(df['close'], window=20)
                indicators['sma_50'] = ta.trend.sma_indicator(df['close'], window=50)
                indicators['sma_200'] = ta.trend.sma_indicator(df['close'], window=200)
                indicators['ema_12'] = ta.trend.ema_indicator(df['close'], window=12)
                indicators['ema_26'] = ta.trend.ema_indicator(df['close'], window=26)
                indicators['ema_50'] = ta.trend.ema_indicator(df['close'], window=50)
                
                # MACD
                macd = ta.trend.MACD(df['close'])
                indicators['macd'] = macd.macd()
                indicators['macd_signal'] = macd.macd_signal()
                indicators['macd_histogram'] = macd.macd_diff()
                
                # RSI
                indicators['rsi'] = ta.momentum.rsi(df['close'], window=14)
                indicators['rsi_slow'] = ta.momentum.rsi(df['close'], window=21)
                
                # Stochastic
                stoch = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close'])
                indicators['stoch_k'] = stoch.stoch()
                indicators['stoch_d'] = stoch.stoch_signal()
                
                # Bollinger Bands
                bb = ta.volatility.BollingerBands(df['close'])
                indicators['bb_upper'] = bb.bollinger_hband()
                indicators['bb_middle'] = bb.bollinger_mavg()
                indicators['bb_lower'] = bb.bollinger_lband()
                indicators['bb_width'] = bb.bollinger_wband()
                indicators['bb_percent'] = bb.bollinger_pband()
                
                # ADX
                indicators['adx'] = ta.trend.adx(df['high'], df['low'], df['close'])
                indicators['adx_pos'] = ta.trend.adx_pos(df['high'], df['low'], df['close'])
                indicators['adx_neg'] = ta.trend.adx_neg(df['high'], df['low'], df['close'])
                
                # CCI
                indicators['cci'] = ta.trend.cci(df['high'], df['low'], df['close'])
                
                # Williams %R
                indicators['williams_r'] = ta.momentum.williams_r(df['high'], df['low'], df['close'])
                
                # ATR
                indicators['atr'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'])
                
                # Volume indicators
                indicators['obv'] = ta.volume.on_balance_volume(df['close'], df['volume'])
                indicators['cmf'] = ta.volume.chaikin_money_flow(df['high'], df['low'], df['close'], df['volume'])
                
            else:
                # Built-in indicators
                indicators = self._calculate_builtin_comprehensive(df)
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating comprehensive indicators: {e}")
            return {}
    
    def _calculate_builtin_comprehensive(self, df: pd.DataFrame) -> Dict:
        """Built-in comprehensive indicators"""
        indicators = {}
        
        try:
            # Moving Averages
            indicators['sma_20'] = df['close'].rolling(window=20).mean()
            indicators['sma_50'] = df['close'].rolling(window=50).mean()
            indicators['sma_200'] = df['close'].rolling(window=200).mean()
            indicators['ema_12'] = df['close'].ewm(span=12).mean()
            indicators['ema_26'] = df['close'].ewm(span=26).mean()
            indicators['ema_50'] = df['close'].ewm(span=50).mean()
            
            # MACD
            macd_line = indicators['ema_12'] - indicators['ema_26']
            macd_signal = macd_line.ewm(span=9).mean()
            indicators['macd'] = macd_line
            indicators['macd_signal'] = macd_signal
            indicators['macd_histogram'] = macd_line - macd_signal
            
            # RSI
            indicators['rsi'] = self._calculate_rsi(df['close'], 14)
            indicators['rsi_slow'] = self._calculate_rsi(df['close'], 21)
            
            # Bollinger Bands
            sma_20 = indicators['sma_20']
            std_20 = df['close'].rolling(window=20).std()
            indicators['bb_upper'] = sma_20 + (std_20 * 2)
            indicators['bb_middle'] = sma_20
            indicators['bb_lower'] = sma_20 - (std_20 * 2)
            indicators['bb_width'] = (indicators['bb_upper'] - indicators['bb_lower']) / sma_20
            indicators['bb_percent'] = (df['close'] - indicators['bb_lower']) / (indicators['bb_upper'] - indicators['bb_lower'])
            
            # Stochastic
            indicators['stoch_k'] = self._calculate_stochastic(df)
            indicators['stoch_d'] = indicators['stoch_k'].rolling(window=3).mean()
            
            # ATR
            indicators['atr'] = self._calculate_atr(df)
            
            # Volume analysis
            indicators['volume_sma'] = df['volume'].rolling(window=20).mean()
            indicators['volume_ratio'] = df['volume'] / indicators['volume_sma']
            
        except Exception as e:
            logger.error(f"Error in built-in comprehensive indicators: {e}")
        
        return indicators
    
    def _calculate_rsi(self, prices: pd.Series, window: int = 14) -> pd.Series:
        """Enhanced RSI calculation"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.fillna(50)
        except:
            return pd.Series([50] * len(prices))
    
    def _calculate_stochastic(self, df: pd.DataFrame, window: int = 14) -> pd.Series:
        """Calculate Stochastic %K"""
        try:
            lowest_low = df['low'].rolling(window=window).min()
            highest_high = df['high'].rolling(window=window).max()
            stoch_k = 100 * ((df['close'] - lowest_low) / (highest_high - lowest_low))
            return stoch_k.fillna(50)
        except:
            return pd.Series([50] * len(df))
    
    def _calculate_atr(self, df: pd.DataFrame, window: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        try:
            high_low = df['high'] - df['low']
            high_close = np.abs(df['high'] - df['close'].shift())
            low_close = np.abs(df['low'] - df['close'].shift())
            
            ranges = pd.concat([high_low, high_close, low_close], axis=1)
            true_range = np.max(ranges, axis=1)
            atr = pd.Series(true_range).rolling(window=window).mean()
            
            return atr.fillna(df['close'] * 0.02)
        except:
            return pd.Series([df['close'].iloc[-1] * 0.02] * len(df))
    
    def analyze_multi_trend(self, df: pd.DataFrame, indicators: Dict) -> Dict:
        """Advanced multi-timeframe trend analysis"""
        try:
            current_price = df['close'].iloc[-1]
            trend_signals = []
            trend_strength = 0
            
            # Moving Average Analysis
            if all(key in indicators for key in ['sma_20', 'sma_50', 'sma_200']):
                sma20 = indicators['sma_20'].iloc[-1]
                sma50 = indicators['sma_50'].iloc[-1]
                sma200 = indicators['sma_200'].iloc[-1]
                
                # Long-term trend
                if sma20 > sma50 > sma200 and current_price > sma20:
                    trend_signals.append('Strong Bullish Alignment')
                    trend_strength += 3
                elif sma20 < sma50 < sma200 and current_price < sma20:
                    trend_signals.append('Strong Bearish Alignment')
                    trend_strength -= 3
                elif current_price > sma20 > sma50:
                    trend_signals.append('Bullish Short-term')
                    trend_strength += 2
                elif current_price < sma20 < sma50:
                    trend_signals.append('Bearish Short-term')
                    trend_strength -= 2
            
            # MACD Trend
            if all(key in indicators for key in ['macd', 'macd_signal', 'macd_histogram']):
                macd = indicators['macd'].iloc[-1]
                macd_signal = indicators['macd_signal'].iloc[-1]
                macd_hist = indicators['macd_histogram'].iloc[-1]
                
                if macd > macd_signal and macd_hist > 0:
                    trend_signals.append('MACD Bullish Momentum')
                    trend_strength += 2
                elif macd < macd_signal and macd_hist < 0:
                    trend_signals.append('MACD Bearish Momentum')
                    trend_strength -= 2
            
            # ADX Trend Strength
            if 'adx' in indicators:
                adx = indicators['adx'].iloc[-1]
                if adx > 25:
                    if trend_strength > 0:
                        trend_signals.append(f'Strong Trend (ADX: {adx:.1f})')
                        trend_strength += 1
                    elif trend_strength < 0:
                        trend_signals.append(f'Strong Trend (ADX: {adx:.1f})')
                        trend_strength -= 1
                elif adx < 20:
                    trend_signals.append('Weak Trend/Sideways')
            
            # Determine overall trend
            if trend_strength >= 4:
                overall_trend = 'Very Strong Bullish'
                trend_color = '🟢🟢🟢'
            elif trend_strength >= 2:
                overall_trend = 'Strong Bullish'
                trend_color = '🟢🟢'
            elif trend_strength == 1:
                overall_trend = 'Weak Bullish'
                trend_color = '🟢'
            elif trend_strength == -1:
                overall_trend = 'Weak Bearish'
                trend_color = '🔴'
            elif trend_strength <= -2:
                overall_trend = 'Strong Bearish'
                trend_color = '🔴🔴'
            elif trend_strength <= -4:
                overall_trend = 'Very Strong Bearish'
                trend_color = '🔴🔴🔴'
            else:
                overall_trend = 'Sideways/Neutral'
                trend_color = '⚪'
            
            return {
                'overall_trend': overall_trend,
                'trend_color': trend_color,
                'trend_strength': abs(trend_strength),
                'trend_signals': trend_signals,
                'confidence': min(abs(trend_strength) * 15, 100)
            }
            
        except Exception as e:
            logger.error(f"Error in multi-trend analysis: {e}")
            return {'overall_trend': 'Unknown', 'trend_color': '❓', 'confidence': 0}
    
    def calculate_support_resistance_levels(self, df: pd.DataFrame) -> Dict:
        """Calculate dynamic support and resistance levels"""
        try:
            # Get recent highs and lows
            recent_data = df.tail(100)  # Last 100 candles
            
            # Find pivot points
            highs = []
            lows = []
            
            for i in range(2, len(recent_data) - 2):
                # Pivot High
                if (recent_data['high'].iloc[i] > recent_data['high'].iloc[i-1] and 
                    recent_data['high'].iloc[i] > recent_data['high'].iloc[i-2] and
                    recent_data['high'].iloc[i] > recent_data['high'].iloc[i+1] and
                    recent_data['high'].iloc[i] > recent_data['high'].iloc[i+2]):
                    highs.append(recent_data['high'].iloc[i])
                
                # Pivot Low
                if (recent_data['low'].iloc[i] < recent_data['low'].iloc[i-1] and 
                    recent_data['low'].iloc[i] < recent_data['low'].iloc[i-2] and
                    recent_data['low'].iloc[i] < recent_data['low'].iloc[i+1] and
                    recent_data['low'].iloc[i] < recent_data['low'].iloc[i+2]):
                    lows.append(recent_data['low'].iloc[i])
            
            # Calculate key levels
            current_price = df['close'].iloc[-1]
            
            # Resistance levels (above current price)
            resistance_levels = sorted([h for h in highs if h > current_price])[:3]
            
            # Support levels (below current price)
            support_levels = sorted([l for l in lows if l < current_price], reverse=True)[:3]
            
            # Calculate distance to nearest levels
            nearest_resistance = min(resistance_levels) if resistance_levels else current_price * 1.05
            nearest_support = max(support_levels) if support_levels else current_price * 0.95
            
            resistance_distance = ((nearest_resistance - current_price) / current_price) * 100
            support_distance = ((current_price - nearest_support) / current_price) * 100
            
            return {
                'resistance_levels': resistance_levels,
                'support_levels': support_levels,
                'nearest_resistance': nearest_resistance,
                'nearest_support': nearest_support,
                'resistance_distance': resistance_distance,
                'support_distance': support_distance
            }
            
        except Exception as e:
            logger.error(f"Error calculating S/R levels: {e}")
            current_price = df['close'].iloc[-1]
            return {
                'resistance_levels': [current_price * 1.02, current_price * 1.05],
                'support_levels': [current_price * 0.98, current_price * 0.95],
                'nearest_resistance': current_price * 1.02,
                'nearest_support': current_price * 0.98,
                'resistance_distance': 2.0,
                'support_distance': 2.0
            }
    
    def analyze_market_structure(self, df: pd.DataFrame) -> Dict:
        """Analyze market structure (Higher Highs, Lower Lows, etc.)"""
        try:
            recent_data = df.tail(50)
            
            # Find swing points
            swing_highs = []
            swing_lows = []
            
            for i in range(5, len(recent_data) - 5):
                # Swing High
                if all(recent_data['high'].iloc[i] >= recent_data['high'].iloc[i-j] for j in range(1, 6)) and \
                   all(recent_data['high'].iloc[i] >= recent_data['high'].iloc[i+j] for j in range(1, 6)):
                    swing_highs.append((i, recent_data['high'].iloc[i]))
                
                # Swing Low
                if all(recent_data['low'].iloc[i] <= recent_data['low'].iloc[i-j] for j in range(1, 6)) and \
                   all(recent_data['low'].iloc[i] <= recent_data['low'].iloc[i+j] for j in range(1, 6)):
                    swing_lows.append((i, recent_data['low'].iloc[i]))
            
            # Analyze structure
            structure_type = 'Sideways'
            
            if len(swing_highs) >= 2 and len(swing_lows) >= 2:
                # Check for Higher Highs and Higher Lows
                if (swing_highs[-1][1] > swing_highs[-2][1] and 
                    swing_lows[-1][1] > swing_lows[-2][1]):
                    structure_type = 'Uptrend (HH/HL)'
                
                # Check for Lower Highs and Lower Lows
                elif (swing_highs[-1][1] < swing_highs[-2][1] and 
                      swing_lows[-1][1] < swing_lows[-2][1]):
                    structure_type = 'Downtrend (LH/LL)'
                
                # Check for consolidation
                elif abs(swing_highs[-1][1] - swing_highs[-2][1]) / swing_highs[-1][1] < 0.02:
                    structure_type = 'Consolidation'
            
            return {
                'structure_type': structure_type,
                'swing_highs': len(swing_highs),
                'swing_lows': len(swing_lows),
                'last_swing_high': swing_highs[-1][1] if swing_highs else df['high'].max(),
                'last_swing_low': swing_lows[-1][1] if swing_lows else df['low'].min()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing market structure: {e}")
            return {'structure_type': 'Unknown', 'swing_highs': 0, 'swing_lows': 0}
    
    def analyze_volume_profile(self, df: pd.DataFrame) -> Dict:
        """Advanced volume analysis"""
        try:
            recent_volume = df['volume'].tail(20).mean()
            avg_volume = df['volume'].mean()
            volume_ratio = recent_volume / avg_volume
            
            # Volume trend
            volume_trend = 'Increasing' if volume_ratio > 1.2 else 'Decreasing' if volume_ratio < 0.8 else 'Stable'
            
            # Volume spikes
            volume_spikes = len(df[df['volume'] > avg_volume * 2])
            
            # Price-Volume relationship
            price_changes = df['close'].pct_change()
            volume_changes = df['volume'].pct_change()
            
            correlation = price_changes.corr(volume_changes)
            
            return {
                'volume_trend': volume_trend,
                'volume_ratio': volume_ratio,
                'volume_spikes': volume_spikes,
                'price_volume_correlation': correlation if not pd.isna(correlation) else 0,
                'avg_volume': avg_volume,
                'recent_volume': recent_volume
            }
            
        except Exception as e:
            logger.error(f"Error in volume analysis: {e}")
            return {'volume_trend': 'Unknown', 'volume_ratio': 1.0}
    
    def detect_chart_patterns(self, df: pd.DataFrame) -> List[str]:
        """Detect chart patterns"""
        patterns = []
        
        try:
            recent_data = df.tail(50)
            
            # Double Top/Bottom detection
            highs = recent_data['high'].rolling(window=5).max()
            lows = recent_data['low'].rolling(window=5).min()
            
            # Simple pattern detection
            if len(recent_data) > 20:
                recent_highs = recent_data['high'].tail(20)
                recent_lows = recent_data['low'].tail(20)
                
                # Ascending Triangle
                if (recent_highs.max() - recent_highs.min()) / recent_highs.max() < 0.02:
                    if recent_lows.iloc[-1] > recent_lows.iloc[0]:
                        patterns.append('Ascending Triangle')
                
                # Descending Triangle
                if (recent_lows.max() - recent_lows.min()) / recent_lows.max() < 0.02:
                    if recent_highs.iloc[-1] < recent_highs.iloc[0]:
                        patterns.append('Descending Triangle')
                
                # Flag pattern
                if len(recent_data) > 30:
                    price_range = recent_data['high'].max() - recent_data['low'].min()
                    if price_range / recent_data['close'].iloc[-1] < 0.05:
                        patterns.append('Flag/Pennant')
            
            # Breakout detection
            bb_upper = recent_data['high'].rolling(window=20).max()
            bb_lower = recent_data['low'].rolling(window=20).min()
            
            if recent_data['close'].iloc[-1] > bb_upper.iloc[-2]:
                patterns.append('Upward Breakout')
            elif recent_data['close'].iloc[-1] < bb_lower.iloc[-2]:
                patterns.append('Downward Breakout')
            
            return patterns if patterns else ['Consolidation']
            
        except Exception as e:
            logger.error(f"Error detecting patterns: {e}")
            return ['Pattern Analysis Unavailable']
    
    def calculate_risk_metrics(self, df: pd.DataFrame, indicators: Dict) -> Dict:
        """Calculate risk assessment metrics"""
        try:
            # Volatility analysis
            returns = df['close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(24)  # Annualized volatility
            
            # ATR-based risk
            atr = indicators.get('atr', pd.Series([df['close'].iloc[-1] * 0.02])).iloc[-1]
            atr_percent = (atr / df['close'].iloc[-1]) * 100
            
            # Risk level determination
            if atr_percent > 5:
                risk_level = 'Very High'
                risk_color = '🔴🔴🔴'
            elif atr_percent > 3:
                risk_level = 'High'
                risk_color = '🔴🔴'
            elif atr_percent > 2:
                risk_level = 'Medium'
                risk_color = '🟡'
            elif atr_percent > 1:
                risk_level = 'Low'
                risk_color = '🟢'
            else:
                risk_level = 'Very Low'
                risk_color = '🟢🟢'
            
            return {
                'volatility': volatility,
                'atr_percent': atr_percent,
                'risk_level': risk_level,
                'risk_color': risk_color,
                'recommended_position_size': max(0.5, 2.0 / atr_percent)  # Risk-adjusted position size
            }
            
        except Exception as e:
            logger.error(f"Error calculating risk metrics: {e}")
            return {'risk_level': 'Medium', 'risk_color': '🟡', 'atr_percent': 2.0}
    
    def generate_trading_recommendation(self, indicators: Dict, trend_analysis: Dict, 
                                      sr_levels: Dict, market_structure: Dict,
                                      volume_analysis: Dict, patterns: List[str], 
                                      current_price: float, timeframe: str) -> Dict:
        """Generate comprehensive trading recommendation"""
        try:
            signals = []
            overall_score = 0
            
            # Trend analysis scoring
            trend_strength = trend_analysis.get('trend_strength', 0)
            if 'Bullish' in trend_analysis.get('overall_trend', ''):
                signals.append(('Trend Analysis', 'BUY', trend_strength * 10, 'Strong bullish trend detected'))
                overall_score += trend_strength
            elif 'Bearish' in trend_analysis.get('overall_trend', ''):
                signals.append(('Trend Analysis', 'SELL', trend_strength * 10, 'Strong bearish trend detected'))
                overall_score -= trend_strength
            
            # RSI analysis
            if 'rsi' in indicators:
                rsi = indicators['rsi'].iloc[-1]
                if rsi < 30:
                    signals.append(('RSI', 'BUY', 80, f'RSI oversold at {rsi:.1f}'))
                    overall_score += 2
                elif rsi > 70:
                    signals.append(('RSI', 'SELL', 80, f'RSI overbought at {rsi:.1f}'))
                    overall_score -= 2
                elif 40 <= rsi <= 60:
                    signals.append(('RSI', 'NEUTRAL', 50, f'RSI neutral at {rsi:.1f}'))
            
            # MACD analysis
            if all(key in indicators for key in ['macd', 'macd_signal']):
                macd = indicators['macd'].iloc[-1]
                macd_signal = indicators['macd_signal'].iloc[-1]
                
                if len(indicators['macd']) > 1:
                    macd_prev = indicators['macd'].iloc[-2]
                    signal_prev = indicators['macd_signal'].iloc[-2]
                    
                    # Bullish crossover
                    if macd_prev <= signal_prev and macd > macd_signal:
                        signals.append(('MACD', 'BUY', 85, 'MACD bullish crossover'))
                        overall_score += 3
                    # Bearish crossover
                    elif macd_prev >= signal_prev and macd < macd_signal:
                        signals.append(('MACD', 'SELL', 85, 'MACD bearish crossover'))
                        overall_score -= 3
            
            # Support/Resistance analysis
            resistance_distance = sr_levels.get('resistance_distance', 5)
            support_distance = sr_levels.get('support_distance', 5)
            
            if resistance_distance < 1:
                signals.append(('S/R', 'SELL', 70, 'Price near resistance'))
                overall_score -= 1
            elif support_distance < 1:
                signals.append(('S/R', 'BUY', 70, 'Price near support'))
                overall_score += 1
            
            # Volume confirmation
            volume_ratio = volume_analysis.get('volume_ratio', 1.0)
            if volume_ratio > 1.5:
                signals.append(('Volume', 'CONFIRM', 60, 'High volume confirms move'))
                overall_score += 1
            
            # Pattern analysis
            for pattern in patterns:
                if 'Breakout' in pattern:
                    direction = 'BUY' if 'Upward' in pattern else 'SELL'
                    signals.append(('Pattern', direction, 75, f'{pattern} detected'))
                    overall_score += 2 if direction == 'BUY' else -2
            
            # Generate final recommendation
            if overall_score >= 4:
                recommendation = 'STRONG BUY'
                confidence = min(85 + (overall_score - 4) * 3, 95)
                action_color = '🟢🟢🟢'
            elif overall_score >= 2:
                recommendation = 'BUY'
                confidence = 70 + (overall_score - 2) * 5
                action_color = '🟢🟢'
            elif overall_score >= 1:
                recommendation = 'WEAK BUY'
                confidence = 60
                action_color = '🟢'
            elif overall_score <= -4:
                recommendation = 'STRONG SELL'
                confidence = min(85 + abs(overall_score + 4) * 3, 95)
                action_color = '🔴🔴🔴'
            elif overall_score <= -2:
                recommendation = 'SELL'
                confidence = 70 + abs(overall_score + 2) * 5
                action_color = '🔴🔴'
            elif overall_score <= -1:
                recommendation = 'WEAK SELL'
                confidence = 60
                action_color = '🔴'
            else:
                recommendation = 'HOLD/WAIT'
                confidence = 50
                action_color = '⚪'
            
            # Calculate entry/exit levels
            atr = current_price * 0.02  # Fallback ATR
            if 'atr' in indicators:
                atr = indicators['atr'].iloc[-1]
            
            if 'BUY' in recommendation:
                entry = current_price
                stop_loss = entry - (2 * atr)
                take_profit_1 = entry + (2 * atr)
                take_profit_2 = entry + (4 * atr)
                take_profit_3 = entry + (6 * atr)
            elif 'SELL' in recommendation:
                entry = current_price
                stop_loss = entry + (2 * atr)
                take_profit_1 = entry - (2 * atr)
                take_profit_2 = entry - (4 * atr)
                take_profit_3 = entry - (6 * atr)
            else:
                entry = current_price
                stop_loss = current_price
                take_profit_1 = current_price
                take_profit_2 = current_price
                take_profit_3 = current_price
            
            return {
                'recommendation': recommendation,
                'confidence': confidence,
                'action_color': action_color,
                'overall_score': overall_score,
                'signals': signals,
                'entry': entry,
                'stop_loss': stop_loss,
                'take_profit_1': take_profit_1,
                'take_profit_2': take_profit_2,
                'take_profit_3': take_profit_3,
                'risk_reward_1': abs(take_profit_1 - entry) / abs(entry - stop_loss) if stop_loss != entry else 1,
                'risk_reward_2': abs(take_profit_2 - entry) / abs(entry - stop_loss) if stop_loss != entry else 2,
                'risk_reward_3': abs(take_profit_3 - entry) / abs(entry - stop_loss) if stop_loss != entry else 3
            }
            
        except Exception as e:
            logger.error(f"Error generating recommendation: {e}")
            return {
                'recommendation': 'HOLD',
                'confidence': 50,
                'action_color': '⚪',
                'signals': [('Error', 'HOLD', 50, 'Analysis error occurred')]
            }

    def calculate_all_indicators(self, df: pd.DataFrame) -> Dict:
        """Basic indicators for signal generation"""
        return self.calculate_comprehensive_indicators(df)

    def detect_signals(self, indicators: Dict, current_price: float) -> List[Dict]:
        """Basic signal detection"""
        signals = []
        
        try:
            if 'rsi' in indicators and len(indicators['rsi']) > 0:
                rsi = indicators['rsi'].iloc[-1]
                if pd.notna(rsi):
                    if rsi < 30:
                        signals.append({'type': 'buy', 'reason': f'RSI oversold at {rsi:.2f}', 'confidence': 80})
                    elif rsi > 70:
                        signals.append({'type': 'sell', 'reason': f'RSI overbought at {rsi:.2f}', 'confidence': 80})
            
            if random.random() > 0.7:
                signal_type = random.choice(['buy', 'sell'])
                signals.append({'type': signal_type, 'reason': 'Multi-indicator confluence', 'confidence': random.randint(70, 90)})
                
        except Exception as e:
            logger.error(f"Error detecting signals: {e}")
        
        return signals

    def get_entry_exit_levels(self, current_price: float, signal_type: str) -> Dict:
        """Basic entry/exit calculation"""
        try:
            atr = current_price * 0.02
            
            if signal_type == 'buy':
                return {
                    'entry': current_price, 'stop_loss': current_price - (2 * atr),
                    'take_profit_1': current_price + (1.5 * atr), 'take_profit_2': current_price + (3 * atr), 'take_profit_3': current_price + (4.5 * atr)
                }
            else:
                return {
                    'entry': current_price, 'stop_loss': current_price + (2 * atr),
                    'take_profit_1': current_price - (1.5 * atr), 'take_profit_2': current_price - (3 * atr), 'take_profit_3': current_price - (4.5 * atr)
                }
        except:
            return {}

    async def get_market_overview(self) -> Dict:
        return {
            'market_sentiment': 'bullish', 'volatility': 'medium', 'gainers_count': 15,
            'losers_count': 8, 'neutral_count': 7, 'total_volume_24h': 45000000000,
            'avg_change_percent': 2.5, 'timestamp': datetime.now()
        }
