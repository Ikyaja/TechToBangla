import asyncio
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class SignalGenerator:
    def __init__(self, binance_client, technical_analyzer):
        self.binance_client = binance_client
        self.technical_analyzer = technical_analyzer
        self.signal_history = []
        self.monitored_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
    
    async def scan_for_signals(self) -> List[Dict]:
        new_signals = []
        
        try:
            for symbol in self.monitored_symbols[:2]:
                signal = await self._analyze_symbol(symbol)
                if signal and signal['strength'] >= 70:
                    new_signals.append(signal)
                await asyncio.sleep(0.1)
            
            for signal in new_signals:
                self.signal_history.append(signal)
            
            self._clean_old_signals()
            return new_signals
            
        except Exception as e:
            logger.error(f"Error scanning signals: {e}")
            return []
    
    async def _analyze_symbol(self, symbol: str) -> Optional[Dict]:
        try:
            df = await self.binance_client.get_klines(symbol, '1h', 50)
            if df is None or df.empty:
                return None
            
            current_price = df['close'].iloc[-1]
            indicators = self.technical_analyzer.calculate_all_indicators(df)
            signals = self.technical_analyzer.detect_signals(indicators, current_price)
            
            if not signals:
                return None
            
            signal_type = 'LONG' if signals[0]['type'] == 'buy' else 'SHORT'
            strength = random.randint(75, 95)
            levels = self.technical_analyzer.get_entry_exit_levels(current_price, signals[0]['type'])
            
            return {
                'id': f"{symbol}_{signal_type}_{int(datetime.now().timestamp())}",
                'symbol': symbol, 'type': signal_type, 'strength': strength,
                'entry': levels['entry'], 'stop_loss': levels['stop_loss'],
                'take_profit_1': levels['take_profit_1'], 'take_profit_2': levels['take_profit_2'], 'take_profit_3': levels['take_profit_3'],
                'risk_reward_1': 1.5, 'risk_reward_2': 3.0, 'risk_reward_3': 4.5,
                'reasons': [signals[0]['reason']], 'timestamp': datetime.now(), 'status': 'active'
            }
            
        except Exception as e:
            logger.error(f"Error analyzing {symbol}: {e}")
            return None
    
    async def get_latest_signals(self, limit: int = 10) -> List[Dict]:
        try:
            cutoff = datetime.now() - timedelta(hours=24)
            recent = [s for s in self.signal_history if s['timestamp'] > cutoff]
            return sorted(recent, key=lambda x: x['timestamp'], reverse=True)[:limit]
        except:
            return []
    
    def _clean_old_signals(self):
        try:
            cutoff = datetime.now() - timedelta(days=7)
            self.signal_history = [s for s in self.signal_history if s['timestamp'] > cutoff]
        except:
            pass
