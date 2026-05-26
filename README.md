# 📊 Telegram MediaInfo Bot

> **Note**  
> This is a useless repository I made.

A simple Telegram bot built with Pyrogram to extract MediaInfo/FFprobe metadata from media files (videos, audio, documents) via direct streaming.

---

## 📢 Credits & Channels

* **Telegram Channel:** [@cantarellabots](https://t.me/cantarellabots)
* **Developer:** [@cantarella-wuwa](https://t.me/cantarella_wuwa)

---

## 🛠️ Features

* **Instant Header Probing:** Uses streaming to fetch MediaInfo without downloading the entire file.
* **Fallback Support:** Uses FFprobe automatically if MediaInfo is not installed.
* **Large File Support:** Automatically generates and uploads a `.txt` file if the formatted MediaInfo output exceeds Telegram's 4096-character limit.
* **Database Support:** Motor (MongoDB) integration for admin controls and user ban management.

---

## 🚀 Setup & Installation

### 1. Prerequisites
Make sure you have Python 3.8+ installed, along with:
* `mediainfo` and/or `ffmpeg`/`ffprobe` in your system PATH.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configuration
Rename/edit `config.py` and populate the following values:
* `API_ID` & `API_HASH` (from [my.telegram.org](https://my.telegram.org))
* `BOT_TOKEN` (from [@BotFather](https://t.me/BotFather))
* `MONGO_URI` (MongoDB connection string)
* `OWNER_ID` (Your Telegram user ID)

### 4. Run the Bot
```bash
py bot.py
```
