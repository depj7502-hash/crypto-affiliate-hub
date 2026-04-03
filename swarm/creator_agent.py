from core import Agent
import json

class CreatorAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Creator", 
            role="Top-tier digital creative director. You take raw market briefs and turn them into highly viral Twitter (X) threads and short-form video scripts.",
            model="llama3-70b-8192"
        )
        
    def generate_content(self, brief_json):
        prompt = f"""
        Here is the research brief from the Oracle:
        {brief_json}
        
        Generate the following for the most viral angle:
        1. A viral Twitter thread (max 2 tweets format) that creates urgency. Include a CTA pointing to a crypto exchange.
        2. A 15-second YouTube Shorts/Reels script (Wait for it... hook, value drop, call to action).
        
        Return ONLY valid JSON with this structure:
        {{
            "twitter_post": "...",
            "video_script": "..."
        }}
        """
        
        return self.think(prompt, json_mode=True)
