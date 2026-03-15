import { LightningElement, wire, track } from 'lwc';
import getSignals from '@salesforce/apex/IntelligenceController.getSignals';
import { refreshApex } from '@salesforce/apex';

export default class Account_Intelligence extends LightningElement {
    @track sortOrder = 'Time';
    @track visitorData = [];
    @track selectedVisitor;
    wiredResults;

    @wire(getSignals, { sortBy: '$sortOrder' })
    wiredSignals(result) {
        this.wiredResults = result;
        if (result.data) {
            this.visitorData = result.data.map(r => {
                // 1. Confidence Score Logic
                const confVal = r.Confidence_Score__c || 0;
                let cClass = confVal >= 80 ? 'conf-high' : confVal >= 50 ? 'conf-mid' : 'conf-low';

                // 2. DYNAMIC REAL-TIME SCALING (Seconds to Months)
                // Use Date.parse for reliable UTC handling from Salesforce
                const visitDate = r.Visited_At__c ? new Date(Date.parse(r.Visited_At__c)) : new Date();
                const now = new Date();
                
                // Absolute millisecond difference, protected against future-dating
                const diffMs = Math.max(0, now.getTime() - visitDate.getTime());
                const diffSec = Math.floor(diffMs / 1000);
                
                let timeStr;
                if (diffSec < 60) {
                    timeStr = 'JUST NOW';
                } else if (diffSec < 3600) {
                    const mins = Math.floor(diffSec / 60);
                    timeStr = mins === 1 ? '1m ago' : `${mins}m ago`;
                } else if (diffSec < 86400) {
                    const hrs = Math.floor(diffSec / 3600);
                    timeStr = hrs === 1 ? '1h ago' : `${hrs}h ago`;
                } else if (diffSec < 2592000) {
                    const days = Math.floor(diffSec / 86400);
                    timeStr = days === 1 ? '1 day ago' : `${days} days ago`;
                } else if (diffSec < 31536000) {
                    const months = Math.floor(diffSec / 2592000);
                    timeStr = months === 1 ? '1 month ago' : `${months} months ago`;
                } else {
                    timeStr = 'Over a year ago';
                }

                return {
                    id: r.Id,
                    company: r.Company_Name__c || 'N/A',
                    domain: r.Domain__c || 'N/A',
                    industry: r.Industry__c || 'N/A',
                    company_size: r.Company_Size__c || 'N/A',
                    hq: r.HQ_Location__c || 'N/A',
                    tech_stack: r.Tech_Stack__c || 'N/A',
                    leadership: r.Leadership__c || 'N/A',
                    intent_score: r.Intent_Score__c || 0,
                    intent_stage: r.Intent_Stage__c || 'N/A',
                    key_signals: r.Key_Signals__c || 'N/A',
                    persona: r.Persona__c || 'N/A',
                    ai_summary: r.AI_Summary__c || 'N/A',
                    sales_action: r.Sales_Action__c || 'N/A',
                    sales_hook: r.Sales_Hook__c || 'N/A',
                    visits: r.Total_Visits__c || 0, // Now reflects the Upsert count
                    confidence: confVal,
                    confClass: cClass,
                    timeAgo: timeStr,
                    duration: this.fmtTime(r.Visit_Duration__c),
                    scoreClass: this.getScoreClass(r.Intent_Score__c)
                };
            });
        }
    }

    // Modal outreach logic
    handleEmailLead() {
        const v = this.selectedVisitor;
        if (!v) return;
        const subject = encodeURIComponent(`Question regarding ${v.company}'s strategy`);
        const body = encodeURIComponent(
            `Hi,\n\nI noticed someone from the ${v.persona} team at ${v.company} was looking into our solutions.\n\n` +
            `${v.sales_hook}\n\n` +
            `Best regards,\n[Your Name]`
        );
        window.location.href = `mailto:?subject=${subject}&body=${body}`;
    }

