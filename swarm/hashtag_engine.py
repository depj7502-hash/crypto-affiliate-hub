from core import Agent
import json

class HashtagEngine(Agent):
    """
    Shared utility used by ALL agents.
    Generates platform-optimized hashtags, titles, and descriptions.
    It learns from historical performance: if a hashtag previously generated
    high engagement, it gets a higher weight. If it flopped, it gets dropped.
    """
    def __init__(self):
        super().__init__(
            name="HashtagEngine",
            role="You are an elite SEO and hashtag optimization specialist with deep knowledge of cryptography, finance, and viral social media mechanics. You constantly iterate and improve metadata.",
            model="llama3-70b-8192"
        )

    def generate(self, platform: str, topic: str, affiliate_link: str, performance_history: list) -> dict:
        """
        Generate optimized hashtags, title, and description for a given platform and topic.
        Uses historical performance to continuously improve.
        """
        past_data_str = json.dumps(performance_history[-3:]) if performance_history else "No history yet. Experiment freely."

        prompt = f"""
        PLATFORM: {platform}
        TOPIC: {topic}
        AFFILIATE LINK: {affiliate_link}
        
        PREVIOUS PERFORMANCE LOG (Analyze what worked and what failed):
        {past_data_str}
        
        Generate highly optimized metadata for this piece of content.
        Rules:
        - Twitter/X: Max 3 hashtags. Make them trending, not generic.
        - YouTube/TikTok: 10-15 hashtags. Mix broad (#crypto) with niche (#btcanalysis2025).
        - Reddit: NO hashtags. Focus on a killer clickbait title that sounds organic.
        - Pinterest: 10+ descriptive hashtags.
        - Instagram: 15-20 hashtags, mix viral and niche.
        - Always embed the affiliate_link naturally in the description CTA.
        - If past data shows certain hashtags failed (low engagement), REPLACE them.
        - If past data shows certain hooks worked, EVOLVE and IMPROVE them.
        
        Respond ONLY with a JSON object:
        {{
            "title": "Optimized, SEO-rich title",
            "description": "Engaging description ending with CTA and affiliate link",
            "hashtags": ["#hash1", "#hash2", ...],
            "improvement_note": "What you changed from last time and why"
        }}
        """
        result_str = self.think(prompt, json_mode=True)
        return json.loads(result_str)
