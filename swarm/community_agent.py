from core import Agent
import json
import os

class CommunityAgent(Agent):
    def __init__(self):
        super().__init__(
            name="CommunityAgent",
            role="You are the ultimate text-based community builder and marketer for Twitter (X.com) and Reddit.",
            model="llama3-70b-8192"
        )
        self.load_skills()

    def load_skills(self):
        skills_dir = os.path.join(os.path.dirname(__file__), "skills")
        try:
            with open(os.path.join(skills_dir, "twitter_algo.md"), "r", encoding="utf-8") as f:
                self.twitter_skill = f.read()
            with open(os.path.join(skills_dir, "reddit_marketing.md"), "r", encoding="utf-8") as f:
                self.reddit_skill = f.read()
        except:
            self.twitter_skill = ""
            self.reddit_skill = ""

    def generate_and_publish(self, context, strategy_brief):
        print(f"[{self.name}] Generating and Auto-Publishing to Twitter & Reddit...")
        
        prompt = f"""
        OVERLORD INSTRUCTIONS: {strategy_brief}
        MARKET DATA: {context}
        
        --- TWITTER KNOWLEDGE BASE ---
        {self.twitter_skill}
        
        --- REDDIT KNOWLEDGE BASE ---
        {self.reddit_skill}
        
        Generate the content AND provide the publishing instructions based on your knowledge base.
        Respond ONLY with a JSON object in this format:
        {{
            "twitter_thread": ["tweet 1", "tweet 2", "tweet CTA..."],
            "reddit_post": {{"title": "hook title", "body": "full text with soft CTA", "subreddit": "r/chosen_subreddit"}}
        }}
        """
        response_text = self.think(prompt, json_mode=True)
        content = json.loads(response_text)
        
        # Publish
        self._publish_twitter(content.get("twitter_thread", []))
        self._publish_reddit(content.get("reddit_post", {}))
        
        return content

    def _publish_twitter(self, thread_array):
        # Placeholder for Playwright automation using headless browser
        print(f"[{self.name}] [PLAYWRIGHT ENGINE] Posting {len(thread_array)} tweets to Twitter Account...")
        
    def _publish_reddit(self, post_data):
        # Placeholder for Playwright automation using headless browser
        subreddit = post_data.get("subreddit", "r/CryptoCurrency")
        print(f"[{self.name}] [PLAYWRIGHT ENGINE] Navigating to {subreddit} and posting stealth thread...")

