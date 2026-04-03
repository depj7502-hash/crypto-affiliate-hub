import os
import sys
import json
import random
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlencode

def load_config():
    config_path = "../config.json"
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    print("WARNING: config.json missing, using env defaults.")
    return {
        "telegram_bot_token": os.environ.get("TELEGRAM_BOT_TOKEN", ""),
        "telegram_channel": os.environ.get("TELEGRAM_CHANNEL_ID", ""),
        "affiliate_links": {
            "mexc": os.environ.get("MEXC_LINK", "#"),
            "bybit": os.environ.get("BYBIT_LINK", "#"),
            "binance": os.environ.get("BINANCE_LINK", "#")
        }
    }

CONFIG = load_config()
RSS_FEEDS = ["https://cointelegraph.com/rss", "https://www.coindesk.com/arc/outboundfeeds/rss/"]

# English Templates for the pixel art crypto empire
POST_TEMPLATES = [
    "🚨 <b>BREAKING NEWS</b> 🚨\n\n{title}\n\n{desc}\n\n⚡ <b>Trade this trend with 0% fees on MEXC:</b>\n<a href='{mexc}'>[ JOIN MEXC NOW ]</a>",
    "📈 <b>MARKET INSIGHT</b> 📈\n\n{title}\n\n{desc}\n\n🔥 <b>Don't miss the move! Get up to $30k bonus on Bybit:</b>\n<a href='{bybit}'>[ CLAIM BYBIT BONUS ]</a>",
    "🌐 <b>CRYPTO RADAR</b> 🌐\n\n{title}\n\n{desc}\n\n🛡️ <b>Secure your profits on Binance, the safest exchange:</b>\n<a href='{binance}'>[ REGISTER ON BINANCE ]</a>"
]

def fetch_top_news():
    for url in RSS_FEEDS:
        try:
            r = requests.get(url, timeout=10)
            root = ET.fromstring(r.content)
            for item in root.findall('.//item'):
                title = item.find('title').text.strip()
                desc = item.find('description').text.strip() if item.find('description') is not None else ""
                # Strip HTML from desc if any
                desc = "<".join(desc.split("<")[:1]) 
                return title, desc
        except Exception:
            continue
    return "Bitcoin hits new milestone!", "Whales are moving massive amounts of liquidity."

def send_telegram_message(text):
    bot_token = CONFIG.get("telegram_bot_token")
    channel_id = CONFIG.get("telegram_channel")
    if not bot_token or not channel_id:
        print("Telegram credentials missing!")
        return
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": channel_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    r = requests.post(url, json=payload)
    print(f"Telegram API: {r.status_code}")
    print(r.text)

if __name__ == "__main__":
    title, desc = fetch_top_news()
    if len(desc) > 300:
        desc = desc[:297] + "..."
    
    template = random.choice(POST_TEMPLATES)
    links = CONFIG.get("affiliate_links", {})
    post_text = template.format(
        title=title, 
        desc=desc, 
        mexc=links.get("mexc", "#"), 
        bybit=links.get("bybit", "#"), 
        binance=links.get("binance", "#")
    )
    send_telegram_message(post_text)
