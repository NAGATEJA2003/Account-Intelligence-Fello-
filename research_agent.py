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