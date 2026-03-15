import os
import sys
import time
import json
import traceback
from datetime import datetime
from generate_signals import generate_random_traffic
from research_agent import get_account_intel
from push_to_salesforce import push_intelligence_to_sf
from fello_logger import get_logger

# Get the directory of this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'data')

log = get_logger("Master")

# --- CONFIGURATION ---
THROTTLE_DELAY = int(os.environ.get('THROTTLE_DELAY', '1'))  # Seconds to wait between AI calls
TOTAL_RECORDS = int(os.environ.get('TOTAL_RECORDS', '5'))    # Number of signals to generate
DRY_RUN = os.environ.get('DRY_RUN', 'false').lower() == 'true'

class PipelineError(Exception):
    """Custom exception for pipeline errors"""
    pass

def verify_environment():
    """Verify that required environment variables are set"""
    log.info("🔍 Verifying environment configuration...")

    required_vars = {
        'GROQ_API_KEY': 'Groq API key',
        'SF_USERNAME': 'Salesforce username',
        'SF_PASSWORD': 'Salesforce password',
        'SF_TOKEN': 'Salesforce security token'
    }

    missing = []
    for var, description in required_vars.items():
        if not os.environ.get(var):
            missing.append(description)
            log.error(f"❌ Missing environment variable: {var} ({description})")

    if missing:
        raise PipelineError(f"Missing required configuration: {', '.join(missing)}")

    log.info("✅ All required environment variables are configured")

def verify_data_directory():
    """Ensure data directory exists"""
    os.makedirs(DATA_DIR, exist_ok=True)
    log.info(f"✅ Data directory ready: {DATA_DIR}")

def generate_signals():
    """Step 1: Generate raw traffic signals"""
    log.info(f"\n{'='*50}")
    log.info("STEP 1: Generating Raw Traffic Signals")
    log.info(f"{'='*50}")

    try:
        generate_random_traffic(TOTAL_RECORDS)
        log.info(f"✅ Generated {TOTAL_RECORDS} visitor signals")
    except Exception as e:
        raise PipelineError(f"Failed to generate signals: {e}")

def load_signals():
    """Step 2: Load signals from disk"""
    log.info(f"\n{'='*50}")
    log.info("STEP 2: Loading Signals from Disk")
    log.info(f"{'='*50}")

    signals_path = os.path.join(DATA_DIR, 'visitor_signals.json')

    if not os.path.exists(signals_path):
        raise PipelineError(f"Signals file not found: {signals_path}")

    try:
        with open(signals_path, 'r') as f:
            visitors = json.load(f)
        log.info(f"✅ Loaded {len(visitors)} raw signals")
        return visitors
    except json.JSONDecodeError as e:
        raise PipelineError(f"Invalid JSON in signals file: {e}")
    except Exception as e:
        raise PipelineError(f"Failed to load signals: {e}")

def enrich_with_ai(visitors):
    """Step 3: Enrich signals with AI research"""
    log.info(f"\n{'='*50}")
    log.info("STEP 3: AI Enrichment")
    log.info(f"{'='*50}")
    log.info(f"Processing {len(visitors)} companies with {THROTTLE_DELAY}s throttling...")

    master_intelligence = []
    successes = 0
    failures = 0

    for index, v in enumerate(visitors, start=1):
        company_name = v.get('company', 'Unknown')
        progress = f"[{index}/{len(visitors)}]"

        try:
            log.info(f"{progress} 🔍 Researching: {company_name}")

            # Get AI intelligence
            intel = get_account_intel(company_name, v['pages_visited'])

            # Merge data
            intel['company'] = company_name
            intel['pages_visited'] = v.get('pages_visited', [])
            intel['time_on_site'] = v.get('time_on_site', '1m')

            master_intelligence.append(intel)
            successes += 1
            log.info(f"{progress} ✅ Successfully enriched {company_name}")

            # Throttle to respect API limits
            if index < len(visitors):
                log.debug(f"{progress} ⏳ Cooling down for {THROTTLE_DELAY}s...")
                time.sleep(THROTTLE_DELAY)

        except ValueError as e:
            failures += 1
            log.error(f"{progress} ❌ Configuration error for {company_name}: {e}")
            raise  # Re-raise configuration errors immediately
        except Exception as e:
            failures += 1
            log.error(f"{progress} ⚠️ Skipping {company_name} due to error: {e}")
            log.debug(traceback.format_exc())
            # Extra delay on error
            time.sleep(5)

    log.info(f"\n📊 AI Enrichment Summary:")
    log.info(f"  ✅ Successful: {successes}")
    log.info(f"  ❌ Failed: {failures}")
    log.info(f"  📦 Total records: {len(master_intelligence)}")

    if len(master_intelligence) == 0:
        raise PipelineError("No records were successfully enriched")

    return master_intelligence

def save_intelligence(master_intelligence):
    """Step 4: Save master intelligence file"""
    log.info(f"\n{'='*50}")
    log.info("STEP 4: Saving Master Intelligence")
    log.info(f"{'='*50}")

    master_path = os.path.join(DATA_DIR, 'master_intelligence.json')

    try:
        with open(master_path, 'w', encoding='utf-8') as f:
            json.dump(master_intelligence, f, indent=4, ensure_ascii=False)
        log.info(f"✅ Saved {len(master_intelligence)} records to {master_path}")
    except Exception as e:
        raise PipelineError(f"Failed to save master intelligence: {e}")

def sync_to_salesforce():
    """Step 5: Sync to Salesforce"""
    if DRY_RUN:
        log.info(f"\n{'='*50}")
        log.info("STEP 5: Salesforce Sync (SKIPPED - Dry Run)")
        log.info(f"{'='*50}")
        log.info("⚠️ DRY_RUN enabled - skipping Salesforce sync")
        return

    log.info(f"\n{'='*50}")
    log.info("STEP 5: Salesforce Sync")
    log.info(f"{'='*50}")

    try:
        push_intelligence_to_sf()
        log.info("✅ Salesforce sync completed")
    except Exception as e:
        raise PipelineError(f"Salesforce sync failed: {e}")

def print_summary(start_time, records_processed):
    """Print execution summary"""
    duration = datetime.now() - start_time

    log.info(f"\n{'='*50}")
    log.info("📊 PIPELINE EXECUTION SUMMARY")
    log.info(f"{'='*50}")
    log.info(f"⏱️  Duration: {duration}")
    log.info(f"📦 Records processed: {records_processed}")
    log.info(f"🔧 Dry Run: {DRY_RUN}")
    log.info(f"✅ Status: COMPLETED SUCCESSFULLY")
    log.info(f"{'='*50}")

def run():
    """Main pipeline entry point"""
    start_time = datetime.now()

    log.info("\n" + "="*50)
    log.info("  🚀 FELLO ACCOUNT INTELLIGENCE SYNC PIPELINE")
    log.info("="*50)
    log.info(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")

    try:
        # Pre-flight checks
        verify_environment()
        verify_data_directory()

        # Pipeline steps
        generate_signals()
        visitors = load_signals()
        master_intelligence = enrich_with_ai(visitors)
        save_intelligence(master_intelligence)
        sync_to_salesforce()

        # Success summary
        print_summary(start_time, len(master_intelligence))

    except PipelineError as e:
        log.error(f"\n❌ PIPELINE ERROR: {e}")
        log.error(traceback.format_exc())
        sys.exit(1)
    except KeyboardInterrupt:
        log.warning("\n⚠️ Pipeline interrupted by user")
        sys.exit(130)
    except Exception as e:
        log.error(f"\n❌ UNEXPECTED ERROR: {e}")
        log.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    run()
