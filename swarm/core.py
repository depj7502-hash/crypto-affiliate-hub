import os
import json
from groq import Groq

def get_groq_client():
    # Fallback to local config if not in Actions
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        config_path = "../config.json"
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                c = json.load(f)
                key = c.get("groq_api_key")
    if not key:
        raise ValueError("GROQ_API_KEY is not set.")
    return Groq(api_key=key)

class Agent:
    def __init__(self, name, role, model="llama3-70b-8192"):
        self.name = name
        self.role = role
        self.model = model
        self.client = get_groq_client()

    def think(self, prompt, context="", json_mode=False):
        sys_prompt = f"You are {self.name}. Your role is: {self.role}."
        if context:
            sys_prompt += f"\nContext/Memory: {context}"
            
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ]
        
        args = {
            "messages": messages,
            "model": self.model,
            "temperature": 0.7
        }
        if json_mode:
            args["response_format"] = {"type": "json_object"}
            
        response = self.client.chat.completions.create(**args)
        return response.choices[0].message.content
