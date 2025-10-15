import logging

logger = logging.getLogger(__name__)

class AutoTrader:
    def __init__(self, binance_client):
        self.binance_client = binance_client
        self.user_settings = {}
    
    def enable_auto_trading(self, user_id: int):
        self.user_settings[user_id] = {'auto_trading_enabled': True}
        logger.info(f"Auto trading enabled for user {user_id}")
    
    def disable_auto_trading(self, user_id: int):
        if user_id in self.user_settings:
            self.user_settings[user_id]['auto_trading_enabled'] = False
        logger.info(f"Auto trading disabled for user {user_id}")
