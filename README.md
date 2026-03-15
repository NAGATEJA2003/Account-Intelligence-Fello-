# Fello Account Intelligence Engine 🚀

An end-to-end buyer intent pipeline that bridges anonymous web traffic with Salesforce CRM insights.

## 🧠 How it Works
1. **Signal Generation**: `generate_signals.py` simulates varied visitor behavior.
2. **AI Research**: `research_agent.py` uses LLMs to perform deep firmographic research.
3. **Stateful Sync**: `push_to_salesforce.py` implements "Revised Diagnosis" logic to update Salesforce records intelligently.
4. **Dashboard**: A custom Lightning Web Component (LWC) visualizes scores, tech stacks, and sales hooks.

## 🛠️ Tech Stack
- **Backend**: Python (Groq/Llama-3)
- **Frontend**: Salesforce LWC, Apex
- **Integration**: Salesforce REST API (JSON-based)

## 📦 Setup
1. Clone the repo.
2. Add your keys to a local `config.json` (excluded from Git).
3. Run `python auto_sync.py` to start the live pipeline.
