# Local RAG Test Prompts

## 1. Basic retrieval
What is the standard VM provisioning target for ACMECloud?

## 2. Multi-document retrieval
What is the production backup retention period, and where is it documented?

## 3. Incident troubleshooting
A VM remains in QUEUED during provisioning. What known issue could explain this, and what recovery steps are recommended?

## 4. Structured data
List all Sev2 incidents in the incident dataset, including their service, region, root cause, and status.

## 5. Cross-format question
Who owns the Compute service, what is its SLO, and what team email should be used for escalation?

## 6. Policy reasoning
For a Sev1 incident, what is the acknowledgment target and how frequently should status updates be posted?

## 7. Specific lookup
What is KC-104? Give its symptom, likely cause, and workaround.

## 8. Comparison
Compare the SLOs of Compute, Storage, Network, IAM, and Monitoring.

## 9. SQL retrieval
Which incidents in the SQL dataset are associated with Compute, and what were their root causes?

## 10. HTML retrieval
What is the scheduled maintenance window?

## 11. JSON retrieval
What regions are configured in the platform JSON, and what is the backup retention value?

## 12. PPT retrieval
According to the reliability review, what were the key Q3 metrics and the top recurring issue?

## 13. Cross-source synthesis
Create a concise troubleshooting checklist for a VM stuck in QUEUED, using the runbook, known-issue data, and incident history. Clearly distinguish documented facts from recommendations.

## 14. Negative test
What is the database engine used by ACMECloud?

Expected behavior: say the datasource does not provide this information rather than inventing an answer.

## 15. Negative test
What was the root cause of INC9999?

Expected behavior: say that INC9999 is not present in the datasource.

## 16. Source awareness
For the answer about backup retention, identify which datasource file(s) support the answer.