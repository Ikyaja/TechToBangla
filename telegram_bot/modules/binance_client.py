"""
Binance API Client for market data and trading operations
"""

import os
import asyncio
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
from binance.client import Client
from binance.exceptions import BinanceAPIException
from binance.enums import *

logger = logging.getLogger(__name__)

class BinanceClient:
    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_SECRET_KEY')
        
        # Initialize Binance client
        try:
            self.client = Client(self.api_key, self.api_secret, testnet=False)
            logger.info("✅ Binance client initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Binance client: {e}")
            self.client = None
    
    async def check_connection(self) -> bool:
        """Check if connection to Binance is working"""
        try:
            if not self.client:
                return False
            
            # Test connectivity
            status = self.client.get_system_status()
            return status['status'] == 0
        except Exception as e:
            logger.error(f"Connection check failed: {e}")
            return False
    
    async def get_account_info(self) -> Optional[Dict]:
        """Get account information"""
        try:
            if not self.client:
                return None
            
            account = self.client.get_account()
            return {
                'balances': [
                    {
                        'asset': balance['asset'],
                        'free': float(balance['free']),
                        'locked': float(balance['locked'])
                    }
                    for balance in account['balances']
                    if float(balance['free']) > 0 or float(balance['locked']) > 0
                ],
                'can_trade': account['canTrade'],
                'can_withdraw': account['canWithdraw'],
                'can_deposit': account['canDeposit']
            }
        except Exception as e:
            logger.error(f"Error getting account info: {e}")
            return None
    
    async def get_symbol_ticker(self, symbol: str) -> Optional[Dict]:
        """Get 24hr ticker statistics for a symbol"""
        try:
            if not self.client:
                return None
            
            ticker = self.client.get_ticker(symbol=symbol)
            return {
                'symbol': ticker['symbol'],
                'price': float(ticker['lastPrice']),
                'change': float(ticker['priceChange']),
                'change_percent': float(ticker['priceChangePercent']),
                'high': float(ticker['highPrice']),
                'low': float(ticker['lowPrice']),
                'volume': float(ticker['volume']),
                'quote_volume': float(ticker['quoteVolume']),
                'open_time': ticker['openTime'],
                'close_time': ticker['closeTime']
            }
        except Exception as e:
            logger.error(f"Error getting ticker for {symbol}: {e}")
            return None
    
    async def get_klines(self, symbol: str, interval: str = '1h', limit: int = 100) -> Optional[pd.DataFrame]:
        """Get kline/candlestick data for a symbol"""
        try:
            if not self.client:
                return None
            
            klines = self.client.get_klines(
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            
            # Convert to DataFrame
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            
            # Convert to appropriate data types
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['open'] = df['open'].astype(float)
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)
            df['close'] = df['close'].astype(float)
            df['volume'] = df['volume'].astype(float)
            
            return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
            
        except Exception as e:
            logger.error(f"Error getting klines for {symbol}: {e}")
            return None
    
    async def get_top_symbols(self, limit: int = 50) -> List[Dict]:
        """Get top trading symbols by volume"""
        try:
            if not self.client:
                return []
            
            # Get 24hr ticker statistics for all symbols
            tickers = self.client.get_ticker()
            
            # Filter USDT pairs and sort by volume
            usdt_pairs = [
                {
                    'symbol': ticker['symbol'],
                    'price': float(ticker['lastPrice']),
                    'change_percent': float(ticker['priceChangePercent']),
                    'volume': float(ticker['quoteVolume'])
                }
                for ticker in tickers
                if ticker['symbol'].endswith('USDT') and float(ticker['quoteVolume']) > 1000000
            ]
            
            # Sort by volume and return top symbols
            usdt_pairs.sort(key=lambda x: x['volume'], reverse=True)
            return usdt_pairs[:limit]
            
        except Exception as e:
            logger.error(f"Error getting top symbols: {e}")
            return []
    
    async def get_market_overview(self) -> Dict:
        """Get overall market overview"""
        try:
            if not self.client:
                return {}
            
            # Get top symbols
            top_symbols = await self.get_top_symbols(20)
            
            if not top_symbols:
                return {}
            
            # Calculate market metrics
            total_volume = sum(symbol['volume'] for symbol in top_symbols)
            gainers = [s for s in top_symbols if s['change_percent'] > 0]
            losers = [s for s in top_symbols if s['change_percent'] < 0]
            
            avg_change = np.mean([s['change_percent'] for s in top_symbols])
            
            return {
                'total_volume_24h': total_volume,
                'gainers_count': len(gainers),
                'losers_count': len(losers),
                'neutral_count': len(top_symbols) - len(gainers) - len(losers),
                'avg_change_percent': avg_change,
                'top_gainer': max(top_symbols, key=lambda x: x['change_percent']) if top_symbols else None,
                'top_loser': min(top_symbols, key=lambda x: x['change_percent']) if top_symbols else None,
                'highest_volume': max(top_symbols, key=lambda x: x['volume']) if top_symbols else None,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error getting market overview: {e}")
            return {}
    
    async def place_order(self, symbol: str, side: str, order_type: str, 
                         quantity: float, price: Optional[float] = None,
                         stop_price: Optional[float] = None,
                         time_in_force: str = TIME_IN_FORCE_GTC) -> Optional[Dict]:
        """Place a trading order"""
        try:
            if not self.client:
                return None
            
            order_params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity,
                'timeInForce': time_in_force
            }
            
            if price:
                order_params['price'] = price
            if stop_price:
                order_params['stopPrice'] = stop_price
            
            # Place the order
            result = self.client.create_order(**order_params)
            
            logger.info(f"Order placed: {result}")
            return result
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error placing order: {e}")
            return None
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return None
    
    async def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get open orders"""
        try:
            if not self.client:
                return []
            
            orders = self.client.get_open_orders(symbol=symbol)
            return orders
            
        except Exception as e:
            logger.error(f"Error getting open orders: {e}")
            return []
    
    async def cancel_order(self, symbol: str, order_id: int) -> bool:
        """Cancel an order"""
        try:
            if not self.client:
                return False
            
            result = self.client.cancel_order(symbol=symbol, orderId=order_id)
            logger.info(f"Order cancelled: {result}")
            return True
            
        except Exception as e:
            logger.error(f"Error cancelling order: {e}")
            return False
    
    async def get_symbol_info(self, symbol: str) -> Optional[Dict]:
        """Get symbol information including filters"""
        try:
            if not self.client:
                return None
            
            exchange_info = self.client.get_exchange_info()
            
            for symbol_info in exchange_info['symbols']:
                if symbol_info['symbol'] == symbol:
                    return symbol_info
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting symbol info for {symbol}: {e}")
            return None
    
    async def get_order_book(self, symbol: str, limit: int = 100) -> Optional[Dict]:
        """Get order book for a symbol"""
        try:
            if not self.client:
                return None
            
            order_book = self.client.get_order_book(symbol=symbol, limit=limit)
            
            return {
                'symbol': symbol,
                'bids': [[float(price), float(qty)] for price, qty in order_book['bids']],
                'asks': [[float(price), float(qty)] for price, qty in order_book['asks']],
                'last_update_id': order_book['lastUpdateId']
            }
            
        except Exception as e:
            logger.error(f"Error getting order book for {symbol}: {e}")
            return None
    
    def format_quantity(self, symbol_info: Dict, quantity: float) -> float:
        """Format quantity according to symbol's LOT_SIZE filter"""
        try:
            for filter_info in symbol_info['filters']:
                if filter_info['filterType'] == 'LOT_SIZE':
                    step_size = float(filter_info['stepSize'])
                    precision = len(str(step_size).split('.')[-1]) if '.' in str(step_size) else 0
                    return round(quantity - (quantity % step_size), precision)
            return quantity
        except Exception as e:
            logger.error(f"Error formatting quantity: {e}")
            return quantity
    
    def format_price(self, symbol_info: Dict, price: float) -> float:
        """Format price according to symbol's PRICE_FILTER"""
        try:
            for filter_info in symbol_info['filters']:
                if filter_info['filterType'] == 'PRICE_FILTER':
                    tick_size = float(filter_info['tickSize'])
                    precision = len(str(tick_size).split('.')[-1]) if '.' in str(tick_size) else 0
                    return round(price - (price % tick_size), precision)
            return price
        except Exception as e:
            logger.error(f"Error formatting price: {e}")
            return price