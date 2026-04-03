from core import Agent
import json

class StrategistAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Strategist", 
            role="Data-driven Growth Hacker. You analyze the system's performance logs and output strict, one-sentence directives to improve the next generation cycle.",
            model="llama3-70b-8192"
        )
        
    def analyze(self, logs):
        if not logs:
            return "Go aggressive on meme coin fomo."
            
        logs_str = json.dumps(logs)
        prompt = f"""
        Here are the past performance logs of the system:
        {logs_str}
        
        Based on this, what is the ONE main directive for the Creator agent today to maximize conversion? Focus on emotion and hooks.
        """
        
        return self.think(prompt)
