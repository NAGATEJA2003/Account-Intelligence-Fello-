import os
import json
from groq import Groq

def get_account_intel(company_name, pages):
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        raise ValueError('GROQ_API_KEY environment variable not set')

    # Default model settings (can be overridden with config.json in future)
    model = os.environ.get('GROQ_MODEL', 'llama-3.3-70b-versatile')

    client = Groq(api_key=api_key)
    
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
        model=model,
        response_format={"type": "json_object"}
    )
    return json.loads(chat.choices[0].message.content)