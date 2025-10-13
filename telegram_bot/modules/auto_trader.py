"""
Automated Trading System
Executes trades automatically based on generated signals
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd

from .binance_client import BinanceClient

logger = logging.getLogger(__name__)

class AutoTrader:
    def __init__(self, binance_client: BinanceClient):
        self.binance_client = binance_client
        self.active_trades = {}
        self.trade_history = []
        self.user_settings = {}
        
        # Default trading parameters
        self.default_settings = {
            'risk_percentage': 2.0,  # Risk per trade as % of balance
            'max_leverage': 125,
            'max_daily_trades': 10,
            'stop_loss_percentage': 2.0,
            'take_profit_levels': [1.5, 3.0, 4.5],  # Risk:Reward ratios
            'partial_close_percentages': [50, 30, 20],  # % to close at each TP
            'trailing_stop': True,
            'min_signal_strength': 75
        }
    
    async def execute_signal(self, signal: Dict, user_id: int) -> Dict:
        """Execute a trading signal for a user"""
        try:
            # Check if user has auto trading enabled
            if not self._is_auto_trading_enabled(user_id):
                return {'success': False, 'error': 'Auto trading not enabled'}
            
            # Validate signal
            if not self._validate_signal(signal):
                return {'success': False, 'error': 'Invalid signal'}
            
            # Check daily trade limit
            if self._exceeded_daily_limit(user_id):
                return {'success': False, 'error': 'Daily trade limit exceeded'}
            
            # Get user settings
            settings = self.user_settings.get(user_id, self.default_settings)
            
            # Calculate position size
            position_size = await self._calculate_position_size(
                signal, settings, user_id
            )
            
            if position_size <= 0:
                return {'success': False, 'error': 'Insufficient balance'}
            
            # Execute the trade
            trade_result = await self._place_trade(signal, position_size, settings, user_id)
            
            if trade_result['success']:
                # Store trade information
                trade_id = trade_result['trade_id']
                self.active_trades[trade_id] = {
                    'user_id': user_id,
                    'signal': signal,
                    'position_size': position_size,
                    'settings': settings,
                    'entry_time': datetime.now(),
                    'status': 'active',
                    'orders': trade_result['orders']
                }
                
                # Add to history
                self.trade_history.append(self.active_trades[trade_id].copy())
                
                logger.info(f"Trade executed successfully for user {user_id}: {trade_id}")
                
            return trade_result
            
        except Exception as e:
            logger.error(f"Error executing signal for user {user_id}: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _calculate_position_size(self, signal: Dict, settings: Dict, user_id: int) -> float:
        """Calculate position size based on risk management"""
        try:
            # Get account balance
            account_info = await self.binance_client.get_account_info()
            if not account_info:
                return 0
            
            # Find USDT balance
            usdt_balance = 0
            for balance in account_info['balances']:
                if balance['asset'] == 'USDT':
                    usdt_balance = balance['free']
                    break
            
            if usdt_balance <= 0:
                return 0
            
            # Calculate risk amount
            risk_amount = usdt_balance * (settings['risk_percentage'] / 100)
            
            # Calculate stop loss distance
            entry_price = signal['entry']
            stop_loss = signal['stop_loss']
            stop_distance = abs(entry_price - stop_loss) / entry_price
            
            # Calculate position size
            leverage = min(settings.get('max_leverage', 125), 125)
            position_value = risk_amount / stop_distance
            position_size = position_value / entry_price
            
            # Apply leverage
            position_size *= leverage
            
            # Get symbol info for minimum quantity
            symbol_info = await self.binance_client.get_symbol_info(signal['symbol'])
            if symbol_info:
                position_size = self.binance_client.format_quantity(symbol_info, position_size)
            
            return position_size
            
        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return 0
    
    async def _place_trade(self, signal: Dict, position_size: float, settings: Dict, user_id: int) -> Dict:
        """Place the actual trade orders"""
        try:
            symbol = signal['symbol']
            signal_type = signal['type']
            entry_price = signal['entry']
            
            # Determine order side
            side = 'BUY' if signal_type == 'LONG' else 'SELL'
            
            # Place market order for entry
            entry_order = await self.binance_client.place_order(
                symbol=symbol,
                side=side,
                order_type='MARKET',
                quantity=position_size
            )
            
            if not entry_order:
                return {'success': False, 'error': 'Failed to place entry order'}
            
            trade_id = f"{user_id}_{symbol}_{int(datetime.now().timestamp())}"
            orders = {'entry': entry_order}
            
            # Place stop loss order
            sl_side = 'SELL' if signal_type == 'LONG' else 'BUY'
            sl_order = await self.binance_client.place_order(
                symbol=symbol,
                side=sl_side,
                order_type='STOP_MARKET',
                quantity=position_size,
                stop_price=signal['stop_loss']
            )
            
            if sl_order:
                orders['stop_loss'] = sl_order
            
            # Place take profit orders
            tp_orders = []
            remaining_quantity = position_size
            
            for i, (tp_price, close_percentage) in enumerate(zip(
                [signal['take_profit_1'], signal['take_profit_2'], signal['take_profit_3']],
                settings['partial_close_percentages']
            )):
                tp_quantity = position_size * (close_percentage / 100)
                remaining_quantity -= tp_quantity
                
                tp_order = await self.binance_client.place_order(
                    symbol=symbol,
                    side=sl_side,  # Same side as stop loss
                    order_type='LIMIT',
                    quantity=tp_quantity,
                    price=tp_price
                )
                
                if tp_order:
                    tp_orders.append(tp_order)
            
            orders['take_profits'] = tp_orders
            
            return {
                'success': True,
                'trade_id': trade_id,
                'orders': orders,
                'entry_price': float(entry_order.get('fills', [{}])[0].get('price', entry_price)),
                'position_size': position_size
            }
            
        except Exception as e:
            logger.error(f"Error placing trade: {e}")
            return {'success': False, 'error': str(e)}
    
    async def monitor_trades(self):
        """Monitor active trades and update their status"""
        while True:
            try:
                for trade_id, trade_info in list(self.active_trades.items()):
                    await self._check_trade_status(trade_id, trade_info)
                
                # Wait before next check
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Error monitoring trades: {e}")
                await asyncio.sleep(60)
    
    async def _check_trade_status(self, trade_id: str, trade_info: Dict):
        """Check the status of a specific trade"""
        try:
            symbol = trade_info['signal']['symbol']
            
            # Get current price
            ticker = await self.binance_client.get_symbol_ticker(symbol)
            if not ticker:
                return
            
            current_price = ticker['price']
            
            # Check if any orders have been filled
            orders_to_check = []
            
            # Add stop loss order
            if 'stop_loss' in trade_info['orders']:
                orders_to_check.append(('stop_loss', trade_info['orders']['stop_loss']))
            
            # Add take profit orders
            for i, tp_order in enumerate(trade_info['orders'].get('take_profits', [])):
                orders_to_check.append((f'take_profit_{i+1}', tp_order))
            
            # Check order statuses
            for order_type, order in orders_to_check:
                if order and 'orderId' in order:
                    # In a real implementation, you would check the order status
                    # For now, we'll simulate based on price levels
                    await self._simulate_order_check(trade_id, trade_info, order_type, current_price)
            
        except Exception as e:
            logger.error(f"Error checking trade status for {trade_id}: {e}")
    
    async def _simulate_order_check(self, trade_id: str, trade_info: Dict, order_type: str, current_price: float):
        """Simulate order status checking (replace with real implementation)"""
        try:
            signal = trade_info['signal']
            signal_type = signal['type']
            
            # Check stop loss
            if order_type == 'stop_loss':
                if signal_type == 'LONG' and current_price <= signal['stop_loss']:
                    await self._close_trade(trade_id, 'stop_loss_hit', current_price)
                elif signal_type == 'SHORT' and current_price >= signal['stop_loss']:
                    await self._close_trade(trade_id, 'stop_loss_hit', current_price)
            
            # Check take profits
            elif order_type.startswith('take_profit'):
                tp_level = int(order_type.split('_')[-1])
                tp_price = signal[f'take_profit_{tp_level}']
                
                if signal_type == 'LONG' and current_price >= tp_price:
                    await self._partial_close(trade_id, order_type, current_price)
                elif signal_type == 'SHORT' and current_price <= tp_price:
                    await self._partial_close(trade_id, order_type, current_price)
            
        except Exception as e:
            logger.error(f"Error simulating order check: {e}")
    
    async def _close_trade(self, trade_id: str, reason: str, close_price: float):
        """Close a trade completely"""
        try:
            if trade_id not in self.active_trades:
                return
            
            trade_info = self.active_trades[trade_id]
            trade_info['status'] = 'closed'
            trade_info['close_reason'] = reason
            trade_info['close_price'] = close_price
            trade_info['close_time'] = datetime.now()
            
            # Calculate P&L
            entry_price = trade_info['signal']['entry']
            position_size = trade_info['position_size']
            signal_type = trade_info['signal']['type']
            
            if signal_type == 'LONG':
                pnl = (close_price - entry_price) * position_size
            else:
                pnl = (entry_price - close_price) * position_size
            
            trade_info['pnl'] = pnl
            trade_info['pnl_percentage'] = (pnl / (entry_price * position_size)) * 100
            
            # Remove from active trades
            del self.active_trades[trade_id]
            
            logger.info(f"Trade {trade_id} closed: {reason}, P&L: {pnl:.2f}")
            
        except Exception as e:
            logger.error(f"Error closing trade {trade_id}: {e}")
    
    async def _partial_close(self, trade_id: str, tp_level: str, close_price: float):
        """Handle partial close at take profit levels"""
        try:
            if trade_id not in self.active_trades:
                return
            
            trade_info = self.active_trades[trade_id]
            
            # Mark this TP level as hit
            if 'hit_levels' not in trade_info:
                trade_info['hit_levels'] = []
            
            if tp_level not in trade_info['hit_levels']:
                trade_info['hit_levels'].append(tp_level)
                
                logger.info(f"Trade {trade_id} hit {tp_level} at {close_price}")
                
                # If all TP levels hit, close the trade
                if len(trade_info['hit_levels']) >= 3:
                    await self._close_trade(trade_id, 'all_tp_hit', close_price)
            
        except Exception as e:
            logger.error(f"Error handling partial close: {e}")
    
    def _is_auto_trading_enabled(self, user_id: int) -> bool:
        """Check if auto trading is enabled for user"""
        return user_id in self.user_settings and self.user_settings[user_id].get('auto_trading_enabled', False)
    
    def _validate_signal(self, signal: Dict) -> bool:
        """Validate signal data"""
        required_fields = ['symbol', 'type', 'entry', 'stop_loss', 'take_profit_1', 'take_profit_2', 'take_profit_3']
        return all(field in signal for field in required_fields)
    
    def _exceeded_daily_limit(self, user_id: int) -> bool:
        """Check if user exceeded daily trade limit"""
        today = datetime.now().date()
        today_trades = [
            trade for trade in self.trade_history
            if trade['user_id'] == user_id and trade['entry_time'].date() == today
        ]
        
        max_trades = self.user_settings.get(user_id, {}).get('max_daily_trades', 10)
        return len(today_trades) >= max_trades
    
    async def get_user_performance(self, user_id: int) -> Dict:
        """Get trading performance for a user"""
        try:
            user_trades = [trade for trade in self.trade_history if trade['user_id'] == user_id]
            
            if not user_trades:
                return {'total_trades': 0, 'win_rate': 0, 'total_pnl': 0}
            
            completed_trades = [trade for trade in user_trades if trade.get('status') == 'closed']
            
            if not completed_trades:
                return {'total_trades': len(user_trades), 'win_rate': 0, 'total_pnl': 0}
            
            winning_trades = [trade for trade in completed_trades if trade.get('pnl', 0) > 0]
            total_pnl = sum(trade.get('pnl', 0) for trade in completed_trades)
            
            return {
                'total_trades': len(user_trades),
                'completed_trades': len(completed_trades),
                'winning_trades': len(winning_trades),
                'win_rate': len(winning_trades) / len(completed_trades) * 100,
                'total_pnl': total_pnl,
                'avg_pnl': total_pnl / len(completed_trades),
                'best_trade': max(trade.get('pnl', 0) for trade in completed_trades),
                'worst_trade': min(trade.get('pnl', 0) for trade in completed_trades),
                'active_trades': len([trade for trade in user_trades if trade.get('status') == 'active'])
            }
            
        except Exception as e:
            logger.error(f"Error getting user performance: {e}")
            return {'total_trades': 0, 'win_rate': 0, 'total_pnl': 0}
    
    def enable_auto_trading(self, user_id: int, settings: Optional[Dict] = None):
        """Enable auto trading for a user"""
        if user_id not in self.user_settings:
            self.user_settings[user_id] = self.default_settings.copy()
        
        self.user_settings[user_id]['auto_trading_enabled'] = True
        
        if settings:
            self.user_settings[user_id].update(settings)
        
        logger.info(f"Auto trading enabled for user {user_id}")
    
    def disable_auto_trading(self, user_id: int):
        """Disable auto trading for a user"""
        if user_id in self.user_settings:
            self.user_settings[user_id]['auto_trading_enabled'] = False
        
        logger.info(f"Auto trading disabled for user {user_id}")
    
    async def close_all_user_trades(self, user_id: int):
        """Close all active trades for a user"""
        user_trades = [
            (trade_id, trade_info) for trade_id, trade_info in self.active_trades.items()
            if trade_info['user_id'] == user_id
        ]
        
        for trade_id, trade_info in user_trades:
            symbol = trade_info['signal']['symbol']
            ticker = await self.binance_client.get_symbol_ticker(symbol)
            
            if ticker:
                await self._close_trade(trade_id, 'manual_close', ticker['price'])
        
        logger.info(f"Closed {len(user_trades)} trades for user {user_id}")
        return len(user_trades)