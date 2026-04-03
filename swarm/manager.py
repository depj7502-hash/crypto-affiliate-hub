import json
import traceback
from oracle_agent import OracleAgent
from strategist_agent import OverlordAgent
from community_agent import CommunityAgent
from visual_agent import VisualAgent
from admin_agent import AdminAgent
from memory import SwarmMemory

def run_swarm():
    try:
        print("--- INITIATING SWARM V5 ---")
        logs = []
        memory = SwarmMemory()
        history = memory.load()

        # Phase 1: Oracle Gathering
        oracle = OracleAgent()
        market_data = oracle.gather_intelligence()
        logs.append(f"Oracle data gathered: {market_data[:50]}...")
        
        # Phase 2: Overlord Strategy
        overlord = OverlordAgent()
        strategy = overlord.formulate_strategy(market_data, history.get("performance_logs", []))
        logs.append("Overlord formulated strategy.")
        
        # Phase 3: Specialized Content Generation & Publishing
        # Community (Text) Agent
        community = CommunityAgent()
        community_content = community.generate_and_publish(market_data, strategy.get("directive_for_community_agent", ""))
        logs.append("Community Agent finished Twitter & Reddit operations.")
        
        # Visual (Video) Agent
        visual = VisualAgent()
        visual_content = visual.generate_and_publish(market_data, strategy.get("directive_for_visual_agent", ""))
        logs.append("Visual Agent finished YouTube & TikTok operations.")
        
        # Compile content for record
        combined_content = {
            "community": community_content,
            "visual": visual_content
        }
        
        with open("daily_content.json", "w", encoding="utf-8") as f:
            json.dump(combined_content, f, ensure_ascii=False, indent=4)
            
        success = True
    except Exception as e:
        print(f"Swarm Error: {e}")
        print(traceback.format_exc())
        logs.append(f"CRITICAL ERROR: {e}")
        success = False

    # Phase 4: Admin Reporting
    admin_summary = f"SWARM V5 CYCLE COMPLETED.\nSUCCESS: {success}\nLOGS:\n" + "\n".join(logs)
    admin = AdminAgent()
    admin.send_report(admin_summary)
    
    # Save memory
    history["performance_logs"].append(admin_summary)
    # Keep last 5 logs to not bloat memory
    if len(history["performance_logs"]) > 5:
        history["performance_logs"].pop(0)
    memory.save(history)

if __name__ == "__main__":
    run_swarm()
