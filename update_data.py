import requests
import json
import os
import xml.etree.ElementTree as ET
from datetime import datetime

# Read config from config.json if exists locally, or use env vars
def load_config():
    config_path = "../config.json"
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    print("WARNING: config.json missing, using env defaults.")
    return {
        "wallet": os.environ.get("WALLET_ADDRESS", "0x0"),
        "telegram_channel": os.environ.get("TELEGRAM_CHANNEL_ID", "@your_channel"),
        "affiliate_links": {
            "mexc": os.environ.get("MEXC_LINK", "#"),
            "bybit": os.environ.get("BYBIT_LINK", "#"),
            "binance": os.environ.get("BINANCE_LINK", "#")
        }
    }

CONFIG = load_config()
RSS_FEEDS = [
    "https://cryptopanic.com/news/rss/",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss"
]

def fetch_rss_news(url):
    try:
        response = requests.get(url, timeout=10)
        root = ET.fromstring(response.content)
        news = []
        for item in root.findall('.//item')[:3]:
            title = item.find('title').text.strip()
            # News redirects directly to TG channel
            tg_handle = CONFIG.get('telegram_channel', '').replace('@', '')
            link = f"https://t.me/{tg_handle}" if tg_handle else "#"
            date = item.find('pubDate').text.strip()
            news.append({
                "title": title,
                "link": link,
                "date": date
            })
        return news
    except Exception as e:
        print(f"Ошибка при парсинге {url}: {e}")
        return []

def update_site_data():
    all_news = []
    for feed in RSS_FEEDS:
        all_news.extend(fetch_rss_news(feed))
    all_news = all_news[:10]

    data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "news": all_news,
        "config": {
            "wallet": CONFIG["wallet"],
            "links": CONFIG["affiliate_links"],
            "telegram": CONFIG["telegram_channel"]
        }
    }
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print(f"Обновлено {len(all_news)} новостей")

if __name__ == "__main__":
    update_site_data()
