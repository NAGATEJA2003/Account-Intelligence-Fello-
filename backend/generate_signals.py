import json, random, os
from datetime import datetime

# Get the directory of this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'data')

def generate_random_traffic(count=5):
    config_path = os.path.join(SCRIPT_DIR, 'config.json')
    if not os.path.exists(config_path): return
    with open(config_path, 'r') as f: config = json.load(f)
    
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
    
    signals_path = os.path.join(DATA_DIR, 'visitor_signals.json')
    with open(signals_path, 'w') as f: json.dump(signals, f, indent=4)
    print(f"Generated {count} signals with varied intent.")

if __name__ == "__main__": generate_random_traffic()