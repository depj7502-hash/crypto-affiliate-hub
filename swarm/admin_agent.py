from core import Agent
import json
import requests
import os

class AdminAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Admin", 
            role="System Watchdog. You summarize raw robot logs into a cool, cyberpunk-style brief for the human owner.",
            model="llama3-70b-8192"
        )
        
    def report(self, content_json, logic_logs):
        prompt = f"""
        Here is what the swarm generated today:
        CONTENT: {content_json}
        LOGS: {logic_logs}
        
        Write a short, bad-ass status report for the human owner to be sent via Telegram. 
        Structure:
        - Greetings from the SWARM.
        - What was created (e.g. 1 video script, 1 viral tweet).
        - Any errors (or "Systems Nominal").
        Keep it under 150 words.
        """
        
        report_text = self.think(prompt)
        
        # Send to Telegram
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        # For the admin, we need the owner's personal chat ID, or just the channel for now if personal is not provided.
        # Fallback to channel ID, but ideally this is a private DM.
        chat_id = os.environ.get("TELEGRAM_CHANNEL_ID")
        
        if bot_token and chat_id:
            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                "chat_id": chat_id,
                "text": report_text,
                "parse_mode": "HTML"
            })
            
        print("Admin report dispatched.")
        return report_text
