from core import Agent
import json
import os
from hashtag_engine import HashtagEngine

class CommunityAgent(Agent):
    def __init__(self):
        super().__init__(
            name="CommunityAgent",
            role="You are the ultimate text-based community builder and marketer for Twitter (X.com) and Reddit. You craft viral content, grow channels, hunt engagement opportunities, and publish everything yourself.",
            model="llama3-70b-8192"
        )
        self.hashtag_engine = HashtagEngine()
        self.load_skills()

    def load_skills(self):
        skills_dir = os.path.join(os.path.dirname(__file__), "skills")
        try:
            with open(os.path.join(skills_dir, "twitter_algo.md"), "r", encoding="utf-8") as f:
                self.twitter_skill = f.read()
            with open(os.path.join(skills_dir, "reddit_marketing.md"), "r", encoding="utf-8") as f:
                self.reddit_skill = f.read()
        except Exception as e:
            print(f"[CommunityAgent] Skill load warning: {e}")
            self.twitter_skill = ""
            self.reddit_skill = ""

    def generate_and_publish(self, context: str, strategy_brief: str, affiliate_links: dict, performance_history: list) -> dict:
        print(f"[{self.name}] Loading skills and generating text content...")

        # Step 1: Generate core content from LLM
        prompt = f"""
        OVERLORD STRATEGY BRIEF: {strategy_brief}
        MARKET DATA FROM ORACLE: {context}
        
        --- YOUR TWITTER ALGORITHM PLAYBOOK ---
        {self.twitter_skill}
        
        --- YOUR REDDIT STEALTH MARKETING PLAYBOOK ---
        {self.reddit_skill}
        
        Using the playbooks above, generate raw content. Do NOT add hashtags or metadata — the metadata engine handles that separately.
        
        Respond ONLY with a JSON object:
        {{
            "twitter_thread": ["tweet 1 (HOOK)", "tweet 2 (VALUE)", "tweet 3 (DATA)", "tweet 4 (CTA)"],
            "reddit_post_body": "Full markdown body of the Reddit post. Minimum 200 words. No affiliate links in body.",
            "reddit_subreddit": "r/CryptoCurrency",
            "engagement_comments": ["comment 1 for trending posts", "comment 2 for trending posts"]
        }}
        """
        raw_content = json.loads(self.think(prompt, json_mode=True))

        # Step 2: HashtagEngine generates optimized metadata for each platform
        twitter_meta = self.hashtag_engine.generate(
            platform="Twitter/X",
            topic=context[:200],
            affiliate_link=affiliate_links.get("mexc", ""),
            performance_history=performance_history
        )
        reddit_meta = self.hashtag_engine.generate(
            platform="Reddit",
            topic=context[:200],
            affiliate_link=affiliate_links.get("bybit", ""),
            performance_history=performance_history
        )

        # Step 3: Merge and publish
        final = {
            "twitter": {
                "thread": raw_content.get("twitter_thread", []),
                "hashtags": twitter_meta.get("hashtags", []),
                "improvement_note": twitter_meta.get("improvement_note", "")
            },
            "reddit": {
                "title": reddit_meta.get("title", ""),
                "body": raw_content.get("reddit_post_body", ""),
                "subreddit": raw_content.get("reddit_subreddit", "r/CryptoCurrency"),
                "description": reddit_meta.get("description", "")
            },
            "engagement_comments": raw_content.get("engagement_comments", [])
        }

        self._publish_twitter(final["twitter"])
        self._publish_reddit(final["reddit"])
        self._post_engagement_comments(final["engagement_comments"])

        return final

    def _publish_twitter(self, data):
        thread = data.get("thread", [])
        tags = " ".join(data.get("hashtags", []))
        print(f"[{self.name}] [PLAYWRIGHT → Twitter] Posting {len(thread)}-tweet thread with tags: {tags}")
        # Playwright automation: login to x.com with credentials from config -> post thread sequentially

    def _publish_reddit(self, data):
        print(f"[{self.name}] [PLAYWRIGHT → Reddit] Posting stealth thread to {data.get('subreddit')}: '{data.get('title')}'")
        # Playwright automation: login to reddit -> navigate to subreddit -> submit post

    def _post_engagement_comments(self, comments):
        print(f"[{self.name}] [PLAYWRIGHT → Reddit/Twitter] Posting {len(comments)} engagement comments on trending posts...")
        # Playwright automation: search trending crypto posts -> reply with value-add comment
