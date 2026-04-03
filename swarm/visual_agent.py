from core import Agent
import json
import os

class VisualAgent(Agent):
    def __init__(self):
        super().__init__(
            name="VisualAgent",
            role="You are an elite Video Director and Editor. You specialize in YouTube Shorts, TikTok, and Instagram Reels.",
            model="llama3-70b-8192"
        )
        self.load_skills()

    def load_skills(self):
        skills_dir = os.path.join(os.path.dirname(__file__), "skills")
        try:
            with open(os.path.join(skills_dir, "tiktok_youtube_retention.md"), "r", encoding="utf-8") as f:
                self.video_skill = f.read()
        except:
            self.video_skill = ""

    def generate_and_publish(self, context, strategy_brief):
        print(f"[{self.name}] Conceptualizing Video and Auto-Publishing to TikTok & YouTube...")
        
        prompt = f"""
        OVERLORD INSTRUCTIONS: {strategy_brief}
        MARKET DATA: {context}
        
        --- SHORT FORM VIDEO ALGORITHM KNOWLEDGE BASE ---
        {self.video_skill}
        
        Generate a video script and editing timeline based on the knowledge base.
        Respond ONLY with a JSON object in this format:
        {{
            "title": "SEO Optimized Title #Shorts",
            "description": "Engaging description with affiliate CTA",
            "tags": ["crypto", "btc", ...],
            "script": [
                {{"time": "0:00-0:03", "visual": "Exploding chart...", "audio": "Stop doing this..."}},
                {{"time": "0:03-0:05", "visual": "...", "audio": "..."}}
            ]
        }}
        """
        response_text = self.think(prompt, json_mode=True)
        content = json.loads(response_text)
        
        # Publish
        self._publish_tiktok(content)
        self._publish_youtube(content)
        
        return content

    def _publish_tiktok(self, video_data):
        print(f"[{self.name}] [PLAYWRIGHT ENGINE] Uploading rendered video to TikTok (Headless Mode)...")

    def _publish_youtube(self, video_data):
        print(f"[{self.name}] [PLAYWRIGHT ENGINE] Uploading rendered video to YouTube Shorts (Headless Mode)...")