    // Sanitized CSV Export
    // downloadExcel() {
    //     try {
    //         if (!this.visitorData || this.visitorData.length === 0) return;
    //         const headers = "Company,Score,Confidence,Last Visit,Stage,Persona,HQ,Signal,Action\n";
    //         const rows = this.visitorData.map(v => {
    //             const s = (v.key_signals || "").replace(/"/g, '""');
    //             const a = (v.sales_action || "").replace(/"/g, '""');
    //             return `"${v.company}",${v.intent_score},${v.confidence}%,"${v.timeAgo}","${v.intent_stage}","${v.persona}","${v.hq}","${s}","${a}"`;
    //         }).join("\n");

    //         const csvContent = "\uFEFF" + headers + rows;
    //         const link = document.createElement("a");
    //         link.href = 'data:text/csv;charset=utf-8;base64,' + window.btoa(unescape(encodeURIComponent(csvContent)));
    //         link.download = `Fello_Account_Intelligence_${new Date().toISOString().split('T')[0]}.csv`;
    //         link.click();
    //     } catch (e) { 
    //         console.error('Export Failed:', e); 
    //     }
    // }
downloadExcel() {
    try {
        if (!this.visitorData || this.visitorData.length === 0) return;

        // 1. Column Headers (Simplified for Data Analysis)
        const headers = "Company,Intent_Score,Confidence_Pct,Total_Visits,Visit_Duration_Seconds,Time_Ago_Mins,Stage,Persona,HQ,Signals\n";

        const rows = this.visitorData.map(v => {
            // --- DATA CLEANING FOR STATISTICS ---
            
            // Extract raw number from "85%"
            const rawConfidence = v.confidence; 

            // Extract raw number from "5 Visits" or "5"
            const rawVisits = parseInt(v.visits) || 0;

            // Extract raw number from "10" or "8"
            const rawScore = v.intent_score;

            // Convert "10m 30s" back to raw seconds for math
            // We'll use the original duration if available or a simple parse
            const rawDuration = parseInt(v.duration) || 0; 

            // Handle strings for CSV safety
            const safeSignal = (v.key_signals || "").replace(/"/g, '""');
            const safeCompany = (v.company || "").replace(/"/g, '""');

            return `"${safeCompany}",${rawScore},${rawConfidence},${rawVisits},${rawDuration},"${v.timeAgo}","${v.intent_stage}","${v.persona}","${v.hq}","${safeSignal}"`;
        }).join("\n");

        // 2. Export logic
        const csvContent = "\uFEFF" + headers + rows;
        const link = document.createElement("a");
        link.href = 'data:text/csv;charset=utf-8;base64,' + window.btoa(unescape(encodeURIComponent(csvContent)));
        link.download = `Fello_Stats_Export_${new Date().toISOString().split('T')[0]}.csv`;
        link.click();

    } catch (e) { 
        console.error('Export Error:', e); 
    }
}
    // Formatting Helpers
    fmtTime(s) { 
        if (!s) return '0s';
        return s > 60 ? `${Math.floor(s/60)}m ${s%60}s` : `${s}s`; 
    }
    
    getScoreClass(s) { 
        return s >= 8 ? 'badge high' : s >= 5 ? 'badge mid' : 'badge low'; 
    }

    // Component Events
    handleSort(e) { 
        this.sortOrder = e.detail.value; 
        return refreshApex(this.wiredResults); 
    }
    
    handleViewDetail(e) { 
        this.selectedVisitor = this.visitorData.find(v => v.id === e.currentTarget.dataset.id); 
    }
    
    closeModal() { 
        this.selectedVisitor = null; 
    }

    // Data Slicing for Banners vs Table
    get topFive() { return this.visitorData.slice(0, 5); }
    get historicalData() { return this.visitorData.slice(5); }
    get sortOptions() { return [{label:'Time', value:'Time'}, {label:'Rating', value:'Rating'}]; }
}