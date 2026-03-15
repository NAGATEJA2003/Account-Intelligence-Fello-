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