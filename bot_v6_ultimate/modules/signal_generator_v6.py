"""
V6 ULTIMATE - Signal Generator Module
Implements Signal Priority System
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class V6SignalGenerator:
    """
    V6 ULTIMATE Signal Generator
    Features: Priority System, Quality Filtering
    """
    
    def __init__(self, binance_client, technical_analyzer):
        self.binance = binance_client
        self.analyzer = technical_analyzer
        self.signal_history = []
        self.monitored_pairs = [
            'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'XRPUSDT',
            'SOLUSDT', 'DOTUSDT', 'AVAXUSDT', 'MATICUSDT', 'LINKUSDT'
        ]
        logger.info("✅ V6 Signal Generator initialized")
    
    async def scan_for_signals_advanced(self) -> List[Dict]:
        """
        V6 ADVANCED SIGNAL SCAN
        Implements priority filtering
        """
        try:
            logger.info("🔍 V6 Advanced signal scan starting...")
            new_signals = []
            
            for pair in self.monitored_pairs[:3]:  # Top 3 pairs
                try:
                    signal = await self._analyze_pair_v6(pair)
                    if signal and signal.get('confidence', 0) >= 75:  # 75%+ only
                        new_signals.append(signal)
                    await asyncio.sleep(0.5)  # Rate limiting
                except Exception as e:
                    logger.error(f"Error analyzing {pair}: {e}")
                    continue
            
            # Apply V6 Priority System
            if new_signals:
                new_signals = self._prioritize_signals_v6(new_signals)
                
                # Add to history
                for signal in new_signals:
                    self.signal_history.append(signal)
                
                self._clean_old_signals()
                
                logger.info(f"✅ Generated {len(new_signals)} priority signals")
            
            return new_signals
            
        except Exception as e:
            logger.error(f"Signal scan error: {e}")
            return []
    
    async def _analyze_pair_v6(self, pair: str) -> Optional[Dict]:
        """
        Analyze single pair with V6 engine
        """
        try:
            # Get 500 candles
            df = await self.binance.get_klines(pair, '1h', 500)
            if df is None or df.empty:
                return None
            
            # Run V6 Ultimate Analysis
            analysis = await self.analyzer.analyze_v6_ultimate(df, pair, '1h', self.binance)
            
            if 'error' in analysis:
                return None
            
            # Extract key data
            recommendation = analysis.get('recommendation', {})
            rec_type = recommendation.get('recommendation', 'HOLD')
            
            if rec_type == 'HOLD':
                return None  # Skip HOLD signals
            
            # Build signal
            signal = {
                'id': f"{pair}_{rec_type}_{int(datetime.now().timestamp())}",
                'pair': pair,
                'type': 'LONG' if 'BUY' in rec_type else 'SHORT',
                'recommendation': rec_type,
                'confidence': recommendation.get('confidence', 75),
                'weighted_score': recommendation.get('weighted_score', 0),
                'entry': recommendation.get('entry', 0),
                'stop_loss': recommendation.get('stop_loss', 0),
                'tp1': recommendation.get('tp1', 0),
                'tp2': recommendation.get('tp2', 0),
                'tp3': recommendation.get('tp3', 0),
                'rr1': recommendation.get('rr1', 1.5),
                'rr2': recommendation.get('rr2', 3.0),
                'rr3': recommendation.get('rr3', 4.5),
                'signals': recommendation.get('signals', []),
                'divergences': analysis.get('divergences', {}),
                'mtf_confirmed': analysis.get('mtf_analysis', {}).get('confirmed', False),
                'regime': analysis.get('regime', {}).get('regime', 'Unknown'),
                'position_size': analysis.get('position_size', {}).get('recommended_position', 2.0),
                'stop_loss_type': analysis.get('stop_loss', {}).get('long', {}).get('type', 'ATR-based'),
                'timestamp': datetime.now(),
                'status': 'active',
                'version': 'V6 ULTIMATE'
            }
            
            return signal
            
        except Exception as e:
            logger.error(f"Pair analysis error for {pair}: {e}")
            return None
    
    def _prioritize_signals_v6(self, signals: List[Dict]) -> List[Dict]:
        """
        V6 SIGNAL PRIORITY SYSTEM
        Ranks signals by quality
        """
        try:
            for signal in signals:
                priority = 0
                
                # Factor 1: Confidence
                priority += signal.get('confidence', 0) * 1.0
                
                # Factor 2: MTF Confirmation
                if signal.get('mtf_confirmed'):
                    priority += 20
                
                # Factor 3: Divergence
                div = signal.get('divergences', {})
                if div.get('has_bullish') or div.get('has_bearish'):
                    priority += 15
                
                # Factor 4: Weighted Score
                priority += abs(signal.get('weighted_score', 0)) * 0.5
                
                # Factor 5: Risk/Reward
                if signal.get('rr1', 0) > 2.0:
                    priority += 10
                
                # Factor 6: Strong Regime
                regime = signal.get('regime', '')
                if 'Strong' in regime:
                    priority += 10
                
                signal['priority'] = priority
            
            # Sort by priority (highest first)
            signals.sort(key=lambda x: x.get('priority', 0), reverse=True)
            
            # Return top 3 only
            return signals[:3]
            
        except Exception as e:
            logger.error(f"Prioritization error: {e}")
            return signals
    
    async def get_signals(self, limit: int = 10) -> List[Dict]:
        """
        Get latest signals from history
        """
        try:
            cutoff = datetime.now() - timedelta(hours=24)
            recent = [s for s in self.signal_history if s.get('timestamp', datetime.now()) > cutoff]
            return sorted(recent, key=lambda x: x.get('timestamp', datetime.now()), reverse=True)[:limit]
        except Exception as e:
            logger.error(f"Get signals error: {e}")
            return []
    
    def _clean_old_signals(self):
        """Clean signals older than 7 days"""
        try:
            cutoff = datetime.now() - timedelta(days=7)
            self.signal_history = [s for s in self.signal_history if s.get('timestamp', datetime.now()) > cutoff]
        except Exception as e:
            logger.error(f"Clean signals error: {e}")
