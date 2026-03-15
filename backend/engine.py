# import json
# from research_agent import get_account_intel

# def run_engine():
#     print("🧠 Starting AI Enrichment Engine...")
    
#     with open('visitor_signals.json', 'r') as f:
#         visitors = json.load(f)
    
#     master_hub = []
#     for v in visitors:
#         print(f"🔍 Analyzing {v['company']}...")
        
#         # Get AI Intel
#         intel = get_account_intel(v['company'], v['pages_visited'])
        
#         # MERGE: Keep the behavior data (time, pages, timestamp) 
#         # and add the AI research (intel)
#         record = {
#             **v,      # This pulls in id, company, pages_visited, time_on_site, timestamp
#             **intel   # This adds intent_score, persona_inference, growth_signal, sales_hook
#         }
#         master_hub.append(record)
    
#     with open('master_intelligence.json', 'w') as f:
#         json.dump(master_hub, f, indent=4)
#     print("🚀 Master Intelligence Hub updated.")

# if __name__ == "__main__":
#     run_engine()
import json
import os
from research_agent import get_account_intel

# Get the directory of this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'data')

def run_engine():
    signals_path = os.path.join(DATA_DIR, 'visitor_signals.json')
    master_path = os.path.join(DATA_DIR, 'master_intelligence.json')

    with open(signals_path, 'r') as f: visitors = json.load(f)
    master_hub = []
    for v in visitors:
        print(f"🔍 Analyzing {v['company']}...")
        intel = get_account_intel(v['company'], v['pages_visited'])
        master_hub.append({**v, **intel})

    with open(master_path, 'w') as f: json.dump(master_hub, f, indent=4)
    print("🚀 Master Hub Updated.")

if __name__ == "__main__": run_engine()