from core import Agent
import requests
import xml.etree.ElementTree as ET

class OracleAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Oracle", 
            role="World-class crypto researcher and trend spotter. You analyze market news and output a JSON array of the top 3 most viral narrative angles to exploit today.",
            model="llama3-70b-8192"
        )
        
    def gather_data(self):
        sources = ["https://cointelegraph.com/rss", "https://www.coindesk.com/arc/outboundfeeds/rss/"]
        raw_news = []
        for url in sources:
            try:
                r = requests.get(url, timeout=10)
                root = ET.fromstring(r.content)
                for item in root.findall('.//item')[:3]:
                    title = item.find('title').text.strip()
                    raw_news.append(title)
            except:
                pass
        
        market_context = "\n".join(raw_news)
        
        prompt = f"""
        Here is the raw news for today:
        {market_context}
        
        Based on this, what are the top 3 narratives that will generate the most FOMO/engagement on specific platforms like Twitter and TikTok?
        Return ONLY valid JSON with this structure:
        {{
            "briefs": [
                {{"angle": "Description of the angle", "target_audience": "e.g. Degen traders, Beginners", "fomo_trigger": "What makes them click"}}
            ]
        }}
        """
        
        return self.think(prompt, json_mode=True)
