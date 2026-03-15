/**
 * Workflow Trigger Component
 *
 * A Salesforce LWC that allows users to trigger GitHub Actions workflows
 * directly from a Salesforce record page or Lightning App Builder page.
 *
 * Features:
 * - Trigger workflow with configurable parameters
 * - Display recent workflow runs
 * - Show workflow status and logs
 * - Real-time updates
 */

import { LightningElement, api, wire, track } from 'lwc';
import { refreshApex } from '@salesforce/apex';
import triggerWorkflow from '@salesforce/apex/GitHubController.triggerWorkflow';
import getRecentWorkflows from '@salesforce/apex/GitHubController.getRecentWorkflows';
import isConfigured from '@salesforce/apex/GitHubController.isConfigured';

export default class WorkflowTrigger extends LightningElement {
    // Public properties
    @api recordId;
    @api title = 'Account Intelligence Sync';
    @api description = 'Trigger the AI-powered account intelligence workflow';
    @api buttonLabel = 'Run Intelligence Sync';
    @api showRecentWorkflows = true;

    // Track properties
    @track loading = false;
    @track error = null;
    @track successMessage = null;
    @track isConfiguredValue = false;
    @track recentWorkflows = [];
    @track showWorkflows = false;

    // Configuration options
    recordCountOptions = [
        { label: '5 records', value: '5' },
        { label: '10 records', value: '10' },
        { label: '20 records', value: '20' }
    ];

    selectedRecordCount = '5';
    dryRun = false;

    // Apex method results
    _isConfiguredResult;
    _workflowsResult;

    @wire(isConfigured)
    wiredIsConfigured(result) {
        this._isConfiguredResult = result;
        if (result.data) {
            this.isConfiguredValue = result.data;
            if (!this.isConfiguredValue) {
                this.error = 'GitHub integration is not configured. Please contact your administrator.';
            }
        } else if (result.error) {
            this.error = 'Unable to check configuration: ' + (result.error.body?.message || result.error.message);
        }
    }

    @wire(getRecentWorkflows)
    wiredWorkflows(result) {
        this._workflowsResult = result;
        if (result.data) {
            this.recentWorkflows = result.data.map(workflow => ({
                ...workflow,
                statusClass: this.getStatusClass(workflow.status, workflow.conclusion),
                createdDate: new Date(workflow.created_at).toLocaleString()
            }));
        } else if (result.error) {
            console.error('Error fetching workflows:', result.error);
        }
    }

    get hasWorkflows() {
        return this.recentWorkflows && this.recentWorkflows.length > 0;
    }

    getStatusClass(status, conclusion) {
        if (status === 'completed') {
            return conclusion === 'success' ? 'slds-text-color_success' : 'slds-text-color_error';
        } else if (status === 'in_progress') {
            return 'slds-text-color_weak';
        }
        return 'slds-text-color_default';
    }

    get statusIcon(conclusion) {
        switch (conclusion) {
            case 'success':
                return 'utility:success';
            case 'failure':
                return 'utility:error';
            case 'cancelled':
                return 'utility:close';
            default:
                return 'utility:refresh';
        }
    }

    handleRecordCountChange(event) {
        this.selectedRecordCount = event.target.value;
    }

    handleDryRunChange(event) {
        this.dryRun = event.target.checked;
    }

    async handleTrigger() {
        this.loading = true;
        this.error = null;
        this.successMessage = null;

        try {
            const result = await triggerWorkflow({
                eventType: 'trigger-sync',
                recordCount: parseInt(this.selectedRecordCount)
            });

            if (result.status === 'SUCCESS') {
                this.successMessage = result.message;
                this.showWorkflows = true;

                // Refresh the workflow list
                await refreshApex(this._workflowsResult);

                // Auto-hide success message after 5 seconds
                setTimeout(() => {
                    this.successMessage = null;
                }, 5000);
            } else {
                this.error = result.message || 'Failed to trigger workflow';
            }
        } catch (err) {
            this.error = err.body?.message || err.message || 'An unexpected error occurred';
            console.error('Error triggering workflow:', err);
        } finally {
            this.loading = false;
        }
    }

    toggleWorkflows() {
        this.showWorkflows = !this.showWorkflows;
    }

    openWorkflow(event) {
        const url = event.currentTarget.dataset.url;
        window.open(url, '_blank');
    }

    refreshWorkflows() {
        refreshApex(this._workflowsResult);
    }
}
