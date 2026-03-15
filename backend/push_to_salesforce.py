"""
Salesforce Integration Module

Handles syncing account intelligence data to Salesforce
with stateful upsert logic and comprehensive error handling.
"""
import os
import re
import json
import logging
from datetime import datetime, timezone
from dotenv import load_dotenv
from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceError
from .fello_logger import get_logger

# Get the directory of this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'data')

load_dotenv()
logger = get_logger("SalesforceSync")


class SalesforceConnectionError(Exception):
    """Custom exception for Salesforce connection errors"""
    pass


class SalesforceSyncError(Exception):
    """Custom exception for Salesforce sync errors"""
    pass


def verify_salesforce_credentials():
    """
    Verify that Salesforce credentials are configured.

    Raises:
        SalesforceConnectionError: If credentials are missing
    """
    required = ['SF_USERNAME', 'SF_PASSWORD', 'SF_TOKEN']
    missing = [var for var in required if not os.getenv(var)]

    if missing:
        raise SalesforceConnectionError(
            f"Missing Salesforce credentials: {', '.join(missing)}. "
            "Please set these environment variables."
        )

    logger.info("✅ Salesforce credentials configured")


def create_salesforce_connection():
    """
    Create and test a Salesforce connection.

    Returns:
        Salesforce: Authenticated Salesforce client

    Raises:
        SalesforceConnectionError: If connection fails
    """
    verify_salesforce_credentials()

    try:
        sf = Salesforce(
            username=os.getenv('SF_USERNAME'),
            password=os.getenv('SF_PASSWORD'),
            security_token=os.getenv('SF_TOKEN')
        )

        # Test connection by querying API version
        logger.info(f"✅ Connected to Salesforce (API version: {sf.sf_version})")
        return sf

    except SalesforceError as e:
        raise SalesforceConnectionError(f"Salesforce authentication failed: {e}")
    except Exception as e:
        raise SalesforceConnectionError(f"Failed to connect to Salesforce: {e}")


def parse_to_seconds(time_str):
    """
    Convert time string (e.g., '5m', '30s', '5m30s') to seconds.

    Args:
        time_str: Time string to parse

    Returns:
        int: Time in seconds (default 60 if invalid)
    """
    if not time_str:
        return 60

    minutes = re.findall(r'(\d+)m', str(time_str))
    seconds = re.findall(r'(\d+)s', str(time_str))

    return (int(minutes[0]) * 60 if minutes else 0) + (int(seconds[0]) if seconds else 0)


def sanitize_value(value, default=''):
    """
    Sanitize a value for Salesforce.

    Args:
        value: Value to sanitize
        default: Default value if None/empty

    Returns:
        Sanitized value
    """
    if value is None:
        return default
    if isinstance(value, list):
        return ", ".join(str(v) for v in value) if value else default
    return str(value) if value else default


def build_record_payload(item):
    """
    Build a Salesforce record payload from intelligence data.

    Args:
        item: Dictionary containing intelligence data

    Returns:
        dict: Formatted record payload
    """
    return {
        'Company_Name__c': sanitize_value(item.get('company'), 'Unknown Company'),
        'Domain__c': sanitize_value(item.get('website'), 'N/A'),
        'Industry__c': sanitize_value(item.get('industry'), 'General Business'),
        'Company_Size__c': sanitize_value(item.get('company_size'), 'Mid-Market'),
        'HQ_Location__c': sanitize_value(item.get('hq'), 'Global/Remote'),
        'Leadership__c': sanitize_value(item.get('leadership'), 'Executive Team'),
        'Tech_Stack__c': sanitize_value(item.get('tech_stack'), 'Standard Tech Stack'),
        'Intent_Score__c': int(item.get('intent_score', 0)),
        'Confidence_Score__c': int(item.get('confidence_score', 0)),
        'Intent_Stage__c': sanitize_value(item.get('intent_stage'), 'Awareness'),
        'Persona__c': sanitize_value(item.get('persona_inference'), 'Interested Visitor'),
        'Key_Signals__c': sanitize_value(item.get('key_signals_observed'), 'General Website Traffic'),
        'AI_Summary__c': sanitize_value(item.get('ai_summary'), 'AI is analyzing...'),
        'Sales_Action__c': sanitize_value(item.get('sales_action'), 'Follow up via LinkedIn'),
        'Sales_Hook__c': sanitize_value(item.get('sales_hook'), 'Explore our solutions'),
        'Visit_Duration__c': parse_to_seconds(item.get('time_on_site')),
        'Visited_At__c': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    }


def find_existing_record(sf, domain):
    """
    Find an existing record by domain.

    Args:
        sf: Salesforce client
        domain: Domain to search for

    Returns:
        list: List of matching records (empty if none found)

    Raises:
        SalesforceSyncError: If query fails
    """
    # Sanitize domain for SOQL
    if not domain or domain == 'N/A':
        return []

    try:
        # Escape single quotes for SOQL
        safe_domain = domain.replace("'", "''")

        query = f"""
            SELECT Id, Total_Visits__c, Intent_Score__c, AI_Summary__c, Intent_Stage__c, Key_Signals__c
            FROM Visitor_Intelligence__c
            WHERE Domain__c = '{safe_domain}'
            LIMIT 1
        """

        result = sf.query(query)
        return result.get('records', [])

    except SalesforceError as e:
        raise SalesforceSyncError(f"Failed to query existing records: {e}")


