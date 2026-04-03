import os
import json
from oracle_agent import OracleAgent
from creator_agent import CreatorAgent
from strategist_agent import StrategistAgent
from admin_agent import AdminAgent
from memory import SwarmMemory

def run_swarm():
    print("Initializing Swarm...")
    memory = SwarmMemory()
    logs = []
    
    try:
        # Phase 1: Strategist feedback
        strat = StrategistAgent()
        directive = strat.analyze(memory.get_data().get("performance_logs", []))
        print(f"Strat Directive: {directive}")
        logs.append(f"Strategist Directive: {directive}")
        
        # Phase 2: Oracle research
        oracle = OracleAgent()
        brief_str = oracle.gather_data()
        brief = json.loads(brief_str)
        memory.update_research(brief)
        print("Oracle gathered intel.")
        logs.append("Oracle gathered intel successfully.")
        
        # Phase 3: Creator generation
        creator = CreatorAgent()
        # Inject strategist directive into brief
        brief["directive"] = directive
        content_str = creator.generate_content(json.dumps(brief))
        content = json.loads(content_str)
        memory.add_content(content)
        print("Creator generated content.")
        logs.append("Creator generated thread and video scripts.")
        
        # Save output for other scripts (e.g. video_generator.py to use)
        with open("daily_content.json", "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=4)
            
        success = True
    except Exception as e:
        print(f"Swarm Error: {e}")
        logs.append(f"ERROR: {str(e)}")
        success = False
        content_str = "{}"
        
    # Phase 4: Admin reporting
    admin = AdminAgent()
    admin.report(content_str, logs)
    
    if success:
        memory.log_performance({"date": memory.get_data()["last_run"], "status": "success", "items_created": 2})

if __name__ == "__main__":
    run_swarm()
