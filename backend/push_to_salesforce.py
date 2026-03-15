import json, os, re
from datetime import datetime, timezone
from dotenv import load_dotenv
from simple_salesforce import Salesforce
from fello_logger import get_logger

# Get the directory of this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'data')

load_dotenv()
logger = get_logger("SalesforceSync")

def parse_to_seconds(time_str):
    if not time_str: return 60
    minutes = re.findall(r'(\d+)m', str(time_str))
    seconds = re.findall(r'(\d+)s', str(time_str))
    return (int(minutes[0]) * 60 if minutes else 0) + (int(seconds[0]) if seconds else 0)

def push_intelligence_to_sf():
    try:
        sf = Salesforce(
            username=os.getenv('SF_USERNAME'), 
            password=os.getenv('SF_PASSWORD'), 
            security_token=os.getenv('SF_TOKEN')
        )
        
        master_path = os.path.join(DATA_DIR, 'master_intelligence.json')
        with open(master_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        logger.info(f"Syncing {len(data)} records with Stateful Re-evaluation...")

        for item in data:
            try:
                domain = item.get('website', 'N/A')
                
                # 1. RETRIEVE PREVIOUS CONTEXT
                # We pull the old summary and score to provide context for the revised diagnosis
                query = f"""
                    SELECT Id, Total_Visits__c, Intent_Score__c, AI_Summary__c, Intent_Stage__c 
                    FROM Visitor_Intelligence__c 
                    WHERE Domain__c = '{domain}' 
                    LIMIT 1
                """
                existing_records = sf.query(query)['records']

                # Base payload from the CURRENT visit
                record_payload = {
                    'Company_Name__c': item.get('company', 'Unknown Company'),
                    'Domain__c': domain,
                    'Industry__c': item.get('industry', 'General Business'),
                    'Company_Size__c': str(item.get('company_size', 'Mid-Market')),
                    'HQ_Location__c': item.get('hq', 'Global/Remote'),
                    'Leadership__c': ", ".join(item.get('leadership', [])) if item.get('leadership') else "Executive Team",
                    'Tech_Stack__c': ", ".join(item.get('tech_stack', [])) if item.get('tech_stack') else "Standard Tech Stack",
                    'Intent_Score__c': item.get('intent_score', 0),
                    'Confidence_Score__c': item.get('confidence_score', 0),
                    'Intent_Stage__c': item.get('intent_stage', 'Awareness'),
                    'Persona__c': item.get('persona_inference', 'Interested Visitor'),
                    'Key_Signals__c': item.get('key_signals_observed', 'General Website Traffic'),
                    'AI_Summary__c': item.get('ai_summary', 'AI is analyzing...'),
                    'Sales_Action__c': item.get('sales_action', 'Follow up via LinkedIn'),
                    'Sales_Hook__c': item.get('sales_hook', 'Explore our solutions'),
                    'Visit_Duration__c': parse_to_seconds(item.get('time_on_site')),
                    'Visited_At__c': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
                }

                if existing_records:
                    # 2. STATEFUL RE-EVALUATION
                    res = existing_records[0]
                    record_id = res['Id']
                    
                    old_score = res.get('Intent_Score__c', 0)
                    old_summary = res.get('AI_Summary__c', '')
                    new_score = item.get('intent_score', 0)
                    # Instead of just overwriting, we 'stack' the history
                    old_signals = res.get('Key_Signals__c', '')
                    new_signals = item.get('key_signals_observed', '')

                    # We show the rep the history directly in the table/modal
                    record_payload['Key_Signals__c'] = f"{new_signals} (Previously: {old_signals})"
                    
                    # LOGIC: If the new score is higher, we flag this as a 'Heating Up' event
                    # This is where you'd typically pass old_summary to your LLM API
                    revised_summary = f"RE-EVALUATED: {item.get('ai_summary')} (Previously: {old_summary[:60]}...)"
                    
                    record_payload['AI_Summary__c'] = revised_summary
                    record_payload['Total_Visits__c'] = (res.get('Total_Visits__c') or 0) + 1
                    
                    sf.Visitor_Intelligence__c.update(record_id, record_payload)
                    logger.info(f"🔄 Revised Diagnosis for {item.get('company')} (Score: {old_score} -> {new_score})")
                
                else:
                    # 3. FRESH DIAGNOSIS
                    record_payload['Total_Visits__c'] = 1
                    sf.Visitor_Intelligence__c.create(record_payload)
                    logger.info(f"✨ Fresh Diagnosis for {item.get('company')}")

            except Exception as e:
                logger.error(f"Error processing {item.get('company')}: {e}")
        
    except Exception as e:
        logger.error(f"System Failure: {e}")

if __name__ == "__main__":
    push_intelligence_to_sf()