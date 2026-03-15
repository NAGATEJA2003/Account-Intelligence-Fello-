# FELLO ACCOUNT INTELLIGENCE ENGINE - ARCHITECTURE EXPORT

## 1. Project Overview
- **Goal**: Bridge anonymous web traffic signals with Salesforce CRM using AI.
- **Live URL**: https://ddl00000iwng4uaj-dev-ed.develop.my.site.com/AccountIntellgence

## 2. Python Backend (The "Brain")
- **File**: research_agent.py (Handles Groq/Gemini AI research)
- **File**: auto_sync.py (The main loop & signal processor)
- **File**: push_to_salesforce.py (The REST API integration)
import json, random, os
from datetime import datetime

def generate_random_traffic(count=5):
    if not os.path.exists('config.json'): return
    with open('config.json', 'r') as f: config = json.load(f)
    
    urls, ips = config['url_pool'], config['ip_pool']
    signals = []
    
    for i in range(count):
        visitor = random.choice(ips)
        # 50% chance of only 1 page (Low Intent), 30% Mid, 20% High
        num_pages = random.choices([1, 3, 6], weights=[50, 30, 20])[0]
        
        if num_pages == 1:
            visited = [random.choice(["/home", "/blog/post-1", "/careers"])]
        else:
            visited = random.sample(urls, k=min(num_pages, len(urls)))

        signals.append({
            "id": f"V-{1000 + i}",
            "company": visitor['name'],
            "website": visitor.get('domain', 'N/A'),
            "pages_visited": visited,
            "time_on_site": f"{random.randint(0, 10)}m",
            "timestamp": datetime.now().strftime("%b %d, %H:%M")
        })
    
    with open('visitor_signals.json', 'w') as f: json.dump(signals, f, indent=4)
    print(f"✅ Generated {count} signals with varied intent.")

if __name__ == "__main__": generate_random_traffic()

import json
from groq import Groq

def get_account_intel(company_name, pages):
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    client = Groq(api_key=config['api_settings']['api_key'])
    
    # Precise rubric to prevent "Always 8" syndrome
    prompt = f"""
    Analyze {company_name} based on visits to: {', '.join(pages)}.
    
    SCORING RUBRIC (Strict):
    - 10: Visited BOTH /pricing AND /demo-request.
    - 7-9: Visited /docs or multiple /case-studies.
    - 4-6: Visited /about-us or 2+ /blog posts.
    - 1-3: Only 1 /blog post or just /home.

    Return ONLY a JSON object:
    {{
        "industry": "string", "company_size": "string", "hq": "string", 
        "website": "string", "persona_inference": "string",
        "intent_score": (int 1-10), "intent_stage": "string",
        "confidence_score": (int 1-100),
        "ai_summary": "2 sentences", "sales_action": "1 specific step",
        "tech_stack": "list", "leadership": "names", 
        "business_signals": "news", "sales_hook": "one-liner",
        "key_signals_observed": "summary of behavior"
    }}
    """

    chat = client.chat.completions.create(
        messages=[{"role": "system", "content": "You are a Revenue Analyst. Return ONLY JSON."},
                  {"role": "user", "content": prompt}],
        model=config['api_settings']['model'],
        response_format={"type": "json_object"}
    )
    return json.loads(chat.choices[0].message.content)

## 3. Salesforce Apex (The "Bridge")
- **File**: AccountIntelligenceController.cls
[PASTE YOUR APEX CODE HERE - Ensure it says 'without sharing']

## 4. LWC Frontend (The "Face")
- **File**: account_Intelligence.js
- **File**: account_Intelligence.html
- **File**: account_Intelligence.js-meta.xml
[PASTE ALL LWC CODE HERE]