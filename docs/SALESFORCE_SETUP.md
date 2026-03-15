# Salesforce Integration Setup Guide

This guide explains how to set up the Workflow Trigger component in Salesforce, allowing users to trigger GitHub Actions workflows directly from Salesforce record pages.

---

## Prerequisites

- Salesforce System Administrator access
- GitHub Personal Access Token (PAT) with `repo` scope
- GitHub Actions workflow already set up

---

## Part 1: Create GitHub Personal Access Token

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click **Generate new token (classic)**
3. Set the following:
   - **Note**: Salesforce Fello Integration
   - **Expiration**: No expiration (or set your preferred date)
   - **Scopes**: Check `repo` (Full control of private repositories)
4. Click **Generate token**
5. **Copy the token** and save it securely (you won't see it again!)

---

## Part 2: Configure Named Credential in Salesforce

### Step 1: Create Auth Provider (for GitHub)

1. In Salesforce, go to **Setup**
2. In Quick Find, enter **Auth. Providers**
3. Click **New**
4. For **Provider Type**, select **GitHub**
5. Fill in:
   - **Name**: GitHub
   - **URL Slug**: github
   - **Consumer Key**: (leave blank for testing)
   - **Consumer Secret**: (leave blank for testing)
   - **Authorize Endpoint URL**: `https://github.com/login/oauth/authorize`
   - **Token Endpoint URL**: `https://github.com/login/oauth/access_token`
6. Click **Save**

### Step 2: Create Named Credential

1. In Salesforce, go to **Setup**
2. In Quick Find, enter **Named Credentials**
3. Click **New Legacy Named Credential** or **New Named Credential**

4. For **Lightning Web Components (Modern)**, use these settings:

   | Field | Value |
   |-------|-------|
   | Label | GitHub API |
   | Name | GitHub_Api |
   | URL | `https://api.github.com` |
   | Certificate | *(Leave blank)* |
   | Identity Type | *Named Principal* |
   | Authentication Protocol | *Password Authentication* |
   | Username | *(Your GitHub username - optional)* |
   | Password | *(Paste your GitHub PAT here)* |
   | Generate Header | *Checked* |

5. **For Advanced Setup (Recommended)**, use **Bearer Token** authentication:

   | Field | Value |
   |-------|-------|
   | Label | GitHub API |
   | Name | GitHub_Api |
   | URL | `https://api.github.com` |
   | Certificate | *(Leave blank)* |
   | Identity Type | *Named Principal* |
   | Authentication Protocol | *No Authentication* |
   | **Allow Merge Fields in HTTP Header** | *Checked* |
   | **Merge Field Value for HTTP Header** | `Authorization: Bearer YOUR_GITHUB_PAT` |

   > **Note**: For production, store the PAT in Custom Metadata or a Protected Custom Setting and reference it as `{!$Setup.Credentials__c.GitHub_Token__c}`

6. Click **Save**

7. **Test the connection**:
   - In the Named Credential detail page, click **Test Connection**
   - You should see: `"current_user_url": "https://api.github.com/user"` in the response

---

## Part 3: Deploy the Components

### Option A: Deploy via SFDX (Recommended)

```bash
# Navigate to your project directory
cd force-app/main/default

# Deploy the workflow trigger component
sf project deploy start --source-dir force-app/main-default/lwc/workflowTrigger --source-dir force-app/main-default/classes/GitHubController.cls --source-dir force-app/main-default/classes/GitHubControllerTest.cls

# Or deploy everything
sf project deploy start
```

### Option B: Deploy via Salesforce UI

1. In Salesforce, go to **Setup**
2. In Quick Find, enter **Lightning Components**
3. Click **New Component**
4. For each file:
   - Copy the content from `force-app/main-default/lwc/workflowTrigger/`
   - **workflowTrigger.js** → JavaScript
   - **workflowTrigger.html** → Markup
   - **workflowTrigger.css** → Style
   - **workflowTrigger.js-meta.xml** → Metadata (or configure in UI)

5. For Apex Classes:
   - Go to **Setup** → **Apex Classes**
   - Click **New**
   - Paste `GitHubController.cls` content
   - Repeat for `GitHubControllerTest.cls`

---

## Part 4: Add Component to a Page

### Add to Record Page

1. Navigate to any record page (e.g., Account, Opportunity)
2. Click the **gear icon** → **Edit Page**
3. In the Lightning App Builder, find **Workflow Trigger** under Custom components
4. **Drag and drop** it onto the page where you want it
5. (Optional) Configure properties:
   - **Title**: Account Intelligence Sync
   - **Description**: Trigger AI-powered analysis
   - **Button Label**: Run Analysis
   - **Show Recent Workflows**: Checked
6. Click **Save** and **Activate**

### Add to Home Page or App Page

1. Go to **Setup** → **Lightning App Builder**
2. Click **New** → **App Page** or **Home Page**
3. Choose a template and click **Finish**
4. Add the **Workflow Trigger** component
5. Configure and save

---

## Part 5: Set Permissions

1. Go to **Setup** → **Permission Sets** or **Profiles**
2. Create or edit a permission set for users who need access
3. Under **Enabled Settings**, ensure:
   - ✅ **API Enabled**
   - ✅ **Apex Class Access** → Add `GitHubController`
   - ✅ **Lightning Web Components** → Add `workflowTrigger`
4. Assign the permission set to users

---

## Part 6: Test the Integration

1. Open a page with the Workflow Trigger component
2. Select the number of records
3. (Optional) Check **Dry Run** to skip Salesforce sync
4. Click **Run Intelligence Sync**
5. You should see:
   - ✅ Success message
   - ✅ Workflow runs appearing in "Recent Workflow Runs"
6. Click **View** on any workflow to see the GitHub Actions run

---

## Troubleshooting

### "GitHub integration is not configured"

**Cause**: Named Credential is missing or misnamed

**Solution**:
1. Verify Named Credential exists with DeveloperName `GitHub_Api`
2. Check the name matches exactly (case-sensitive)
3. Test the connection in the Named Credential detail page

### "Callout failed: Unauthorized"

**Cause**: GitHub token is invalid or expired

**Solution**:
1. Verify your GitHub PAT is valid
2. Ensure it has `repo` scope
3. Regenerate the token if needed and update the Named Credential

### "Failed to trigger workflow: 404 Not Found"

**Cause**: Repository name or owner is incorrect

**Solution**:
1. Update `REPO_OWNER` and `REPO_NAME` in `GitHubController.cls`
2. Ensure the repository exists and you have access
3. For private repos, ensure your PAT has access

### No workflows appearing

**Cause**: Named Credential authentication issue

**Solution**:
1. Check that "Allow Merge Fields in HTTP Header" is checked
2. Verify the Authorization header format: `Bearer YOUR_TOKEN`
3. Test the Named Credential connection

### For more help

- Check the **Debug Logs** in Salesforce Setup
- Review the **GitHub Actions** tab in your repository
- Check the **Apex Test Execution** for test failures

---

## Security Best Practices

✅ **DO**:
- Use Named Credentials for storing GitHub tokens
- Restrict who can trigger workflows via permission sets
- Monitor GitHub Actions logs for unusual activity
- Use separate GitHub tokens for different environments
- Set appropriate expiration dates on tokens

❌ **DON'T**:
- Hardcode tokens in Apex code
- Share tokens via email or chat
- Grant unnecessary GitHub scopes
- Allow unauthenticated access
- Use production tokens for testing

---

## Advanced Configuration

### Store Token in Custom Metadata (Production-Ready)

1. Create Custom Metadata Type `GitHub_Config__mdt`
2. Add field `Token__c` (Text, 255 chars, Encrypted)
3. Create a record with your PAT
4. Update Named Credential to reference: `{!$CustomMetadata.GitHub_Config__mdt.Default.Token__c}`

### Multiple Environments

Use different Named Credentials for dev, test, and prod:

- `GitHub_Api_Dev`
- `GitHub_Api_Test`
- `GitHub_Api_Prod`

Then update `GitHubController.cls` to use the appropriate one based on environment.

### Audit Trail

Enable **Debug Logs** for users triggering workflows to track:
- When workflows were triggered
- Who triggered them
- What parameters were used