def update_existing_record(sf, record_id, payload, company_name, old_record):
    """
    Update an existing Salesforce record.

    Args:
        sf: Salesforce client
        record_id: ID of record to update
        payload: New data payload
        company_name: Company name (for logging)
        old_record: Existing record data

    Returns:
        bool: True if score increased (heating up)
    """
    old_score = old_record.get('Intent_Score__c', 0)
    new_score = payload.get('Intent_Score__c', 0)
    old_summary = old_record.get('AI_Summary__c', '')
    old_signals = old_record.get('Key_Signals__c', '')
    new_signals = payload.get('Key_Signals__c', '')

    # Append history to signals
    payload['Key_Signals__c'] = f"{new_signals} (Previously: {old_signals})"

    # Append history to summary
    payload['AI_Summary__c'] = f"RE-EVALUATED: {payload['AI_Summary__c']} (Previously: {old_summary[:60]}...)"

    # Increment visit count
    payload['Total_Visits__c'] = (old_record.get('Total_Visits__c') or 0) + 1

    # Perform update
    sf.Visitor_Intelligence__c.update(record_id, payload)

    heating_up = new_score > old_score
    status_emoji = "🔥" if heating_up else "🔄"
    logger.info(f"{status_emoji} Updated {company_name} (Score: {old_score} → {new_score}, Visits: {payload['Total_Visits__c']})")

    return heating_up


def create_new_record(sf, payload, company_name):
    """
    Create a new Salesforce record.

    Args:
        sf: Salesforce client
        payload: Record payload
        company_name: Company name (for logging)
    """
    payload['Total_Visits__c'] = 1
    sf.Visitor_Intelligence__c.create(payload)
    logger.info(f"✨ Created new record for {company_name}")


def push_intelligence_to_sf():
    """
    Main function to sync intelligence data to Salesforce.

    Raises:
        SalesforceConnectionError: If connection fails
        SalesforceSyncError: If sync operations fail
    """
    logger.info("\n" + "="*50)
    logger.info("  SALESFORCE SYNC MODULE")
    logger.info("="*50)

    # Load master intelligence data
    master_path = os.path.join(DATA_DIR, 'master_intelligence.json')

    if not os.path.exists(master_path):
        raise SalesforceSyncError(f"Master intelligence file not found: {master_path}")

    with open(master_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    logger.info(f"📦 Loaded {len(data)} records for sync")

    # Create Salesforce connection
    sf = create_salesforce_connection()

    # Sync statistics
    stats = {
        'created': 0,
        'updated': 0,
        'heating_up': 0,
        'failed': 0,
        'errors': []
    }

    logger.info("🔄 Beginning sync operations...")

    for index, item in enumerate(data, start=1):
        company_name = item.get('company', 'Unknown')
        domain = item.get('website', 'N/A')

        try:
            logger.debug(f"[{index}/{len(data)}] Processing {company_name}...")

            # Build payload
            payload = build_record_payload(item)

            # Check for existing record
            existing_records = find_existing_record(sf, domain)

            if existing_records:
                # Update existing
                record_id = existing_records[0]['Id']
                is_heating_up = update_existing_record(sf, record_id, payload, company_name, existing_records[0])
                stats['updated'] += 1
                if is_heating_up:
                    stats['heating_up'] += 1
            else:
                # Create new
                create_new_record(sf, payload, company_name)
                stats['created'] += 1

        except SalesforceError as e:
            stats['failed'] += 1
            error_msg = f"Salesforce API error for {company_name}: {e}"
            logger.error(f"❌ {error_msg}")
            stats['errors'].append(error_msg)

        except Exception as e:
            stats['failed'] += 1
            error_msg = f"Unexpected error for {company_name}: {e}"
            logger.error(f"❌ {error_msg}")
            stats['errors'].append(error_msg)

    # Print summary
    logger.info("\n" + "="*50)
    logger.info("📊 SYNC SUMMARY")
    logger.info("="*50)
    logger.info(f"✅ Created: {stats['created']}")
    logger.info(f"🔄 Updated: {stats['updated']}")
    logger.info(f"🔥 Heating Up: {stats['heating_up']}")
    logger.info(f"❌ Failed: {stats['failed']}")

    if stats['errors']:
        logger.warning(f"\n⚠️ Errors encountered:")
        for error in stats['errors'][:5]:  # Show first 5 errors
            logger.warning(f"  • {error}")
        if len(stats['errors']) > 5:
            logger.warning(f"  ... and {len(stats['errors']) - 5} more")

    logger.info("="*50)

    if stats['failed'] > 0:
        raise SalesforceSyncError(f"Sync completed with {stats['failed']} errors")


if __name__ == "__main__":
    try:
        push_intelligence_to_sf()
    except (SalesforceConnectionError, SalesforceSyncError) as e:
        logger.error(f"❌ Salesforce sync failed: {e}")
        exit(1)
