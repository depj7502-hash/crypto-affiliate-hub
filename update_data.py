import requests
import json
import os
import xml.etree.ElementTree as ET
from datetime import datetime

# --- КОНФИГУРАЦИЯ (ОТРЕДАКТИРУЙ ЭТО) ---
CONFIG = {
    "wallet": "0x5555555555555555555555555555555555555555", # Твой кошелек
    "affiliate_links": {
        "mexc": "https://www.mexc.com/register?inviteCode=YOUR_CODE",
        "bybit": "https://www.bybit.com/register?affiliate_id=YOUR_CODE",
        "binance": "https://accounts.binance.com/register?ref=YOUR_CODE"
    },
    "rss_feeds": [
        "https://cryptopanic.com/news/rss/",
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://cointelegraph.com/rss"
    ]
}

def fetch_rss_news(url):
    """Парсит новости из RSS ленты"""
    try:
        response = requests.get(url, timeout=10)
        root = ET.fromstring(response.content)
        news = []
        for item in root.findall('.//item')[:5]: # Берем топ-5 новостей из каждой ленты
            title = item.find('title').text
            news.append({
                "title": title,
                "time": datetime.now().strftime("%H:%M") # Упрощаем время для UI
            })
        return news
    except Exception as e:
        print(f"Ошибка при парсинге {url}: {e}")
        return []

def update_site_data():
    all_news = []
    for feed in CONFIG["rss_feeds"]:
        all_news.extend(fetch_rss_news(feed))
    
    # Сортируем или обрезаем до топ-10
    all_news = all_news[:10]

    data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "news": all_news,
        "config": {
            "wallet": CONFIG["wallet"],
            "links": CONFIG["affiliate_links"]
        }
    }
    
    # Сохраняем в папку хаба
    # Путь зависит от того, где запущен скрипт (локально или в GitHub Actions)
    output_path = "data.json"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print(f"Обновлено {len(all_news)} новостей в {output_path}")

if __name__ == "__main__":
    update_site_data()
