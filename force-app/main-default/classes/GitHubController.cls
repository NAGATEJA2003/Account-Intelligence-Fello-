/**
 * GitHubController
 *
 * Apex controller for triggering GitHub Actions workflows from Salesforce.
 * Uses repository_dispatch API to trigger the Fello Account Intelligence sync.
 *
 * Setup Required:
 * 1. Create a Named Credential "GitHub_Api" with:
 *    - URL: https://api.github.com
 *    - Authentication Type: Bearertoken
 *    - Token: Your GitHub Personal Access Token (repo scope)
 * 2. Add the GitHub username and repo name in custom metadata or custom settings
 */
public with sharing class GitHubController {

    private static final String REPO_OWNER = 'NAGATEJA2003';
    private static final String REPO_NAME = 'Account-Intelligence-Fello-';

    /**
     * Triggers the GitHub Actions workflow via repository_dispatch
     *
     * @param eventType The event type to trigger (default: 'trigger-sync')
     * @param recordCount Number of signals to generate (default: 5)
     * @return Success message with workflow URL
     */
    @AuraEnabled(cacheable=false)
    public static Map<String, String> triggerWorkflow(String eventType, Integer recordCount) {
        try {
            // Validate inputs
            if (String.isBlank(eventType)) {
                eventType = 'trigger-sync';
            }
            if (recordCount == null || recordCount <= 0) {
                recordCount = 5;
            }

            // Get the dispatch endpoint
            String endpoint = 'callout:GitHub_Api/repos/' + REPO_OWNER + '/' + REPO_NAME + '/dispatches';

            // Build the payload
            Map<String, Object> payload = new Map<String, Object>();
            payload.put('event_type', eventType);

            Map<String, Object> clientPayload = new Map<String, Object>();
            clientPayload.put('record_count', recordCount);
            clientPayload.put('triggered_by', UserInfo.getName());
            clientPayload.put('triggered_date', System.now().format());
            payload.put('client_payload', clientPayload);

            // Create HTTP request
            HttpRequest req = new HttpRequest();
            req.setEndpoint(endpoint);
            req.setMethod('POST');
            req.setHeader('Accept', 'application/vnd.github.v3+json');
            req.setHeader('Content-Type', 'application/json');
            req.setBody(JSON.serialize(payload));
            req.setTimeout(30000);

            // Send the request
            Http http = new Http();
            HTTPResponse res = http.send(req);

            // Parse response
            Map<String, String> result = new Map<String, String>();

            if (res.getStatusCode() == 204) {
                result.put('status', 'SUCCESS');
                result.put('message', 'Workflow triggered successfully');
                result.put('workflowUrl', 'https://github.com/' + REPO_OWNER + '/' + REPO_NAME + '/actions');
            } else {
                result.put('status', 'ERROR');
                result.put('message', 'Failed to trigger workflow: ' + res.getBody());
                result.put('statusCode', String.valueOf(res.getStatusCode()));
            }

            return result;

        } catch (CalloutException e) {
            Map<String, String> result = new Map<String, String>();
            result.put('status', 'ERROR');
            result.put('message', 'Callout failed: ' + e.getMessage());
            return result;
        } catch (Exception e) {
            Map<String, String> result = new Map<String, String>();
            result.put('status', 'ERROR');
            result.put('message', 'Unexpected error: ' + e.getMessage());
            return result;
        }
    }

    /**
     * Gets the status of recent workflow runs
     *
     * @return List of recent workflow runs with status
     */
    @AuraEnabled(cacheable=true)
    public static List<Map<String, Object>> getRecentWorkflows() {
        try {
            String endpoint = 'callout:GitHub_Api/repos/' + REPO_OWNER + '/' + REPO_NAME + '/actions/runs?per_page=5';

            HttpRequest req = new HttpRequest();
            req.setEndpoint(endpoint);
            req.setMethod('GET');
            req.setHeader('Accept', 'application/vnd.github.v3+json');
            req.setTimeout(30000);

            Http http = new Http();
            HTTPResponse res = http.send(req);

            if (res.getStatusCode() == 200) {
                Map<String, Object> response = (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
                List<Map<String, Object>> runs = (List<Map<String, Object>>) response.get('workflow_runs');

                List<Map<String, Object>> result = new List<Map<String, Object>>();
                for (Map<String, Object> run : runs) {
                    Map<String, Object> runInfo = new Map<String, Object>();
                    runInfo.put('id', run.get('id'));
                    runInfo.put('status', run.get('status'));
                    runInfo.put('conclusion', run.get('conclusion'));
                    runInfo.put('created_at', run.get('created_at'));
                    runInfo.put('html_url', run.get('html_url'));
                    runInfo.put('name', run.get('name'));
                    result.add(runInfo);
                }
                return result;
            }

            return new List<Map<String, Object>>();

        } catch (Exception e) {
            System.debug('Error fetching workflows: ' + e.getMessage());
            return new List<Map<String, Object>>();
        }
    }

    /**
     * Checks if the GitHub integration is properly configured
     *
     * @return true if Named Credential exists and is configured
     */
    @AuraEnabled(cacheable=true)
    public static Boolean isConfigured() {
        try {
            List<NamedCredential> creds = [
                SELECT Id, DeveloperName, Endpoint
                FROM NamedCredential
                WHERE DeveloperName = 'GitHub_Api'
                LIMIT 1
            ];
            return !creds.isEmpty();
        } catch (Exception e) {
            return false;
        }
    }
}
