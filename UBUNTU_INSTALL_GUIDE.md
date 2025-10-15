# 🚀 PANDUAN LENGKAP INSTALL BOT DI UBUNTU

## 📋 DAFTAR ISI
1. [Persiapan & Requirements](#1-persiapan--requirements)
2. [Install Python & Dependencies](#2-install-python--dependencies)
3. [Copy Bot ke Server](#3-copy-bot-ke-server)
4. [Install Bot Dependencies](#4-install-bot-dependencies)
5. [Konfigurasi Bot](#5-konfigurasi-bot)
6. [Jalankan Bot](#6-jalankan-bot)
7. [Setup Auto-Start (24/7)](#7-setup-auto-start-247)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. PERSIAPAN & REQUIREMENTS

### ✅ Yang Anda Butuhkan:

1. **Ubuntu Server** (18.04 / 20.04 / 22.04)
   - VPS dari DigitalOcean, Vultr, AWS, dll
   - Minimal: 1GB RAM, 1 CPU
   - Recommended: 2GB RAM, 2 CPU

2. **Telegram Bot Token**
   - Sudah ada: `8285776454:AAE2lg7Lrkc0e7dVNFTMPef_dZEQ6JK4Wko`

3. **Binance API Keys** (optional, ada demo mode)
   - Sudah ada di config

4. **SSH Access** ke Ubuntu server

---

## 2. INSTALL PYTHON & DEPENDENCIES

### 📦 Step 2.1: Update System

```bash
# Login ke Ubuntu server via SSH
ssh user@your-server-ip

# Update package list
sudo apt update

# Upgrade packages
sudo apt upgrade -y
```

### 📦 Step 2.2: Install Python 3.10 (Recommended!)

Ubuntu 22.04 sudah include Python 3.10, tapi jika belum:

```bash
# Cek Python version
python3 --version

# Jika < 3.10 atau > 3.11, install Python 3.10:
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev -y

# Install pip
sudo apt install python3-pip -y

# Upgrade pip
python3.10 -m pip install --upgrade pip
```

### 📦 Step 2.3: Install System Dependencies

```bash
# Install required system packages
sudo apt install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    git \
    curl \
    wget \
    screen \
    tmux

# Install untuk kompilasi (jika diperlukan)
sudo apt install -y \
    python3-dev \
    gcc \
    g++

echo "✅ System dependencies installed!"
```

---

## 3. COPY BOT KE SERVER

### 📂 Step 3.1: Buat Directory untuk Bot

```bash
# Buat directory
mkdir -p ~/trading_bots
cd ~/trading_bots

echo "✅ Directory created: ~/trading_bots"
```

### 📂 Step 3.2: Copy Bot Files

**Pilihan A: Via SCP (dari komputer lokal)**

```bash
# Dari komputer lokal Anda:
# Copy V5
scp -r /workspace/telegram_bot user@your-server-ip:~/trading_bots/bot_v5

# Copy V6
scp -r /workspace/bot_v6_ultimate user@your-server-ip:~/trading_bots/bot_v6
```

**Pilihan B: Via Git (jika ada repo)**

```bash
# Di server
cd ~/trading_bots
git clone your-repo-url
```

**Pilihan C: Manual Copy-Paste**

```bash
# Buat structure manual
cd ~/trading_bots
mkdir -p bot_v5/{modules,config,logs}
mkdir -p bot_v6/{modules,config,logs}

# Kemudian copy-paste content file per file (dijelaskan di bawah)
```

---

## 4. INSTALL BOT DEPENDENCIES

### 📦 Step 4.1: Create Virtual Environment (Recommended!)

```bash
# Masuk ke directory bot
cd ~/trading_bots/bot_v6  # atau bot_v5

# Buat virtual environment
python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Sekarang terminal akan show (venv) di depan

echo "✅ Virtual environment created & activated!"
```

### 📦 Step 4.2: Install Python Dependencies

```bash
# Pastikan venv aktif (ada tulisan (venv) di terminal)

# Upgrade pip
pip install --upgrade pip

# Install dependencies satu per satu
pip install python-telegram-bot==20.7
pip install python-binance==1.0.19
pip install python-dotenv==1.0.0
pip install aiohttp==3.9.1
pip install requests==2.31.0

# Install pandas & numpy (compatible versions)
pip install pandas==2.0.3
pip install numpy==1.24.4

# Install TA library (optional, bot bisa jalan tanpa ini)
pip install ta==0.10.2

echo "✅ All dependencies installed!"
```

**Jika ada error saat install pandas:**

```bash
# Install pre-built wheels (lebih mudah)
pip install --upgrade pip setuptools wheel
pip install pandas numpy --no-build-isolation
```

### 📦 Step 4.3: Verify Installation

```bash
# Test import semua library
python3 << 'PYEOF'
try:
    import telegram
    print("✅ python-telegram-bot: OK")
except:
    print("❌ python-telegram-bot: FAILED")

try:
    import binance
    print("✅ python-binance: OK")
except:
    print("❌ python-binance: FAILED")

try:
    import pandas
    print("✅ pandas: OK")
except:
    print("❌ pandas: FAILED")

try:
    import numpy
    print("✅ numpy: OK")
except:
    print("❌ numpy: FAILED")

try:
    from dotenv import load_dotenv
    print("✅ python-dotenv: OK")
except:
    print("❌ python-dotenv: FAILED")

print("\n✅ Dependency check complete!")
PYEOF
```

---

## 5. KONFIGURASI BOT

### ⚙️ Step 5.1: Edit Config File

```bash
# Edit .env file
nano config/.env
```

**Isi file .env:**
```env
TELEGRAM_BOT_TOKEN=8285776454:AAE2lg7Lrkc0e7dVNFTMPef_dZEQ6JK4Wko
BINANCE_API_KEY=8a81A0t9zsXIRtaPHBhK9nHw9oezbZZHhepnvcJVoiDu0obJ3DaOQl5tcEm20jpS
BINANCE_SECRET_KEY=8ZrwXhPRyPB0YGKkFIyba1ajoD90eAccHzd0nV1u2qTbMvMip4VQ0OXdp38mukva
BOT_NAME=AI FUTURE SIGNAL V6 ULTIMATE
DEFAULT_LEVERAGE=125
```

**Save:** Ctrl+O, Enter, Ctrl+X

### ⚙️ Step 5.2: Set Permissions

```bash
# Make main.py executable
chmod +x main.py

# Make run script executable (jika ada)
chmod +x RUN_V6_ULTIMATE.sh

echo "✅ Permissions set!"
```

---

## 6. JALANKAN BOT

### 🚀 Step 6.1: Test Run (Foreground)

```bash
# Pastikan di directory bot dan venv aktif
cd ~/trading_bots/bot_v6  # atau bot_v5
source venv/bin/activate

# Run bot
python3 main.py
```

**Output yang diharapkan:**
```
🔥 AI FUTURE SIGNAL BOT V6.0 ULTIMATE
==========================================
✅ Bot initialized successfully
📊 Starting signal monitoring...
✅ Bot is running! Press Ctrl+C to stop.
```

**Test di Telegram:**
1. Open Telegram
2. Search bot Anda
3. Send: `/start`
4. Jika muncul welcome message = **SUCCESS!** ✅

**Stop bot:** Ctrl+C

---

### 🚀 Step 6.2: Run in Background dengan Screen

Screen memungkinkan bot jalan terus meskipun SSH disconnect.

```bash
# Install screen (jika belum ada)
sudo apt install screen -y

# Start screen session
screen -S trading_bot

# Di dalam screen, jalankan bot
cd ~/trading_bots/bot_v6
source venv/bin/activate
python3 main.py

# Detach dari screen (bot tetap jalan):
# Tekan: Ctrl+A lalu D

# Bot sekarang running di background! ✅
```

**Useful Screen Commands:**
```bash
# Lihat running screens
screen -ls

# Attach kembali ke screen
screen -r trading_bot

# Kill screen
screen -S trading_bot -X quit

# Detach dari screen
Ctrl+A lalu D
```

---

### 🚀 Step 6.3: Run dengan Systemd (Auto-Restart)

Systemd lebih robust - bot auto-restart jika crash!

```bash
# Buat systemd service file
sudo nano /etc/systemd/system/trading-bot-v6.service
```

**Isi file:**
```ini
[Unit]
Description=AI Future Signal Bot V6 Ultimate
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/trading_bots/bot_v6
Environment="PATH=/home/ubuntu/trading_bots/bot_v6/venv/bin"
ExecStart=/home/ubuntu/trading_bots/bot_v6/venv/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**IMPORTANT:** Ganti `ubuntu` dengan username Anda!

**Save:** Ctrl+O, Enter, Ctrl+X

**Activate service:**
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (auto-start on boot)
sudo systemctl enable trading-bot-v6

# Start service
sudo systemctl start trading-bot-v6

# Check status
sudo systemctl status trading-bot-v6
```

**Useful Systemd Commands:**
```bash
# Start bot
sudo systemctl start trading-bot-v6

# Stop bot
sudo systemctl stop trading-bot-v6

# Restart bot
sudo systemctl restart trading-bot-v6

# Check status
sudo systemctl status trading-bot-v6

# View logs
sudo journalctl -u trading-bot-v6 -f

# Disable auto-start
sudo systemctl disable trading-bot-v6
```

---

## 7. SETUP AUTO-START (24/7)

### 🔄 Step 7.1: Test Auto-Restart

```bash
# Dengan systemd, bot akan auto-restart jika crash

# Test: Kill bot process
sudo systemctl stop trading-bot-v6
# Wait 10 seconds
sudo systemctl status trading-bot-v6
# Should show "active (running)"

echo "✅ Auto-restart working!"
```

### 🔄 Step 7.2: Test Server Reboot

```bash
# Reboot server
sudo reboot

# Wait 2-3 minutes, login kembali
ssh user@your-server-ip

# Check bot status
sudo systemctl status trading-bot-v6
# Should show "active (running)"

echo "✅ Auto-start on boot working!"
```

---

## 8. TROUBLESHOOTING

### ❌ Problem 1: "Module not found"

**Solution:**
```bash
# Make sure virtual environment is active
source ~/trading_bots/bot_v6/venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Or install manually
pip install python-telegram-bot==20.7 python-binance==1.0.19 python-dotenv aiohttp
```

---

### ❌ Problem 2: "Telegram Bot Token Invalid"

**Solution:**
```bash
# Check .env file
cat config/.env

# Make sure token tidak ada spasi/newline extra
# Regenerate token dari @BotFather jika perlu

# Edit .env
nano config/.env
# Save: Ctrl+O, Enter, Ctrl+X

# Restart bot
sudo systemctl restart trading-bot-v6
```

---

### ❌ Problem 3: "Binance API Error"

**Solution:**
```bash
# Bot otomatis pindah ke demo mode jika Binance blocked
# Cek logs:
tail -f logs/bot_v6.log

# Jika mau force demo mode, edit binance_client.py:
# self.demo_mode = True
```

---

### ❌ Problem 4: "Permission Denied"

**Solution:**
```bash
# Set permissions
chmod +x main.py
chmod -R 755 ~/trading_bots/bot_v6

# Make sure logs directory writable
mkdir -p logs
chmod 777 logs
```

---

### ❌ Problem 5: "Pandas/Numpy Build Error"

**Solution:**
```bash
# Install pre-built wheels
pip install --upgrade pip setuptools wheel

# Use compatible versions
pip install pandas==2.0.3 numpy==1.24.4

# Or skip pandas (bot will use built-in)
# Bot tetap jalan tanpa pandas!
```

---

### ❌ Problem 6: Bot Crash/Stop

**Solution:**
```bash
# View logs
sudo journalctl -u trading-bot-v6 -n 100

# Or
tail -50 logs/bot_v6.log

# Restart bot
sudo systemctl restart trading-bot-v6

# Check status
sudo systemctl status trading-bot-v6
```

---

## 9. MONITORING & MAINTENANCE

### 📊 Step 9.1: Monitor Bot

```bash
# View live logs
sudo journalctl -u trading-bot-v6 -f

# Or
tail -f logs/bot_v6.log

# Check bot status
sudo systemctl status trading-bot-v6

# Check resource usage
htop
# Look for python3 process
```

### 📊 Step 9.2: Check Bot Health

```bash
# Telegram: Send /status to bot
# Should show:
# 🟢 Status: Online
# 👥 Active Users: X
# ⏰ Last Update: ...

# Server: Check process
ps aux | grep main.py

# Check memory usage
free -h

# Check disk space
df -h
```

### 📊 Step 9.3: Update Bot

```bash
# Stop bot
sudo systemctl stop trading-bot-v6

# Backup current version
cp -r ~/trading_bots/bot_v6 ~/trading_bots/bot_v6_backup_$(date +%Y%m%d)

# Update files (via scp, git, atau manual)
# ...

# Restart bot
sudo systemctl start trading-bot-v6

# Check status
sudo systemctl status trading-bot-v6
```

---

## 10. SECURITY BEST PRACTICES

### 🔒 Step 10.1: Secure API Keys

```bash
# Set proper permissions on .env
chmod 600 config/.env

# Only owner can read/write
ls -la config/.env
# Should show: -rw------- 1 user user
```

### 🔒 Step 10.2: Setup Firewall

```bash
# Enable UFW firewall
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTPS (jika diperlukan)
sudo ufw allow 443/tcp

# Check status
sudo ufw status

echo "✅ Firewall configured!"
```

### 🔒 Step 10.3: Regular Backups

```bash
# Create backup script
cat > ~/backup_bot.sh << 'BACKUPEOF'
#!/bin/bash
BACKUP_DIR=~/bot_backups
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup V6
tar -czf $BACKUP_DIR/bot_v6_$DATE.tar.gz ~/trading_bots/bot_v6

# Keep only last 7 backups
cd $BACKUP_DIR
ls -t bot_v6_*.tar.gz | tail -n +8 | xargs rm -f

echo "✅ Backup complete: bot_v6_$DATE.tar.gz"
BACKUPEOF

chmod +x ~/backup_bot.sh

# Add to crontab (daily backup at 3 AM)
(crontab -l 2>/dev/null; echo "0 3 * * * ~/backup_bot.sh") | crontab -

echo "✅ Auto-backup configured!"
```

---

## 11. COMPLETE INSTALLATION SCRIPT

### 🚀 All-in-One Script

Saya buatkan script yang install SEMUA otomatis:

```bash
#!/bin/bash

echo "🔥 AI FUTURE SIGNAL BOT - AUTO INSTALLER"
echo "Installing V6 ULTIMATE on Ubuntu..."
echo ""

# Update system
echo "📦 Updating system..."
sudo apt update && sudo apt upgrade -y

# Install Python 3.10
echo "🐍 Installing Python 3.10..."
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3.10-dev python3-pip

# Install system dependencies
echo "📦 Installing system packages..."
sudo apt install -y build-essential libssl-dev libffi-dev git curl wget screen

# Create directory
echo "📂 Creating directories..."
mkdir -p ~/trading_bots/bot_v6/{modules,config,logs}
cd ~/trading_bots/bot_v6

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3.10 -m venv venv
source venv/bin/activate

# Install Python packages
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install python-telegram-bot==20.7
pip install python-binance==1.0.19
pip install python-dotenv==1.0.0
pip install aiohttp==3.9.1
pip install requests==2.31.0
pip install pandas==2.0.3
pip install numpy==1.24.4
pip install ta==0.10.2 2>/dev/null || echo "TA library optional"

echo ""
echo "✅ Installation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Copy bot files to ~/trading_bots/bot_v6/"
echo "2. Configure config/.env"
echo "3. Run: python3 main.py"
echo ""
```

Save as `install_bot.sh` dan run:
```bash
chmod +x install_bot.sh
./install_bot.sh
```

---

## 12. STEP-BY-STEP COPY FILES

### 📄 Manual Copy Method (jika tidak bisa SCP)

#### **File 1: config/.env**
```bash
nano ~/trading_bots/bot_v6/config/.env
```
Copy paste dari `/workspace/bot_v6_ultimate/config/.env`

#### **File 2: main.py**
```bash
nano ~/trading_bots/bot_v6/main.py
```
Copy paste dari `/workspace/bot_v6_ultimate/main.py`

#### **File 3: modules/technical_analysis_v6.py**
```bash
nano ~/trading_bots/bot_v6/modules/technical_analysis_v6.py
```
Copy paste dari `/workspace/bot_v6_ultimate/modules/technical_analysis_v6.py`

#### **File 4: modules/signal_generator_v6.py**
```bash
nano ~/trading_bots/bot_v6/modules/signal_generator_v6.py
```
Copy paste dari `/workspace/bot_v6_ultimate/modules/signal_generator_v6.py`

#### **File 5: modules/ui_formatter_v6.py**
```bash
nano ~/trading_bots/bot_v6/modules/ui_formatter_v6.py
```
Copy paste dari `/workspace/bot_v6_ultimate/modules/ui_formatter_v6.py`

#### **File 6: modules/binance_client.py**
```bash
nano ~/trading_bots/bot_v6/modules/binance_client.py
```
Copy paste dari `/workspace/bot_v6_ultimate/modules/binance_client.py`

#### **File 7: modules/__init__.py**
```bash
touch ~/trading_bots/bot_v6/modules/__init__.py
touch ~/trading_bots/bot_v6/__init__.py
```

---

## 13. FINAL CHECKLIST

### ✅ Pre-Run Checklist:

```bash
# 1. Check structure
cd ~/trading_bots/bot_v6
ls -la
# Should show: main.py, modules/, config/, logs/

# 2. Check modules
ls -la modules/
# Should show: technical_analysis_v6.py, signal_generator_v6.py, ui_formatter_v6.py, binance_client.py

# 3. Check config
ls -la config/
# Should show: .env

# 4. Check permissions
ls -l main.py
# Should show: -rwxr-xr-x

# 5. Check venv
source venv/bin/activate
which python3
# Should show: ~/trading_bots/bot_v6/venv/bin/python3

# 6. Test imports
python3 -c "from modules.technical_analysis_v6 import V6TechnicalAnalyzer; print('✅ Import OK')"

# 7. All OK? RUN!
python3 main.py
```

---

## 14. PRODUCTION DEPLOYMENT

### 🏭 Complete Production Setup:

```bash
# 1. Stop any running bots
sudo systemctl stop trading-bot-v6 2>/dev/null
screen -S trading_bot -X quit 2>/dev/null

# 2. Setup systemd service
sudo nano /etc/systemd/system/trading-bot-v6.service
```

**Content:**
```ini
[Unit]
Description=AI Future Signal Bot V6 Ultimate
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/trading_bots/bot_v6
Environment="PATH=/home/ubuntu/trading_bots/bot_v6/venv/bin"
ExecStart=/home/ubuntu/trading_bots/bot_v6/venv/bin/python3 main.py
Restart=always
RestartSec=10
StandardOutput=append:/home/ubuntu/trading_bots/bot_v6/logs/bot_output.log
StandardError=append:/home/ubuntu/trading_bots/bot_v6/logs/bot_error.log

[Install]
WantedBy=multi-user.target
```

**Ganti `ubuntu` dengan username Anda!**

```bash
# 3. Enable & Start
sudo systemctl daemon-reload
sudo systemctl enable trading-bot-v6
sudo systemctl start trading-bot-v6

# 4. Verify
sudo systemctl status trading-bot-v6

# 5. Check logs
tail -f logs/bot_output.log

echo "✅ Production deployment complete!"
```

---

## 15. QUICK REFERENCE

### 📋 Common Commands:

```bash
# Start bot (systemd)
sudo systemctl start trading-bot-v6

# Stop bot
sudo systemctl stop trading-bot-v6

# Restart bot
sudo systemctl restart trading-bot-v6

# View logs
sudo journalctl -u trading-bot-v6 -f

# Or
tail -f ~/trading_bots/bot_v6/logs/bot_v6.log

# Check status
sudo systemctl status trading-bot-v6

# Activate venv
cd ~/trading_bots/bot_v6
source venv/bin/activate

# Run manually
python3 main.py

# Run in screen
screen -S trading_bot
python3 main.py
# Detach: Ctrl+A, D

# Attach to screen
screen -r trading_bot
```

---

## 16. COMPLETE EXAMPLE WALKTHROUGH

### 🎯 Example: Fresh Ubuntu 22.04 Server

```bash
# ========================================
# COMPLETE INSTALLATION - COPY PASTE INI!
# ========================================

# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python & tools
sudo apt install -y python3.10 python3.10-venv python3-pip screen git

# 3. Create directory
mkdir -p ~/trading_bots/bot_v6
cd ~/trading_bots/bot_v6

# 4. Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip install --upgrade pip
pip install python-telegram-bot==20.7
pip install python-binance==1.0.19  
pip install python-dotenv==1.0.0
pip install aiohttp==3.9.1
pip install pandas==2.0.3 numpy==1.24.4

# 6. Create structure
mkdir -p modules config logs
touch modules/__init__.py __init__.py

# 7. Copy files
# (Copy semua file dari /workspace/bot_v6_ultimate/)
# Via SCP, Git, atau manual copy-paste

# 8. Test run
python3 main.py

# 9. If OK, setup systemd
sudo nano /etc/systemd/system/trading-bot-v6.service
# (Copy content dari section 14)

# 10. Enable & start
sudo systemctl daemon-reload
sudo systemctl enable trading-bot-v6
sudo systemctl start trading-bot-v6

# 11. Check status
sudo systemctl status trading-bot-v6

# ========================================
# DONE! BOT RUNNING 24/7! ✅
# ========================================
```

---

## 17. TESTING CHECKLIST

### ✅ Setelah Install:

```bash
# 1. Bot running?
sudo systemctl status trading-bot-v6
# Should show: active (running) ✅

# 2. No errors in logs?
tail -50 logs/bot_v6.log
# Should not show critical errors ✅

# 3. Telegram responding?
# Open Telegram, send /start
# Should get welcome message ✅

# 4. Analysis working?
# Telegram: Click "📈 Analysis"
# Choose pair & timeframe
# Should get analysis in 15-20 sec ✅

# 5. V6 features active?
# Telegram: Send /v6
# Should list all 10 features ✅

# ALL OK? READY TO TRADE! 🚀
```

---

## 18. BACKUP & RESTORE

### 💾 Backup Bot:

```bash
# Quick backup
cd ~/trading_bots
tar -czf bot_v6_backup_$(date +%Y%m%d).tar.gz bot_v6/

# Backup to remote
scp bot_v6_backup_*.tar.gz user@backup-server:/backups/
```

### 💾 Restore Bot:

```bash
# Stop bot
sudo systemctl stop trading-bot-v6

# Extract backup
cd ~/trading_bots
tar -xzf bot_v6_backup_20251014.tar.gz

# Restart bot
sudo systemctl start trading-bot-v6
```

---

## 19. PERFORMANCE OPTIMIZATION

### ⚡ Step 19.1: Optimize Python

```bash
# Use Python with optimizations
# Edit systemd service:
sudo nano /etc/systemd/system/trading-bot-v6.service

# Change ExecStart to:
ExecStart=/home/ubuntu/trading_bots/bot_v6/venv/bin/python3 -O main.py
#                                                           ^^^ optimization flag

# Reload & restart
sudo systemctl daemon-reload
sudo systemctl restart trading-bot-v6
```

### ⚡ Step 19.2: Increase Resources (jika lambat)

```bash
# Check current resources
htop

# If needed, upgrade VPS:
# - More RAM (2GB → 4GB)
# - More CPU (1 core → 2 cores)
# - Faster disk (HDD → SSD)
```

---

## 20. COMMON ISSUES & SOLUTIONS

| Issue | Solution |
|-------|----------|
| Bot tidak start | Check logs: `sudo journalctl -u trading-bot-v6 -n 50` |
| Import error | Reinstall: `pip install -r requirements.txt` |
| Telegram tidak respond | Check token di `.env`, restart bot |
| High CPU usage | Normal saat analysis, reduce scan frequency |
| High memory | Normal 100-300MB, restart if > 500MB |
| Binance API error | Bot auto demo mode, or update API keys |
| Permission denied | `chmod 755 -R ~/trading_bots/bot_v6` |
| Pandas error | Use Python 3.10, or skip pandas (built-in works) |

---

## 🎯 SUMMARY COMMANDS

### 📋 Quick Setup (Copy-Paste):

```bash
# Install
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.10 python3.10-venv python3-pip screen
mkdir -p ~/trading_bots/bot_v6 && cd ~/trading_bots/bot_v6
python3.10 -m venv venv && source venv/bin/activate
pip install --upgrade pip
pip install python-telegram-bot==20.7 python-binance==1.0.19 python-dotenv aiohttp pandas==2.0.3 numpy==1.24.4

# Copy files (via SCP or manual)
# ...

# Run
python3 main.py

# Or with screen
screen -S trading_bot
python3 main.py
# Ctrl+A, D to detach

# Or with systemd (production)
# (Setup service file seperti di section 14)
sudo systemctl enable trading-bot-v6
sudo systemctl start trading-bot-v6
sudo systemctl status trading-bot-v6
```

---

## 🔥 FINAL NOTES:

### ✅ What You'll Have After Installation:

1. ✅ **Bot running 24/7** on Ubuntu server
2. ✅ **Auto-restart** if crash (with systemd)
3. ✅ **Auto-start** on server reboot
4. ✅ **Logging** all activities
5. ✅ **Secure** with proper permissions
6. ✅ **Backed up** automatically
7. ✅ **Monitoring** via systemd
8. ✅ **Professional deployment** ready!

### 🎯 Recommended Setup:

- **VPS:** 2GB RAM, 2 CPU, 20GB SSD
- **Python:** 3.10 or 3.11
- **Deployment:** Systemd (auto-restart)
- **Monitoring:** Logs + systemd status
- **Backup:** Daily automatic
- **Security:** Firewall + secure keys

---

## 💎 DONE!

Follow panduan ini step-by-step dan bot Anda akan running 24/7 di Ubuntu! 🚀

**Questions?** Check troubleshooting section atau contact @Ulascryptomaster

**Happy Trading!** 💰🎯

---

Created: 2025-10-14
Version: Complete Ubuntu Install Guide
For: V5 & V6 Ultimate Bots
