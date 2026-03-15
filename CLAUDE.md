# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Fello Account Intelligence Engine - A Salesforce application that bridges anonymous web traffic signals with Salesforce CRM using AI. The system consists of:
- Python backend for signal generation and AI analysis (Groq/Gemini)
- Salesforce Apex controller for data management
- Lightning Web Component (LWC) frontend dashboard

## Development Commands

### Linting
```bash
npm run lint                    # Lint Aura and LWC JavaScript
npm run prettier                # Format all files
npm run prettier:verify         # Check formatting
```

### Testing
```bash
npm test                        # Run all unit tests
npm run test:unit               # Run LWC Jest tests
npm run test:unit:watch         # Run tests in watch mode
npm run test:unit:coverage      # Run tests with coverage report
```

### Pre-commit Hooks
The project uses husky and lint-staged. Pre-commit hooks automatically:
1. Format files with prettier
2. Lint JavaScript files
3. Run related LWC tests

### Salesforce Deployment
```bash
# Authorize org
sf org login web

# Deploy to org
sf project deploy start

# Deploy specific source
sf project deploy start --source-dir force-app/main/default/lwc/account_Intelligence
```

## Architecture

### LWC Component Structure
Located at `force-app/main/default/lwc/account_Intelligence/`:
- `account_Intelligence.js` - Main component logic with @wire service to Apex
- `account_Intelligence.html` - Template with SLDS styling, modal detail view, and data table
- `account_Intelligence.css` - Component styles
- `__tests__/account_Intelligence.test.js` - Jest tests

### Data Flow
1. LWC calls `IntelligenceController.getSignals()` Apex method via @wire decorator
2. Apex returns `Visitor_Signal__c` records with fields: Company_Name__c, Intent_Score__c, Persona__c, etc.
3. LWC transforms data for display:
   - Real-time time formatting (seconds → months)
   - Confidence score styling
   - Intent score badge classes
4. Top 5 records displayed as banner cards, rest in data table
5. Modal shows detailed firmographics and AI-generated insights

### Key Apex Controller (Expected)
The LWC expects an Apex controller `IntelligenceController` with:
- `@AuraEnabled(cacheable=true) static List<Visitor_Signal__c> getSignals(String sortBy)`
- Should query `Visitor_Signal__c` custom object with fields: Company_Name__c, Domain__c, Industry__c, Company_Size__c, HQ_Location__c, Tech_Stack__c, Leadership__c, Intent_Score__c, Intent_Stage__c, Key_Signals__c, Persona__c, AI_Summary__c, Sales_Action__c, Sales_Hook__c, Total_Visits__c, Confidence_Score__c, Visited_At__c, Visit_Duration__c

### Time Formatting Logic
The component implements sophisticated real-time display:
- < 60s: "JUST NOW"
- < 1h: "Xm ago"
- < 24h: "Xh ago"
- < 30 days: "X days ago"
- < 365 days: "X months ago"
- > 1 year: "Over a year ago"

### CSV Export
The `downloadExcel()` method exports data sanitized for analysis:
- Raw numeric values for confidence, visits, duration
- UTF-8 BOM encoding for Excel compatibility
- Proper CSV escaping for text fields

## Project Configuration

- Source API Version: 66.0
- LWC API Version: 60.0 (in component metadata)
- Package directory: `force-app/main/default`
- Supports: RecordPage, AppPage, HomePage, Community pages

## Python Backend

### Directory Structure
The Python backend is organized in the `backend/` directory:
- `backend/__init__.py` - Module initialization
- `backend/engine.py` - Main AI enrichment orchestrator
- `backend/research_agent.py` - AI research module using Groq API
- `backend/auto_sync.py` - Full sync pipeline controller
- `backend/push_to_salesforce.py` - Salesforce data sync (REST API)
- `backend/clear_sf_data.py` - Salesforce data cleanup utility
- `backend/fello_logger.py` - Logging utility
- `backend/generate_signals.py` - Test data generator
- `backend/config.json` - API settings, URL/IP pools

### Entry Scripts
Convenience scripts at project root for running Python code:
- `run_engine.py` - Run the AI enrichment engine
- `run_sync.py` - Run the full sync pipeline (generate → enrich → sync)
- `run_signals.py` - Generate test visitor signals

Usage:
```bash
python run_engine.py    # AI enrichment only
python run_sync.py      # Full pipeline
python run_signals.py   # Generate test data
```

### Data and Logs
- `data/` - Generated data files (visitor_signals.json, master_intelligence.json)
- `logs/` - Log files (fello_operations.log, pipeline.log)
- `docs/` - Documentation (README.md, account_intelligence_sub.md)

### Python Backend Architecture

1. **Signal Generation** (`generate_signals.py`)
   - Reads from `backend/config.json` for URL/IP pools
   - Outputs to `data/visitor_signals.json`

2. **AI Research** (`research_agent.py`)
   - Uses Groq API for company intelligence
   - Reads from `backend/config.json` for API settings

3. **AI Enrichment** (`engine.py`)
   - Reads from `data/visitor_signals.json`
   - Outputs to `data/master_intelligence.json`

4. **Salesforce Sync** (`push_to_salesforce.py`)
   - Reads from `data/master_intelligence.json`
   - Upserts to `Visitor_Intelligence__c` custom object
   - Logs to `logs/fello_operations.log`

### Environment Variables
Create a `.env` file in the project root:
```
SF_USERNAME=your_sf_username
SF_PASSWORD=your_sf_password
SF_TOKEN=your_sf_security_token
```

### Python Dependencies
```bash
pip install groq simple-salesforce python-dotenv
```
