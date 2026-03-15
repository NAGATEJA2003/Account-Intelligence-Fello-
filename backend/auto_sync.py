import os
import time
import json
from generate_signals import generate_random_traffic
from research_agent import get_account_intel
from push_to_salesforce import push_intelligence_to_sf
from fello_logger import get_logger

# Get the directory of this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'data')

log = get_logger("Master")

# --- CONFIGURATION ---
THROTTLE_DELAY = 1  # Seconds to wait between AI calls to avoid 429 errors
TOTAL_RECORDS = int(os.environ.get('TOTAL_RECORDS', '5'))  # Number of signals to generate (from env var)

def run():
    log.info("🚀 Launching Fello Sync Pipeline...")

    # 1. Generate Raw Traffic
    generate_random_traffic(TOTAL_RECORDS)

    # 2. Load signals from disk
    signals_path = os.path.join(DATA_DIR, 'visitor_signals.json')
    master_path = os.path.join(DATA_DIR, 'master_intelligence.json')

    if os.path.exists(signals_path):
        with open(signals_path, 'r') as f:
            visitors = json.load(f)
        log.info(f"✅ Loaded {len(visitors)} raw signals from local logs.")
    else:
        log.error("❌ visitor_signals.json missing!")
        return

    # 3. Iterate and Enrich with AI
    master_intelligence = []
    log.info(f"🧠 Starting AI Research Agent (Groq) with {THROTTLE_DELAY}s throttling...")

    for index, v in enumerate(visitors, start=1):
        try:
            name_to_research = v.get('company', 'Unknown')
            # Progress tracking for your screen recording/demo
            print(f"\n[{index}/{len(visitors)}] Researching: {name_to_research}...")

            # 1. Get the AI data (The "Brain" call)
            intel = get_account_intel(name_to_research, v['pages_visited'])

            # 2. Data Formatting & Metric Injection
            intel['company'] = name_to_research
            intel['pages_visited'] = v.get('pages_visited', [])
            intel['time_on_site'] = v.get('time_on_site', '1m')

            master_intelligence.append(intel)

            # 3. THE RATE LIMIT FIX: Dynamic Throttling
            if index < len(visitors):
                log.info(f"⏳ Cooling down for {THROTTLE_DELAY}s to respect Groq API limits...")
                time.sleep(THROTTLE_DELAY)

        except Exception as e:
            log.error(f"⚠️ Skip {v.get('company')} due to error: {e}")
            # Wait a little even on error to let the API breath
            time.sleep(5)

    # 4. Save the Master Intelligence File
    with open(master_path, 'w', encoding='utf-8') as f:
        json.dump(master_intelligence, f, indent=4)
    log.info("💾 master_intelligence.json successfully updated with fresh AI research.")

    # 5. Salesforce Sync Execution
    # Adding a buffer to ensure file I/O is finished
    time.sleep(2)
    if os.path.exists(master_path):
        log.info("☁️ Initiating Stateful Salesforce Sync (Upsert Logic)...")
        push_intelligence_to_sf()
    else:
        log.error("❌ Final sync aborted: Master file was not generated.")

if __name__ == "__main__":
    run()