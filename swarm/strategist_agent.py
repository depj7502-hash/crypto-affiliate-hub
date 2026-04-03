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
        
        HISTORICAL PERFORMANCE & ANALYTICS:
        {performance_logs}
        
        You are not just a strategist; you are a ruthless A/B Tester and Optimizer. 
        Analyze the past performance metrics (views, clicks, engagement). If a specific hashtag, hook style, or topic failed previously, explicitly ban it. If something worked, order them to scale it.
        
        Respond ONLY with a JSON object in this format:
        {{
            "analysis_of_past_data": "What worked, what failed, and why.",
            "meta_strategy": "The overarching theme for today based on data...",
            "directive_for_community_agent": "Focus on these exact subreddits, use these specific dynamic hashtags, write in this specific evolving tone...",
            "directive_for_visual_agent": "Use this specific hook format, optimize title around these SEO keywords, avoid these past mistakes..."
        }}
        """
        response_str = self.think(prompt, json_mode=True)
        return json.loads(response_str)
