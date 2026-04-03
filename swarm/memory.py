import json
import os
from datetime import datetime

class SwarmMemory:
    def __init__(self, filename="memory.json"):
        self.filename = filename
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except:
                    return self._default()
        return self._default()

    def _default(self):
        return {
            "last_run": "",
            "research_brief": "",
            "content_queue": [],
            "performance_logs": []
        }

    def save(self):
        self.data["last_run"] = datetime.now().isoformat()
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def update_research(self, brief):
        self.data["research_brief"] = brief
        self.save()

    def add_content(self, content_dict):
        self.data["content_queue"].append(content_dict)
        self.save()
        
    def log_performance(self, log):
        self.data["performance_logs"].append(log)
        if len(self.data["performance_logs"]) > 30:
            self.data["performance_logs"] = self.data["performance_logs"][-30:] # Keep last 30
        self.save()
        
    def get_data(self):
        return self.data
