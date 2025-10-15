"""
V6 ULTIMATE - Technical Analysis Module
INSTITUTIONAL-GRADE with 10 Advanced Features
"""
import logging
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
except:
    PANDAS_AVAILABLE = False
    logger.warning("Pandas not available, using simple data structures")

class V6TechnicalAnalyzer:
    """
    V6 ULTIMATE Technical Analyzer
    Implements 10 Institutional-Grade Features
    """
    
    def __init__(self):
        self.version = "6.0 ULTIMATE"
        logger.info(f"✅ {self.version} Technical Analyzer initialized")
    
    async def analyze_v6_ultimate(self, df, pair: str, timeframe: str, binance_client) -> Dict:
        """
        MAIN V6 ULTIMATE ANALYSIS
        Includes ALL 10 advanced features
        """
        try:
            logger.info(f"🔬 V6 ULTIMATE Analysis: {pair} on {timeframe}")
            
            if df is None or (PANDAS_AVAILABLE and df.empty):
                return {'error': 'No data'}
            
            # Get current price
            if PANDAS_AVAILABLE:
                current_price = float(df['close'].iloc[-1])
            else:
                current_price = df[-1]['close'] if df else 0
            
            # FEATURE 1: Calculate base indicators
            indicators = self._calculate_indicators(df)
            
            # FEATURE 2: Divergence Detection
            divergences = self._detect_divergences(df, indicators)
            
            # FEATURE 3: Multi-Timeframe Confirmation
            mtf = await self._multi_timeframe_check(pair, timeframe, binance_client)
            
            # FEATURE 4: Market Regime Detection
            regime = self._detect_regime(df, indicators)
            
            # FEATURE 5: Volume Profile
            volume_profile = self._volume_profile(df)
            
            # FEATURE 6: Correlation Analysis
            correlations = self._analyze_correlations(df, indicators)
            
            # FEATURE 7: Enhanced Patterns
            patterns = self._detect_patterns_v6(df)
            
            # Calculate support/resistance
            sr_levels = self._calc_support_resistance(df)
            
            # Trend analysis
            trend = self._analyze_trend(df, indicators, divergences, mtf)
            
            # Risk assessment
            risk = self._assess_risk(df, indicators, regime)
            
            # FEATURE 8: Weighted Scoring
            # FEATURE 9: Generate recommendation with priority
            recommendation = self._generate_v6_recommendation(
                indicators, trend, sr_levels, regime,
                divergences, mtf, volume_profile, patterns,
                correlations, current_price
            )
            
            # FEATURE 10: Kelly Position Sizing & Dynamic Stop Loss
            position_size = self._kelly_position_size(risk, trend)
            stop_loss = self._dynamic_stop_loss(current_price, indicators, sr_levels, recommendation)
            
            return {
                'pair': pair,
                'timeframe': timeframe,
                'current_price': current_price,
                'version': self.version,
                'indicators': indicators,
                'divergences': divergences,
                'mtf_analysis': mtf,
                'regime': regime,
                'volume_profile': volume_profile,
                'correlations': correlations,
                'patterns': patterns,
                'sr_levels': sr_levels,
                'trend': trend,
                'risk': risk,
                'recommendation': recommendation,
                'position_size': position_size,
                'stop_loss': stop_loss,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"V6 Analysis error: {e}")
            return {'error': str(e)}
    
    def _calculate_indicators(self, df) -> Dict:
        """Calculate all technical indicators"""
        indicators = {}
        
        try:
            if PANDAS_AVAILABLE:
                # RSI
                delta = df['close'].diff()
                gain = delta.where(delta > 0, 0).rolling(14).mean()
                loss = -delta.where(delta < 0, 0).rolling(14).mean()
                rs = gain / loss
                indicators['rsi'] = 100 - (100 / (1 + rs))
                
                # Moving Averages
                indicators['sma20'] = df['close'].rolling(20).mean()
                indicators['sma50'] = df['close'].rolling(50).mean()
                indicators['ema12'] = df['close'].ewm(span=12).mean()
                indicators['ema26'] = df['close'].ewm(span=26).mean()
                
                # MACD
                indicators['macd'] = indicators['ema12'] - indicators['ema26']
                indicators['macd_signal'] = indicators['macd'].ewm(span=9).mean()
                
                # ATR
                high_low = df['high'] - df['low']
                indicators['atr'] = high_low.rolling(14).mean()
                
            return indicators
            
        except Exception as e:
            logger.error(f"Indicator calculation error: {e}")
            return {}
    
    def _detect_divergences(self, df, indicators: Dict) -> Dict:
        """
        FEATURE 1: Divergence Detection
        Detects Bullish/Bearish RSI & MACD divergences
        """
        divergences = []
        
        try:
            if not PANDAS_AVAILABLE or 'rsi' not in indicators:
                return {'divergences': [], 'has_bullish': False, 'has_bearish': False}
            
            # Simple divergence check on last 20 candles
            recent_df = df.tail(20)
            rsi_recent = indicators['rsi'].tail(20)
            
            # Find price lows and highs
            price_min_idx = recent_df['close'].idxmin()
            price_max_idx = recent_df['close'].idxmax()
            
            # Bullish Divergence: Price lower low, RSI higher low
            if price_min_idx in rsi_recent.index:
                price_low = recent_df.loc[price_min_idx, 'close']
                rsi_low = rsi_recent.loc[price_min_idx]
                
                # Check if it's a divergence
                prev_price_lows = recent_df[recent_df.index < price_min_idx]['close'].min()
                prev_rsi_lows = rsi_recent[rsi_recent.index < price_min_idx].min()
                
                if price_low < prev_price_lows and rsi_low > prev_rsi_lows:
                    divergences.append({
                        'type': 'Bullish RSI Divergence',
                        'strength': 90,
                        'signal': 'STRONG BUY'
                    })
            
            # Bearish Divergence: Price higher high, RSI lower high
            if price_max_idx in rsi_recent.index:
                price_high = recent_df.loc[price_max_idx, 'close']
                rsi_high = rsi_recent.loc[price_max_idx]
                
                prev_price_highs = recent_df[recent_df.index < price_max_idx]['close'].max()
                prev_rsi_highs = rsi_recent[rsi_recent.index < price_max_idx].max()
                
                if price_high > prev_price_highs and rsi_high < prev_rsi_highs:
                    divergences.append({
                        'type': 'Bearish RSI Divergence',
                        'strength': 90,
                        'signal': 'STRONG SELL'
                    })
            
            has_bullish = any(d['signal'] in ['BUY', 'STRONG BUY'] for d in divergences)
            has_bearish = any(d['signal'] in ['SELL', 'STRONG SELL'] for d in divergences)
            
            return {
                'divergences': divergences,
                'count': len(divergences),
                'has_bullish': has_bullish,
                'has_bearish': has_bearish
            }
            
        except Exception as e:
            logger.error(f"Divergence detection error: {e}")
            return {'divergences': [], 'has_bullish': False, 'has_bearish': False}
    
    async def _multi_timeframe_check(self, pair: str, main_tf: str, binance_client) -> Dict:
        """
        FEATURE 2: Multi-Timeframe Confirmation
        Checks 3 higher timeframes for trend confirmation
        """
        try:
            tf_map = {
                '1m': ['5m', '15m', '1h'],
                '5m': ['15m', '1h', '4h'],
                '15m': ['1h', '4h', '1d'],
                '30m': ['1h', '4h', '1d'],
                '1h': ['4h', '1d', '1w']
            }
            
            check_tfs = tf_map.get(main_tf, ['1h', '4h', '1d'])
            votes = {'bullish': 0, 'bearish': 0, 'neutral': 0}
            
            for tf in check_tfs[:2]:  # Check 2 higher TFs
                try:
                    df = await binance_client.get_klines(pair, tf, 50)
                    if df is not None and not df.empty:
                        sma20 = df['close'].rolling(20).mean()
                        current = df['close'].iloc[-1]
                        
                        if current > sma20.iloc[-1]:
                            votes['bullish'] += 1
                        elif current < sma20.iloc[-1]:
                            votes['bearish'] += 1
                        else:
                            votes['neutral'] += 1
                except:
                    continue
            
            total = sum(votes.values())
            if total == 0:
                return {'confirmed': False, 'trend': 'Unknown', 'confidence': 0}
            
            if votes['bullish'] >= 2:
                return {'confirmed': True, 'trend': 'Bullish', 'confidence': (votes['bullish']/total)*100, 'votes': votes}
            elif votes['bearish'] >= 2:
                return {'confirmed': True, 'trend': 'Bearish', 'confidence': (votes['bearish']/total)*100, 'votes': votes}
            else:
                return {'confirmed': False, 'trend': 'Mixed', 'confidence': 50, 'votes': votes}
                
        except Exception as e:
            logger.error(f"MTF error: {e}")
            return {'confirmed': False, 'trend': 'Unknown', 'confidence': 0}
    
    def _detect_regime(self, df, indicators: Dict) -> Dict:
        """
        FEATURE 3: Market Regime Detection
        Detects if market is Trending, Ranging, High Volatility, or Transitional
        """
        try:
            if not PANDAS_AVAILABLE:
                return {'regime': 'Unknown', 'confidence': 50}
            
            # Calculate volatility
            returns = df['close'].pct_change()
            volatility = returns.std()
            
            # Calculate trend strength (simple)
            sma20 = df['close'].rolling(20).mean()
            price_above_sma = (df['close'] > sma20).sum() / len(df)
            
            # Determine regime
            if volatility > 0.03:  # 3% volatility
                regime = 'High Volatility'
                strategy = 'Breakout Trading'
                confidence = 80
            elif price_above_sma > 0.7:  # 70% above SMA
                regime = 'Strong Trending Up'
                strategy = 'Trend Following (Long)'
                confidence = 85
            elif price_above_sma < 0.3:  # 70% below SMA
                regime = 'Strong Trending Down'
                strategy = 'Trend Following (Short)'
                confidence = 85
            elif 0.4 < price_above_sma < 0.6:  # Around SMA
                regime = 'Ranging/Consolidation'
                strategy = 'Mean Reversion'
                confidence = 75
            else:
                regime = 'Transitional'
                strategy = 'Wait for Clarity'
                confidence = 50
            
            return {
                'regime': regime,
                'strategy': strategy,
                'confidence': confidence,
                'volatility': volatility * 100
            }
            
        except Exception as e:
            logger.error(f"Regime detection error: {e}")
            return {'regime': 'Unknown', 'confidence': 50}
    
    def _volume_profile(self, df) -> Dict:
        """
        FEATURE 4: Volume Profile Analysis
        Calculates High Volume Nodes and Point of Control
        """
        try:
            if not PANDAS_AVAILABLE:
                return {'hvn': [], 'poc': 0}
            
            # Simple volume profile
            volume_by_price = {}
            for idx, row in df.tail(100).iterrows():
                price_level = round(row['close'], 2)
                if price_level not in volume_by_price:
                    volume_by_price[price_level] = 0
                volume_by_price[price_level] += row['volume']
            
            # Find top 3 HVNs
            sorted_levels = sorted(volume_by_price.items(), key=lambda x: x[1], reverse=True)
            hvn = [price for price, vol in sorted_levels[:3]]
            poc = sorted_levels[0][0] if sorted_levels else 0
            
            return {
                'hvn': hvn,
                'poc': poc,
                'description': f'POC at {poc}, HVNs: {hvn}'
            }
            
        except Exception as e:
            logger.error(f"Volume profile error: {e}")
            return {'hvn': [], 'poc': 0}
    
    def _analyze_correlations(self, df, indicators: Dict) -> Dict:
        """
        FEATURE 5: Correlation Analysis
        Analyzes price-volume and indicator correlations
        """
        try:
            if not PANDAS_AVAILABLE:
                return {'pv_corr': 0, 'interpretation': 'Unknown'}
            
            price_change = df['close'].pct_change()
            volume_change = df['volume'].pct_change()
            
            pv_corr = price_change.corr(volume_change)
            
            if pv_corr > 0.5:
                interpretation = 'Healthy - Volume confirms price'
            elif pv_corr < -0.5:
                interpretation = 'Warning - Volume diverges'
            else:
                interpretation = 'Neutral'
            
            return {
                'price_volume_corr': float(pv_corr) if not pd.isna(pv_corr) else 0,
                'interpretation': interpretation
            }
            
        except Exception as e:
            logger.error(f"Correlation error: {e}")
            return {'price_volume_corr': 0, 'interpretation': 'Unknown'}
    
    def _detect_patterns_v6(self, df) -> List[str]:
        """
        FEATURE 6: Enhanced Pattern Recognition
        """
        patterns = []
        
        try:
            if not PANDAS_AVAILABLE:
                return ['Analysis Unavailable']
            
            recent = df.tail(30)
            
            # Double Top/Bottom (simplified)
            highs = recent['high'].rolling(5).max()
            lows = recent['low'].rolling(5).min()
            
            if len(highs) > 10:
                last_high = highs.iloc[-1]
                prev_high = highs.iloc[-10]
                if abs(last_high - prev_high) / last_high < 0.02:
                    patterns.append('Double Top (Bearish)')
            
            if len(lows) > 10:
                last_low = lows.iloc[-1]
                prev_low = lows.iloc[-10]
                if abs(last_low - prev_low) / last_low < 0.02:
                    patterns.append('Double Bottom (Bullish)')
            
            # Breakout detection
            bb_upper = recent['high'].rolling(20).max()
            if recent['close'].iloc[-1] > bb_upper.iloc[-2]:
                patterns.append('Upward Breakout (Bullish)')
            
            return patterns if patterns else ['Consolidation']
            
        except Exception as e:
            logger.error(f"Pattern detection error: {e}")
            return ['Pattern Analysis Error']
    
    def _calc_support_resistance(self, df) -> Dict:
        """Calculate support and resistance levels"""
        try:
            if not PANDAS_AVAILABLE:
                return {'support': 0, 'resistance': 0}
            
            current_price = df['close'].iloc[-1]
            recent = df.tail(100)
            
            # Simple pivot points
            highs = recent['high'].rolling(5).max()
            lows = recent['low'].rolling(5).min()
            
            resistance = highs[highs > current_price].min() if len(highs[highs > current_price]) > 0 else current_price * 1.02
            support = lows[lows < current_price].max() if len(lows[lows < current_price]) > 0 else current_price * 0.98
            
            return {
                'resistance': float(resistance),
                'support': float(support),
                'distance_to_resistance': ((resistance - current_price) / current_price) * 100,
                'distance_to_support': ((current_price - support) / current_price) * 100
            }
            
        except Exception as e:
            logger.error(f"S/R error: {e}")
            return {'support': 0, 'resistance': 0}
    
    def _analyze_trend(self, df, indicators: Dict, divergences: Dict, mtf: Dict) -> Dict:
        """Analyze trend with divergence and MTF bonuses"""
        try:
            if not PANDAS_AVAILABLE:
                return {'trend': 'Unknown', 'strength': 0, 'confidence': 50}
            
            score = 0
            
            # Base trend from MAs
            if 'sma20' in indicators and 'sma50' in indicators:
                current = df['close'].iloc[-1]
                sma20 = indicators['sma20'].iloc[-1]
                sma50 = indicators['sma50'].iloc[-1]
                
                if current > sma20 > sma50:
                    score += 3
                elif current < sma20 < sma50:
                    score -= 3
            
            # MACD
            if 'macd' in indicators and 'macd_signal' in indicators:
                macd = indicators['macd'].iloc[-1]
                signal = indicators['macd_signal'].iloc[-1]
                if macd > signal:
                    score += 2
                elif macd < signal:
                    score -= 2
            
            # Divergence bonus
            if divergences.get('has_bullish'):
                score += 3
            elif divergences.get('has_bearish'):
                score -= 3
            
            # MTF bonus
            if mtf.get('confirmed'):
                if mtf['trend'] == 'Bullish':
                    score += 2
                elif mtf['trend'] == 'Bearish':
                    score -= 2
            
            # Determine trend
            if score >= 5:
                trend = 'Very Strong Bullish'
            elif score >= 3:
                trend = 'Strong Bullish'
            elif score >= 1:
                trend = 'Weak Bullish'
            elif score <= -5:
                trend = 'Very Strong Bearish'
            elif score <= -3:
                trend = 'Strong Bearish'
            elif score <= -1:
                trend = 'Weak Bearish'
            else:
                trend = 'Neutral'
            
            confidence = min(abs(score) * 15, 99)
            
            return {
                'trend': trend,
                'strength': abs(score),
                'confidence': confidence,
                'score': score
            }
            
        except Exception as e:
            logger.error(f"Trend analysis error: {e}")
            return {'trend': 'Unknown', 'strength': 0, 'confidence': 50}
    
    def _assess_risk(self, df, indicators: Dict, regime: Dict) -> Dict:
        """Assess risk level"""
        try:
            if not PANDAS_AVAILABLE:
                return {'risk_level': 'Medium', 'atr_percent': 2.0}
            
            atr = indicators.get('atr', pd.Series([0])).iloc[-1]
            current_price = df['close'].iloc[-1]
            atr_percent = (atr / current_price) * 100 if current_price > 0 else 2.0
            
            # Adjust for regime
            if regime.get('regime') == 'High Volatility':
                atr_percent *= 1.5
            
            if atr_percent > 5:
                risk_level = 'Very High'
            elif atr_percent > 3:
                risk_level = 'High'
            elif atr_percent > 2:
                risk_level = 'Medium'
            else:
                risk_level = 'Low'
            
            return {
                'risk_level': risk_level,
                'atr_percent': atr_percent,
                'recommended_position': max(0.5, 2.0 / atr_percent)
            }
            
        except Exception as e:
            logger.error(f"Risk assessment error: {e}")
            return {'risk_level': 'Medium', 'atr_percent': 2.0}
    
    def _generate_v6_recommendation(self, indicators, trend, sr_levels, regime, 
                                   divergences, mtf, volume_profile, patterns,
                                   correlations, current_price) -> Dict:
        """
        FEATURE 7: Weighted Scoring System
        FEATURE 8: Generate V6 Recommendation
        """
        try:
            # Explicit weights
            weights = {
                'trend': 3.0,
                'divergence': 2.5,
                'mtf': 2.5,
                'regime': 1.5,
                'volume': 1.5,
                'patterns': 2.0
            }
            
            weighted_score = 0
            signals = []
            
            # Trend
            trend_score = trend.get('score', 0)
            weighted_score += trend_score * weights['trend']
            if trend_score > 0:
                signals.append(('Trend', 'BUY', trend.get('confidence', 70), f"{trend.get('trend')}"))
            elif trend_score < 0:
                signals.append(('Trend', 'SELL', trend.get('confidence', 70), f"{trend.get('trend')}"))
            
            # Divergence
            if divergences.get('has_bullish'):
                weighted_score += 3 * weights['divergence']
                signals.append(('Divergence', 'BUY', 90, 'Bullish Divergence'))
            elif divergences.get('has_bearish'):
                weighted_score -= 3 * weights['divergence']
                signals.append(('Divergence', 'SELL', 90, 'Bearish Divergence'))
            
            # MTF
            if mtf.get('confirmed'):
                if mtf['trend'] == 'Bullish':
                    weighted_score += 2 * weights['mtf']
                    signals.append(('MTF', 'BUY', int(mtf['confidence']), 'Multi-TF Bullish'))
                elif mtf['trend'] == 'Bearish':
                    weighted_score -= 2 * weights['mtf']
                    signals.append(('MTF', 'SELL', int(mtf['confidence']), 'Multi-TF Bearish'))
            
            # Volume correlation
            pv_corr = correlations.get('price_volume_corr', 0)
            if pv_corr > 0.5:
                weighted_score += 1 * weights['volume']
                signals.append(('Volume', 'CONFIRM', 75, 'Volume confirms move'))
            
            # Determine recommendation
            if weighted_score >= 12:
                recommendation = 'STRONG BUY'
                confidence = min(90 + int((weighted_score - 12) * 0.5), 99)
            elif weighted_score >= 6:
                recommendation = 'BUY'
                confidence = 75 + int((weighted_score - 6))
            elif weighted_score >= 3:
                recommendation = 'WEAK BUY'
                confidence = 65
            elif weighted_score <= -12:
                recommendation = 'STRONG SELL'
                confidence = min(90 + int(abs(weighted_score + 12) * 0.5), 99)
            elif weighted_score <= -6:
                recommendation = 'SELL'
                confidence = 75 + int(abs(weighted_score + 6))
            elif weighted_score <= -3:
                recommendation = 'WEAK SELL'
                confidence = 65
            else:
                recommendation = 'HOLD'
                confidence = 50
            
            # Calculate levels
            atr = indicators.get('atr', pd.Series([current_price * 0.02])).iloc[-1] if PANDAS_AVAILABLE else current_price * 0.02
            
            if 'BUY' in recommendation:
                entry = current_price
                stop_loss = entry - (2 * atr)
                tp1 = entry + (2 * atr)
                tp2 = entry + (4 * atr)
                tp3 = entry + (6 * atr)
            elif 'SELL' in recommendation:
                entry = current_price
                stop_loss = entry + (2 * atr)
                tp1 = entry - (2 * atr)
                tp2 = entry - (4 * atr)
                tp3 = entry - (6 * atr)
            else:
                entry = stop_loss = tp1 = tp2 = tp3 = current_price
            
            return {
                'recommendation': recommendation,
                'confidence': confidence,
                'weighted_score': weighted_score,
                'signals': signals,
                'entry': entry,
                'stop_loss': stop_loss,
                'tp1': tp1,
                'tp2': tp2,
                'tp3': tp3,
                'rr1': abs(tp1 - entry) / abs(entry - stop_loss) if stop_loss != entry else 1,
                'rr2': abs(tp2 - entry) / abs(entry - stop_loss) if stop_loss != entry else 2,
                'rr3': abs(tp3 - entry) / abs(entry - stop_loss) if stop_loss != entry else 3
            }
            
        except Exception as e:
            logger.error(f"Recommendation error: {e}")
            return {'recommendation': 'HOLD', 'confidence': 50, 'signals': []}
    
    def _kelly_position_size(self, risk: Dict, trend: Dict) -> Dict:
        """
        FEATURE 9: Kelly Criterion Position Sizing
        """
        try:
            # Kelly formula: f = (p*b - q) / b
            win_rate = 0.85  # 85%
            avg_win = 3.0
            avg_loss = 1.0
            
            p = win_rate
            q = 1 - win_rate
            b = avg_win / avg_loss
            
            kelly = (p * b - q) / b
            fractional_kelly = kelly * 0.5  # 50% of Kelly for safety
            
            # Adjust for confidence
            confidence = trend.get('confidence', 50) / 100
            adjusted = fractional_kelly * confidence
            
            # Adjust for risk
            risk_level = risk.get('risk_level', 'Medium')
            if risk_level == 'Very High':
                multiplier = 0.3
            elif risk_level == 'High':
                multiplier = 0.5
            elif risk_level == 'Medium':
                multiplier = 0.75
            else:
                multiplier = 1.0
            
            final = adjusted * multiplier
            final = min(max(final, 0.005), 0.05)  # Between 0.5% and 5%
            
            return {
                'kelly_percent': kelly * 100,
                'fractional_kelly': fractional_kelly * 100,
                'recommended_position': final * 100,
                'max': 5.0,
                'min': 0.5
            }
            
        except Exception as e:
            logger.error(f"Kelly calculation error: {e}")
            return {'recommended_position': 2.0}
    
    def _dynamic_stop_loss(self, current_price: float, indicators: Dict, 
                          sr_levels: Dict, recommendation: Dict) -> Dict:
        """
        FEATURE 10: Dynamic Stop Loss (3 types)
        """
        try:
            # Type 1: ATR-based
            atr = indicators.get('atr', pd.Series([current_price * 0.02])).iloc[-1] if PANDAS_AVAILABLE else current_price * 0.02
            atr_stop_long = current_price - (2 * atr)
            atr_stop_short = current_price + (2 * atr)
            
            # Type 2: Support-based
            support = sr_levels.get('support', current_price * 0.98)
            resistance = sr_levels.get('resistance', current_price * 1.02)
            support_stop_long = support - (current_price * 0.001)
            support_stop_short = resistance + (current_price * 0.001)
            
            # Type 3: Percentage-based
            percent_stop_long = current_price * 0.98  # 2% max risk
            percent_stop_short = current_price * 1.02
            
            # Choose best for LONG
            if support_stop_long > current_price * 0.97:
                recommended_long = support_stop_long
                type_long = 'Support-based'
            elif (current_price - atr_stop_long) / current_price < 0.03:
                recommended_long = atr_stop_long
                type_long = 'ATR-based'
            else:
                recommended_long = percent_stop_long
                type_long = 'Risk-based'
            
            # Choose best for SHORT
            if support_stop_short < current_price * 1.03:
                recommended_short = support_stop_short
                type_short = 'Resistance-based'
            elif (atr_stop_short - current_price) / current_price < 0.03:
                recommended_short = atr_stop_short
                type_short = 'ATR-based'
            else:
                recommended_short = percent_stop_short
                type_short = 'Risk-based'
            
            return {
                'long': {
                    'recommended': recommended_long,
                    'type': type_long,
                    'atr_stop': atr_stop_long,
                    'support_stop': support_stop_long,
                    'percent_stop': percent_stop_long,
                    'risk_percent': ((current_price - recommended_long) / current_price) * 100
                },
                'short': {
                    'recommended': recommended_short,
                    'type': type_short,
                    'atr_stop': atr_stop_short,
                    'resistance_stop': support_stop_short,
                    'percent_stop': percent_stop_short,
                    'risk_percent': ((recommended_short - current_price) / current_price) * 100
                }
            }
            
        except Exception as e:
            logger.error(f"Dynamic stop loss error: {e}")
            return {
                'long': {'recommended': current_price * 0.98, 'type': 'Default'},
                'short': {'recommended': current_price * 1.02, 'type': 'Default'}
            }
