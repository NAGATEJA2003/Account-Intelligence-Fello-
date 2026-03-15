# Team Setup Guide - Fello Account Intelligence Sync

This guide helps team members set up their own fork of the Account Intelligence workflow with their own credentials.

## Prerequisites

- GitHub account
- Salesforce account with API access
- Groq API key ([Get one here](https://console.groq.com/keys))

---

## Step 1: Fork the Repository

1. Go to https://github.com/NAGATEJA2003/Account-Intelligence-Fello-
2. Click the **Fork** button in the top-right
3. Select your account as the destination
4. Click **Create fork**

---

## Step 2: Configure GitHub Secrets

In your forked repository, add your personal credentials as secrets:

1. Go to your fork's **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** for each of the following:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `SF_USERNAME` | Your Salesforce username | `user@example.com` |
| `SF_PASSWORD` | Your Salesforce password | `your-password` |
| `SF_TOKEN` | Your Salesforce security token | `your-security-token` |
| `GROQ_API_KEY` | Your Groq API key | `gsk_...` |

---

## Step 3: Run the Workflow

### Option A: Manual Trigger (Recommended for testing)

1. In your fork, go to **Actions** tab
2. Select "Fello Account Intelligence Sync"
3. Click **Run workflow**
4. Choose options:
   - **Branch**: `main`
   - **Record count**: 5, 10, or 20
   - **Dry run**: Check this to skip Salesforce sync (for testing)
5. Click **Run workflow**

### Option B: Webhook Trigger

You can trigger the workflow via webhook from external services:

```bash
curl -X POST \
  -H "Authorization: token YOUR_GITHUB_PAT" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/YOUR_USERNAME/Account-Intelligence-Fello-/dispatches \
  -d '{"event_type":"trigger-sync"}'
```

---

## Step 4: View Results

After the workflow completes:

1. Go to **Actions** tab in your fork
2. Click on the workflow run
3. Download artifacts (logs and generated JSON files)
4. Check your Salesforce for synced records

---

## Keeping Your Fork Updated

To get the latest changes from the original repository:

```bash
# Add the original repo as a remote
git remote add upstream https://github.com/NAGATEJA2003/Account-Intelligence-Fello-.git

# Fetch latest changes
git fetch upstream

# Merge into your main branch
git checkout main
git merge upstream/main

# Push to your fork
git push origin main
```

Or use GitHub's "Sync fork" button on your fork's page.

---

## Troubleshooting

### Workflow fails with "secret not set"
- Ensure all 4 secrets are added to **your fork** (not the original repo)
- Secret names are case-sensitive

### Salesforce authentication fails
- Verify your username, password, and security token
- Check if your IP is whitelisted in Salesforce

### Groq API errors
- Verify your API key is valid
- Check if you have available quota

### Need help?
- Check the workflow logs for detailed error messages
- Download the artifacts to inspect generated files
- Open an issue in the original repository

---

## Security Best Practices

- ✅ Never share your personal access tokens or API keys
- ✅ Use strong, unique passwords
- ✅ Rotate your Salesforce security token periodically
- ✅ Monitor your Groq API usage
- ❌ Don't commit secrets to the repository
- ❌ Don't share screenshots with sensitive information
