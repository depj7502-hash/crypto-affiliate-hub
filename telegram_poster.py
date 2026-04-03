"""
TELEGRAM AUTO-POSTER
Автоматически постит крипто-новости в Telegram канал каждые 3 часа.
Запускается через GitHub Actions.
"""

import requests
import json
import xml.etree.ElementTree as ET
import os
import sys
from datetime import datetime
import time
import random

# --- Загружаем конфиг из переменны среды (GitHub Secrets) или файла ---
def load_config():
    try:
        # В GitHub Actions используем Secrets
        return {
            "bot_token": os.environ.get("TELEGRAM_BOT_TOKEN", ""),
            "channel_id": os.environ.get("TELEGRAM_CHANNEL_ID", ""),
            "affiliate_links": {
                "mexc": os.environ.get("MEXC_LINK", "https://www.mexc.com"),
                "bybit": os.environ.get("BYBIT_LINK", "https://www.bybit.com"),
            }
        }
    except Exception as e:
        print(f"Config error: {e}")
        sys.exit(1)

RSS_FEEDS = [
    "https://cointelegraph.com/rss",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
]

TEMPLATES = [
    "🔥 *{title}*\n\n💡 Торгуй с 0% комиссией → {link}",
    "⚡ *{title}*\n\n📈 Зарегистрируйся на лучшей бирже → {link}",
    "🚀 *{title}*\n\n💰 Получи бонус до $1000 → {link}",
    "📊 *{title}*\n\n⭐ Топ биржа 2026 → {link}",
]

def fetch_news():
    all_news = []
    for url in RSS_FEEDS:
        try:
            r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            root = ET.fromstring(r.content)
            for item in root.findall('.//item')[:3]:
                title_el = item.find('title')
                if title_el is not None and title_el.text:
                    all_news.append(title_el.text.strip())
        except Exception as e:
            print(f"RSS error {url}: {e}")
    return all_news

def send_telegram(bot_token, channel_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": channel_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        result = r.json()
        if result.get("ok"):
            print(f"✅ Успешно отправлено в {channel_id}")
            return True
        else:
            print(f"❌ Ошибка Telegram: {result}")
            return False
    except Exception as e:
        print(f"❌ Сетевая ошибка: {e}")
        return False

def main():
    config = load_config()
    
    if not config["bot_token"] or not config["channel_id"]:
        print("❌ TELEGRAM_BOT_TOKEN или TELEGRAM_CHANNEL_ID не настроены в GitHub Secrets!")
        sys.exit(1)

    news_list = fetch_news()
    
    if not news_list:
        print("Новостей не найдено — выходим")
        return

    # Берём рандомную новость и рандомный шаблон
    title = random.choice(news_list)
    template = random.choice(TEMPLATES)
    affiliate_link = random.choice(list(config["affiliate_links"].values()))
    
    message = template.format(title=title, link=affiliate_link)
    
    success = send_telegram(config["bot_token"], config["channel_id"], message)
    
    if success:
        print(f"Пост отправлен: {datetime.now().strftime('%H:%M')}")

if __name__ == "__main__":
    main()
