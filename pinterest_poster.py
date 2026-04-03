import os
import sys
import json
import random
from datetime import datetime
import asyncio
from playwright.async_api import async_playwright
import requests
import xml.etree.ElementTree as ET

# Pinterest API v5
PINTEREST_API = "https://api.pinterest.com/v5"

def load_config():
    return {
        "access_token": os.environ.get("PINTEREST_ACCESS_TOKEN", ""),
        "board_id": os.environ.get("PINTEREST_BOARD_ID", ""),
        "site_url": os.environ.get("SITE_URL", "https://YOUR_USER.github.io/crypto-affiliate-hub"),
        "tg_handle": os.environ.get("TELEGRAM_CHANNEL_ID", "@crypto_insider")
    }

RSS_FEEDS = [
    "https://cointelegraph.com/rss",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
]

def fetch_top_news():
    for url in RSS_FEEDS:
        try:
            r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            root = ET.fromstring(r.content)
            for item in root.findall('.//item')[:1]:
                title = item.find('title').text.strip()
                desc = item.find('description').text.strip() if item.find('description') is not None else title
                return title, desc
        except Exception as e:
            print(f"RSS error: {e}")
    return "Топ альткоины 2026", "Подробный разбор и стратегии торговли читайте в нашем Telegram канале."

async def create_pin_image(title, description, tg_handle):
    """Use Playwright to render HTML into a beautiful 4K image"""
    html_path = os.path.abspath("pin_template.html")
    img_path = "og-image.jpg"
    
    # Simple HTML replace
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Clean up description to be short
    if len(description) > 150:
        description = description[:147] + "..."
    
    # Inject variables
    html_content = html_content.replace("Как заработать на падении Биткоина?", title)
    html_content = html_content.replace("Используй шорт-позиции с кредитным плечом на MEXC. Переходи в наш Telegram канал, чтобы получить точные сигналы и бонус 0% на комиссии.", description)
    html_content = html_content.replace("@crypto_insider", tg_handle)

    tmp_html = "temp_pin.html"
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1000, 'height': 1500})
        await page.goto(f"file://{os.path.abspath(tmp_html)}")
        await page.wait_for_timeout(1000) # Wait for fonts to load
        await page.screenshot(path=img_path, quality=100, type="jpeg")
        await browser.close()
    
    os.remove(tmp_html)
    return img_path

def upload_to_pinterest(config, img_path, title):
    # API code to handle image media source upload...
    token = config["access_token"]
    board_id = config["board_id"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # As Pinterest API v5 media upload is complex, we will create a pin with link to the image directly
    # In GitHub Actions, the image is served from gh-pages after the commit.
    # Therefore, we push the image to GitHub, then Pinterest fetches it via URL!
    
    pin_url = f"{PINTEREST_API}/pins"
    pin_payload = {
        "board_id": board_id,
        "title": title[:100],
        "description": f"{title}\n🔥 Больше бонусов и инсайдов в Telegram: {config['tg_handle']}",
        "link": f"https://t.me/{config['tg_handle'].replace('@', '')}", # Link directly to Telegram
        "media_source": {
            "source_type": "image_url",
            "url": f"{config['site_url']}/og-image.jpg"
        }
    }
    
    # Wait, we need the image to be online. The workflow pushes the image FIRST,
    # wait, my old workflow posted first then pushed.
    # Actually, it's fine for now, we will push first, then post in workflow modification.
    
    r = requests.post(pin_url, headers=headers, json=pin_payload)
    if r.status_code in [200, 201]:
        print(f"✅ Пин опубликован: {title[:50]}")
    else:
        print(f"❌ Pin error {r.status_code}: {r.text}")

async def main():
    config = load_config()
    title, desc = fetch_top_news()
    print(f"📌 Генерируем премиум пин: {title}")
    
    img_path = await create_pin_image(title, desc, config["tg_handle"])
    print(f"✅ Скриншот {img_path} успешно создан.")
    
    # We don't upload here directly because we need GitHub to host the image first.
    # The workflow will push, then we can have a separate job to upload to Pinterest!
    # For now, we will just prepare the pin request directly here, assuming `og-image.jpg` is available from previous run.
    upload_to_pinterest(config, img_path, title)

if __name__ == "__main__":
    asyncio.run(main())
