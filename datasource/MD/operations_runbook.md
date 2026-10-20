# ACMECloud Compute Operations Runbook

## VM provisioning failure
1. Check the provisioning transaction state.
2. Identify the compute worker and image-store worker.
3. Check worker health and queue depth.
4. Review logs for `IMAGE_TRANSFER_TIMEOUT` or `STALE_QUEUE`.
5. If KC-104 symptoms are present, follow the approved worker recovery procedure.
6. Record the incident ID and validation results.

## Severity
- Sev1: complete production outage or major customer impact.
- Sev2: significant degradation with workaround available.
- Sev3: limited impact.

## Recovery validation
A VM is considered recovered when provisioning reaches ACTIVE, health checks pass, and monitoring shows no new critical alerts for 15 minutes.
