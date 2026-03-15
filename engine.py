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
from research_agent import get_account_intel

def run_engine():
    with open('visitor_signals.json', 'r') as f: visitors = json.load(f)
    master_hub = []
    for v in visitors:
        print(f"🔍 Analyzing {v['company']}...")
        intel = get_account_intel(v['company'], v['pages_visited'])
        master_hub.append({**v, **intel})
    
    with open('master_intelligence.json', 'w') as f: json.dump(master_hub, f, indent=4)
    print("🚀 Master Hub Updated.")

if __name__ == "__main__": run_engine()