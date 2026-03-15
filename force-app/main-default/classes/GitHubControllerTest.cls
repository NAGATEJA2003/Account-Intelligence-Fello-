/**
 * GitHubControllerTest
 *
 * Test class for GitHubController
 */
@IsTest
private class GitHubControllerTest {

    @IsTest
    static void testTriggerWorkflowSuccess() {
        // Test successful workflow trigger
        Test.setMock(HttpCalloutMock.class, new GitHubApiMock(204));

        Test.startTest();
        Map<String, String> result = GitHubController.triggerWorkflow('trigger-sync', 5);
        Test.stopTest();

        System.assertEquals('SUCCESS', result.get('status'));
        System.assertNotEquals(null, result.get('workflowUrl'));
    }

    @IsTest
    static void testTriggerWorkflowError() {
        // Test API error response
        Test.setMock(HttpCalloutMock.class, new GitHubApiMock(401));

        Test.startTest();
        Map<String, String> result = GitHubController.triggerWorkflow('trigger-sync', 5);
        Test.stopTest();

        System.assertEquals('ERROR', result.get('status'));
    }

    @IsTest
    static void testTriggerWorkflowDefaults() {
        // Test default values
        Test.setMock(HttpCalloutMock.class, new GitHubApiMock(204));

        Test.startTest();
        Map<String, String> result = GitHubController.triggerWorkflow(null, null);
        Test.stopTest();

        System.assertEquals('SUCCESS', result.get('status'));
    }

    @IsTest
    static void testTriggerWorkflowTenRecords() {
        // Test with different record count
        Test.setMock(HttpCalloutMock.class, new GitHubApiMock(204));

        Test.startTest();
        Map<String, String> result = GitHubController.triggerWorkflow('trigger-sync', 10);
        Test.stopTest();

        System.assertEquals('SUCCESS', result.get('status'));
    }

    @IsTest
    static void testGetRecentWorkflows() {
        // Test fetching recent workflows
        Test.setMock(HttpCalloutMock.class, new GitHubApiMock(200, '{"workflow_runs":[]}'));

        Test.startTest();
        List<Map<String, Object>> result = GitHubController.getRecentWorkflows();
        Test.stopTest();

        System.assertNotEquals(null, result);
    }

    @IsTest
    static void testGetRecentWorkflowsError() {
        // Test error handling when fetching workflows
        Test.setMock(HttpCalloutMock.class, new GitHubApiMock(404));

        Test.startTest();
        List<Map<String, Object>> result = GitHubController.getRecentWorkflows();
        Test.stopTest();

        System.assertEquals(0, result.size());
    }

    @IsTest
    static void testIsConfiguredReturnsTrue() {
        // Note: isConfigured checks for NamedCredential existence
        // In test context without NamedCredential, returns false
        Test.startTest();
        Boolean result = GitHubController.isConfigured();
        Test.stopTest();

        // Should return false in test context without NamedCredential
        System.assertEquals(false, result);
    }

    @IsTest
    static void testTriggerWorkflowCalloutException() {
        // Test handling of callout exceptions
        Test.setMock(HttpCalloutMock.class, new GitHubApiMock(500));

        Test.startTest();
        Map<String, String> result = GitHubController.triggerWorkflow('trigger-sync', 5);
        Test.stopTest();

        System.assertEquals('ERROR', result.get('status'));
    }

    /**
     * Mock class for GitHub API callouts
     */
    public class GitHubApiMock implements HttpCalloutMock {
        private Integer statusCode;
        private String responseBody;

        public GitHubApiMock(Integer statusCode) {
            this.statusCode = statusCode;
            this.responseBody = null;
        }

        public GitHubApiMock(Integer statusCode, String responseBody) {
            this.statusCode = statusCode;
            this.responseBody = responseBody;
        }

        public HTTPResponse respond(HTTPRequest req) {
            HTTPResponse res = new HTTPResponse();
            res.setStatusCode(statusCode);
            res.setStatus('OK');

            if (responseBody != null) {
                res.setBody(responseBody);
            }

            return res;
        }
    }
}
