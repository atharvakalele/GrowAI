# 🛠️ 07 — Error Handling & Logging Rules v1.1
**When to apply:** When building error handling, logging, or monitoring systems

---

## Rule 1: Comprehensive Logging
- Every important action should be logged
- Logs should have categories: INFO, WARNING, BUG, CRITICAL
- Provide log filters so user can view specific categories
- Enable: copy, download, and clear logs from UI

## Rule 2: Clear Error Messages
- If something goes wrong, log it clearly
- Include: what failed, where it failed, possible cause
- Both developers and users should benefit from clear error messages

## Rule 3: Error Handling in Every API Call
- Wrap ALL external calls (API, network, file I/O) in try-catch
- Log full error details (status code, response body, timestamp)
- Never let unhandled errors crash the system

## Rule 4: Process Monitoring
- Show active process status to user
- Notify on task start and task completion
- Let user configure notification preferences

## Rule 5: Log-Based Development
- If self-developing: always read logs to understand issues
- If using AI tools: share logs with AI for better solutions
- Logs are the foundation of debugging

## Rule 6: Safety & Stability
- Software must never damage other data or systems
- Every feature designed to prevent:
  - Accidental data loss
  - Unintended system side-effects
  - Resource exhaustion

## Rule 7: Notification Intelligence
- Implement priority-based notifications (Critical alerts separate from normal)
- Provide Silent mode option
- Critical alerts must be visually/audibly distinct from regular notifications
- Let user configure alert priority levels

## Rule 8: Error Knowledge Base
- Build Error → Reason → Fix mapping system
- Auto-suggestion system: when error occurs, suggest likely fix from past data
- Group errors by type for pattern recognition

## Rule 9: Fail-safe & Kill Switch
- **Emergency Stop button** — immediately halt all running automation
- **Safe Exit system** — gracefully stop without data corruption
- **Auto-stop on abnormal behavior** — detect anomalies (e.g., excessive API calls, unexpected data) and halt automatically
- Critical for any automation system to prevent runaway processes

---
*Category: Error Handling & Logging | Source: Msir's Universal Rulebook | Updated: 12 April 2026*
