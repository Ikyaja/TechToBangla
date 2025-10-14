#!/bin/bash
echo "📦 Installing V6 Ultimate dependencies..."
pip3 install --user --upgrade pip --quiet
pip3 install --user python-telegram-bot==20.7 --quiet
pip3 install --user python-binance==1.0.19 --quiet
pip3 install --user pandas==2.1.4 --quiet
pip3 install --user numpy==1.24.4 --quiet
pip3 install --user requests==2.31.0 --quiet
pip3 install --user python-dotenv==1.0.0 --quiet
pip3 install --user aiohttp==3.9.1 --quiet
pip3 install --user ta==0.10.2 --quiet 2>/dev/null || echo "⚠️ TA optional, using built-in"
echo "✅ Dependencies ready!"
