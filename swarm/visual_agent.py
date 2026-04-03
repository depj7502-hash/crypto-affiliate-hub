from core import Agent
import json
import os
from hashtag_engine import HashtagEngine

class VisualAgent(Agent):
    def __init__(self):
        super().__init__(
            name="VisualAgent",
            role="You are an elite Video Director, Screenwriter and Uploader for YouTube Shorts, TikTok, and Instagram Reels. You create punchy, high-retention crypto content and publish it yourself.",
            model="llama3-70b-8192"
        )
        self.hashtag_engine = HashtagEngine()
        self.load_skills()

    def load_skills(self):
        skills_dir = os.path.join(os.path.dirname(__file__), "skills")
        try:
            with open(os.path.join(skills_dir, "tiktok_youtube_retention.md"), "r", encoding="utf-8") as f:
                self.video_skill = f.read()
        except Exception as e:
            print(f"[VisualAgent] Skill load warning: {e}")
            self.video_skill = ""

    def generate_and_publish(self, context: str, strategy_brief: str, affiliate_links: dict, performance_history: list) -> dict:
        print(f"[{self.name}] Loading skills and generating video script...")

        # Step 1: Generate raw video script from LLM
        prompt = f"""
        OVERLORD STRATEGY BRIEF: {strategy_brief}
        MARKET DATA FROM ORACLE: {context}
        
        --- YOUR SHORT-FORM VIDEO ALGORITHM PLAYBOOK ---
        {self.video_skill}
        
        Using the retention playbook, create a detailed video script. 
        Do NOT generate hashtags or titles — the metadata engine handles that.
        Focus ONLY on the script timing and visuals.
        
        Respond ONLY with a JSON object:
        {{
            "hook_line": "The first spoken sentence (must create irresistible curiosity in under 4 words)",
            "script": [
                {{"time": "0:00-0:03", "visual": "Pixel art BTC chart exploding up", "audio": "They said BTC was dead..."}},
                {{"time": "0:03-0:08", "visual": "Close-up of liquidation numbers", "audio": "...while $500M in shorts got wiped"}},
                {{"time": "0:08-0:30", "visual": "Clean data visualization, pixel art style", "audio": "Here is exactly what happened and how I traded it"}},
                {{"time": "0:30-0:44", "visual": "CTA screen with link animation", "audio": "I use MEXC for zero-fee trading. Link is below."}}
            ],
            "visual_style": "Pixel Art Cyberpunk | Glitch Effects | Fast Cuts"
        }}
        """
        raw_script = json.loads(self.think(prompt, json_mode=True))

        # Step 2: HashtagEngine generates unique, evolving metadata for EACH platform
        yt_meta = self.hashtag_engine.generate(
            platform="YouTube Shorts",
            topic=context[:200],
            affiliate_link=affiliate_links.get("mexc", ""),
            performance_history=performance_history
        )
        tt_meta = self.hashtag_engine.generate(
            platform="TikTok",
            topic=context[:200],
            affiliate_link=affiliate_links.get("bybit", ""),
            performance_history=performance_history
        )
        ig_meta = self.hashtag_engine.generate(
            platform="Instagram Reels",
            topic=context[:200],
            affiliate_link=affiliate_links.get("binance", ""),
            performance_history=performance_history
        )

        final = {
            "script": raw_script,
            "youtube": {
                "title": yt_meta.get("title", ""),
                "description": yt_meta.get("description", ""),
                "hashtags": yt_meta.get("hashtags", []),
                "improvement_note": yt_meta.get("improvement_note", "")
            },
            "tiktok": {
                "title": tt_meta.get("title", ""),
                "description": tt_meta.get("description", ""),
                "hashtags": tt_meta.get("hashtags", [])
            },
            "instagram": {
                "title": ig_meta.get("title", ""),
                "description": ig_meta.get("description", ""),
                "hashtags": ig_meta.get("hashtags", [])
            }
        }

        # Step 3: Publish to all platforms
        self._publish_youtube(final)
        self._publish_tiktok(final)
        self._publish_instagram(final)

        return final

    def _publish_youtube(self, data):
        title = data["youtube"].get("title", "Crypto Alert")
        tags = ", ".join(data["youtube"].get("hashtags", []))
        print(f"[{self.name}] [PLAYWRIGHT → YouTube] Uploading Short: '{title}' | Tags: {tags[:80]}...")
        # Playwright: login YouTube Studio -> Upload video file -> fill title, desc, tags -> publish

    def _publish_tiktok(self, data):
        title = data["tiktok"].get("title", "Crypto Alert")
        print(f"[{self.name}] [PLAYWRIGHT → TikTok] Uploading: '{title}'...")
        # Playwright: login TikTok Creator Center -> upload -> fill caption with hashtags -> post

    def _publish_instagram(self, data):
        title = data["instagram"].get("title", "Crypto Alert")
        print(f"[{self.name}] [PLAYWRIGHT → Instagram] Uploading Reel: '{title}'...")
        # Playwright: login Instagram -> create reel -> fill caption + hashtags -> publish
