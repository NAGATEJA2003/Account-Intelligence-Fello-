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

## 📦 Quick Start

### Option 1: Run Locally
```bash
# Clone the repo
git clone https://github.com/NAGATEJA2003/Account-Intelligence-Fello-.git
cd Account-Intelligence-Fello-

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GROQ_API_KEY="your-groq-api-key"
export SF_USERNAME="your-salesforce-username"
export SF_PASSWORD="your-salesforce-password"
export SF_TOKEN="your-salesforce-security-token"

# Run the full pipeline
python run_sync.py
```

### Option 2: Use GitHub Actions (Team Collaboration)
Each team member can fork and run with their own credentials:
- 👉 **[Team Setup Guide](docs/TEAM_SETUP.md)** - Complete instructions for forking and configuring

---

## 📋 Features

| Feature | Description |
|---------|-------------|
| **AI-Powered Analysis** | Uses Groq Llama-3 for deep company research |
| **Real-time Scoring** | Intent scores and confidence metrics |
| **Salesforce Sync** | Stateful upsert logic prevents duplicate records |
| **LWC Dashboard** | Visualize intelligence directly in Salesforce |
| **CI/CD Ready** | GitHub Actions workflow for automated runs |

---

## 🤝 Contributing

Contributions are welcome! For team setup instructions, see [TEAM_SETUP.md](docs/TEAM_SETUP.md).
