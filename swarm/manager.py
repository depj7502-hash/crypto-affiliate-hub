import json
import traceback
from oracle_agent import OracleAgent
from strategist_agent import OverlordAgent
from community_agent import CommunityAgent
from visual_agent import VisualAgent
from admin_agent import AdminAgent
from memory import SwarmMemory

# === LOAD AFFILIATE LINKS FROM CONFIG ===
def load_affiliate_links():
    try:
        import os
        config_path = os.path.join(os.path.dirname(__file__), "../config.json")
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        return cfg.get("affiliate_links", {})
    except:
        return {}

def run_swarm():
    logs = []
    success = False

    try:
        print("╔══════════════════════════════════╗")
        print("║  🧠  SWARM V5.1  INITIALIZING...  ║")
        print("╚══════════════════════════════════╝")

        memory = SwarmMemory()
        history = memory.load()
        performance_logs = history.get("performance_logs", [])
        affiliate_links = load_affiliate_links()

        # ─────────────────────────────────────
        # PHASE 1: ORACLE — Market Intelligence
        # ─────────────────────────────────────
        print("\n[PHASE 1] Oracle scanning market...")
        oracle = OracleAgent()
        market_data = oracle.gather_intelligence()
        logs.append(f"Oracle gathered data: {market_data[:80]}...")

        # ─────────────────────────────────────
        # PHASE 2: OVERLORD — Cross-Platform Strategy + Analytics
        # ─────────────────────────────────────
        print("\n[PHASE 2] Overlord analyzing data and setting strategy...")
        overlord = OverlordAgent()
        strategy = overlord.formulate_strategy(market_data, performance_logs)
        logs.append(f"Overlord strategy: {strategy.get('meta_strategy','')[:100]}")
        logs.append(f"Overlord analysis: {strategy.get('analysis_of_past_data','')[:100]}")

        # ─────────────────────────────────────
        # PHASE 3A: COMMUNITY AGENT — Text + Hashtags → Twitter & Reddit
        # ─────────────────────────────────────
        print("\n[PHASE 3A] Community Agent generating text + hashtags → Twitter & Reddit...")
        community = CommunityAgent()
        community_content = community.generate_and_publish(
            context=market_data,
            strategy_brief=strategy.get("directive_for_community_agent", ""),
            affiliate_links=affiliate_links,
            performance_history=performance_logs
        )
        logs.append(f"Community Agent published thread + Reddit post. Improvement: {community_content['twitter'].get('improvement_note','')[:60]}")

        # ─────────────────────────────────────
        # PHASE 3B: VISUAL AGENT — Video Script + Hashtags → YT/TikTok/IG
        # ─────────────────────────────────────
        print("\n[PHASE 3B] Visual Agent generating video + hashtags → YouTube, TikTok, Instagram...")
        visual = VisualAgent()
        visual_content = visual.generate_and_publish(
            context=market_data,
            strategy_brief=strategy.get("directive_for_visual_agent", ""),
            affiliate_links=affiliate_links,
            performance_history=performance_logs
        )
        logs.append(f"Visual Agent published to YT/TikTok/IG. YT improvement: {visual_content['youtube'].get('improvement_note','')[:60]}")

        # Save full content snapshot
        with open("daily_content.json", "w", encoding="utf-8") as f:
            json.dump({"community": community_content, "visual": visual_content}, f, ensure_ascii=False, indent=4)

        success = True

    except Exception as e:
        print(f"\n[MANAGER] CRITICAL ERROR: {e}")
        print(traceback.format_exc())
        logs.append(f"CRITICAL ERROR: {e}")

    # ─────────────────────────────────────
    # PHASE 4: ADMIN — Telegram Report
    # ─────────────────────────────────────
    print("\n[PHASE 4] Admin sending Telegram report...")
    summary = f"{'✅ SUCCESS' if success else '❌ FAILED'}\n\n" + "\n".join(f"• {l}" for l in logs)
    admin = AdminAgent()
    admin.send_report(f"📊 SWARM V5.1 REPORT:\n{summary}")

    # Update memory with latest run log
    performance_logs.append(summary)
    if len(performance_logs) > 5:
        performance_logs.pop(0)
    history["performance_logs"] = performance_logs
    memory.save(history)

if __name__ == "__main__":
    run_swarm()
