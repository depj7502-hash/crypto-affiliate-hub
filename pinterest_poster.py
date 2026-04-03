"""
PINTEREST AUTO-POSTER
Автоматически публикует крипто-пины на Pinterest каждый день.
Пины ведут на наш affiliate hub.
Запускается через GitHub Actions (однажды в день).
"""

import requests
import json
import xml.etree.ElementTree as ET
import os
import sys
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import random

# Pinterest API v5
PINTEREST_API = "https://api.pinterest.com/v5"

def load_config():
    return {
        "access_token": os.environ.get("PINTEREST_ACCESS_TOKEN", ""),
        "board_id": os.environ.get("PINTEREST_BOARD_ID", ""),
        "site_url": os.environ.get("SITE_URL", "https://YOUR_USERNAME.github.io/crypto-affiliate-hub"),
    }

RSS_FEEDS = [
    "https://cointelegraph.com/rss",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
]

# Цветовые схемы для пинов
COLOR_SCHEMES = [
    {"bg": (5, 5, 5), "accent": (0, 242, 255), "text": (255, 255, 255)},
    {"bg": (10, 0, 30), "accent": (112, 0, 255), "text": (255, 255, 255)},
    {"bg": (0, 20, 0), "accent": (0, 255, 100), "text": (255, 255, 255)},
    {"bg": (30, 0, 0), "accent": (255, 100, 0), "text": (255, 255, 255)},
]

def fetch_top_news():
    """Берём одну топ-новость дня"""
    for url in RSS_FEEDS:
        try:
            r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            root = ET.fromstring(r.content)
            for item in root.findall('.//item')[:1]:
                title_el = item.find('title')
                if title_el is not None and title_el.text:
                    return title_el.text.strip()
        except Exception as e:
            print(f"RSS error: {e}")
    return f"Топ монеты для инвестиций в {datetime.now().strftime('%B %Y')}"

def create_pin_image(title: str) -> io.BytesIO:
    """Создаёт красивое изображение для пина (1000x1500px)"""
    width, height = 1000, 1500
    scheme = random.choice(COLOR_SCHEMES)
    
    img = Image.new("RGB", (width, height), scheme["bg"])
    draw = ImageDraw.Draw(img)
    
    # Фоновый градиент (рисуем линиями)
    for y in range(height):
        alpha = y / height
        r = int(scheme["bg"][0] * (1 - alpha) + scheme["accent"][0] * alpha * 0.3)
        g = int(scheme["bg"][1] * (1 - alpha) + scheme["accent"][1] * alpha * 0.3)
        b = int(scheme["bg"][2] * (1 - alpha) + scheme["accent"][2] * alpha * 0.3)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Декоративная полоса сверху
    draw.rectangle([(0, 0), (width, 8)], fill=scheme["accent"])
    
    # Логотип/бренд
    draw.text((50, 50), "CRYPTOHUB 2026", fill=scheme["accent"])
    
    # Иконка
    draw.ellipse([(width//2 - 60, 200), (width//2 + 60, 320)], 
                 outline=scheme["accent"], width=4)
    draw.text((width//2 - 15, 245), "₿", fill=scheme["accent"])
    
    # Заголовок новости (обёртка текста)
    words = title.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        if len(' '.join(current_line)) > 28:
            lines.append(' '.join(current_line[:-1]))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    
    y_pos = 380
    for line in lines[:4]:
        draw.text((50, y_pos), line, fill=scheme["text"])
        y_pos += 60
    
    # Нижняя CTA
    draw.rectangle([(50, 1300), (width - 50, 1400)], fill=scheme["accent"])
    draw.text((width//2 - 120, 1330), "ОТКРЫТЬ БИРЖУ →", fill=scheme["bg"])
    
    # Сохраняем в буфер
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=95)
    buffer.seek(0)
    return buffer

def upload_to_pinterest(config, image_buffer, title, link):
    """Загружает пин в Pinterest через API v5"""
    token = config["access_token"]
    board_id = config["board_id"]
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Сначала загружаем медиа
    # Pinterest API v5 требует pre-upload для images
    media_url = f"{PINTEREST_API}/media"
    media_payload = {"media_type": "image"}
    
    r = requests.post(media_url, headers=headers, json=media_payload)
    
    if r.status_code != 201:
        print(f"❌ Media pre-upload error: {r.text}")
        return False
    
    upload_data = r.json()
    upload_url = upload_data.get("upload_url")
    media_id = upload_data.get("media_id")
    
    if not upload_url:
        # Простой способ через прямую ссылку на изображение
        # Публикуем пин с ссылкой на внешнее изображение (из нашего сайта)
        pass
    
    # Публикуем пин
    pin_url = f"{PINTEREST_API}/pins"
    pin_payload = {
        "board_id": board_id,
        "title": title[:100],
        "description": f"{title} | Лучшие крипто биржи 2026 | Бонусы и 0% комиссии",
        "link": link,
        "media_source": {
            "source_type": "image_url",
            "url": f"{config['site_url']}/og-image.jpg"  # Используем статичное OG изображение
        }
    }
    
    r2 = requests.post(pin_url, headers=headers, json=pin_payload)
    
    if r2.status_code in [200, 201]:
        print(f"✅ Пин опубликован: {title[:50]}")
        return True
    else:
        print(f"❌ Pin error {r2.status_code}: {r2.text}")
        return False

def main():
    config = load_config()
    
    if not config["access_token"] or not config["board_id"]:
        print("❌ PINTEREST_ACCESS_TOKEN или PINTEREST_BOARD_ID не настроены!")
        sys.exit(1)
    
    news_title = fetch_top_news()
    print(f"📌 Публикуем пин: {news_title}")
    
    # Генерируем изображение
    image_buffer = create_pin_image(news_title)
    
    # Сохраняем локально (для деплоя на сайт как OG image)
    with open("og-image.jpg", "wb") as f:
        f.write(image_buffer.read())
    image_buffer.seek(0)
    
    # Публикуем в Pinterest
    success = upload_to_pinterest(
        config, 
        image_buffer, 
        news_title,
        config["site_url"]
    )
    
    print(f"Готово: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    main()
