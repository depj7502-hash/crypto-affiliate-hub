from core import Agent
import json

class OverlordAgent(Agent):
    def __init__(self):
        super().__init__(
            name="OverlordAdmin", 
            role="You are the Overlord Strategist of an autonomous crypto empire. You scan the entire surface of available data and dictate strategy to your sub-agents.",
            model="llama3-70b-8192"
        )
        
    def formulate_strategy(self, oracle_data, performance_logs):
        print("[OVERLORD] Formulating cross-platform meta-strategy...")
        prompt = f"""
        ORACLE MARKET REPORT:
        {oracle_data}
        
        HISTORICAL PERFORMANCE:
        {performance_logs}
        
        Your job is to dictate the exact angle the content team should take today to maximize affiliate signups.
        For example: If Oracle reports a Bitcoin pump, order the Community Agent to hype the rally on Twitter/Reddit, and order the Visual Agent to make an urgent FOMO YouTube Short.
        
        Respond ONLY with a JSON object in this format:
        {{
            "meta_strategy": "The overarching theme for today...",
            "directive_for_community_agent": "Exact instructions on what to write for Twitter and Reddit...",
            "directive_for_visual_agent": "Exact instructions on what to show in the YouTube/TikTok videos..."
        }}
        """
        response_str = self.think(prompt, json_mode=True)
        return json.loads(response_str)
