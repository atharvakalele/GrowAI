# Grow24 AI / GoAmrita - Future Module Classification and Naming v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Purpose:** Standard dashboard naming and future module classification for ALL NEW future modules/features

---

# 1. PURPOSE

This document defines:
- final naming recommendation for the two-dashboard architecture
- default dashboard landing behavior
- future module classification by dashboard/report behavior

This applies only to **new future modules/features**.

Legacy modules stay unchanged until a planned migration phase.

---

# 2. FINAL DASHBOARD NAMING RECOMMENDATION

Recommended final names:

## Dashboard 1
```text
Strategy Impact Dashboard
```

Short meaning:
```text
Outcome Dashboard
```

Purpose:
- Show what changed in the business
- Show effect of our intelligence and actions
- Show profit, loss prevention, rank, Buy Box, conversion, and learning impact

## Dashboard 2
```text
Activity Dashboard
```

Short meaning:
```text
Execution Dashboard
```

Purpose:
- Show what the system did
- Show runs, failures, reports, warnings, retries, approvals, and operational status

---

# 3. DEFAULT LANDING PAGE RULE

The default landing page should be:

```text
Strategy Impact Dashboard
```

Why:
- Owner should see business outcome first
- System should answer "Did we improve the business?" before showing technical operations
- This matches the MASTER philosophy: simple outside, powerful inside

The second page should be:

```text
Activity Dashboard
```

Why:
- Operator/developer/staff need operational visibility
- It keeps execution noise away from the owner-facing strategy view

---

# 4. FUTURE MODULE CLASSIFICATION

Future modules should be classified by how they contribute to dashboards.

## A. Impact-Heavy Modules

These modules mainly affect the **Strategy Impact Dashboard**.

They answer:
```text
What business impact happened?
```

Examples:
- Competitor Tracker
- Buy Box Monitor
- Listing Health
- Profit Engine
- Rank Tracker
- Review Impact
- FBA Risk / Stockout Risk
- Organic Flywheel Detector
- Product Health Score

Expected outputs:
- Raw output
- Impact summary
- Activity summary if module runs as a scheduled/automated job
- Registry entry

Dashboard behavior:
- Main dashboard priority may be high
- Activity dashboard should show run details only

## B. Activity-Heavy Modules

These modules mainly affect the **Activity Dashboard**.

They answer:
```text
What happened in the system?
```

Examples:
- Import Engine
- Scheduler
- Report Builder
- Approval Engine
- Sync Engine
- Retry / Recovery
- Notification Engine
- Token/Auth Health Monitor
- Queue Manager

Expected outputs:
- Raw output/log if needed
- Activity summary
- Registry entry
- Impact summary only if measurable business impact exists

Dashboard behavior:
- Activity dashboard priority may be high during failures
- Main dashboard should stay clean unless there is business impact

## C. Mixed Modules

These modules belong to **both dashboards**.

They answer both:
```text
What business impact happened?
What system activity happened?
```

Examples:
- Pricing / Repricing
- Campaign Optimizer
- Rule Engine
- A+ Module
- New Product Launch
- Keyword Expansion
- Budget Redistribution
- Stock Restock / FBA Shipment

Expected outputs:
- Raw output
- Impact summary
- Activity summary
- Registry entry

Dashboard behavior:
- Main Dashboard shows outcome
- Activity Dashboard shows execution
- Same module must speak in two languages:
  - business language
  - execution language

---

# 5. CLASSIFICATION RULE

Before building any new module, developer must decide:

- Is this module impact-heavy?
- Is this module activity-heavy?
- Is this module mixed?

This decision affects:
- required summaries
- dashboard target
- default display section
- priority logic
- review behavior

---

# 6. DASHBOARD TARGET MAPPING

Recommended mapping:

| Classification | dashboard_targets | Required summary |
|---|---|---|
| Impact-heavy | `main` or `both` | Impact summary |
| Activity-heavy | `activity` or `both` | Activity summary |
| Mixed | `both` | Impact + Activity summary |

## Important

If a module has any scheduled/automated run, it should usually publish an Activity Summary even if it is impact-heavy.

If a module can affect profit, rank, Buy Box, stock risk, conversion, or customer trust, it should usually publish an Impact Summary.

---

# 7. NAMING CONSISTENCY RULE

Use these names consistently in future docs and UI:

- `Strategy Impact Dashboard`
- `Activity Dashboard`
- `Impact Summary`
- `Activity Summary`
- `Report Registry`
- `Raw Output`

Avoid introducing multiple competing names unless explicitly approved.

---

# 8. QUICK EXAMPLES

## Competitor Tracker
- Classification: Impact-heavy / mixed
- Main Dashboard: Buy Box threats, rank risk, revenue at risk, competitor pressure
- Activity Dashboard: ASINs scanned, API retries, warnings, report generated

## Listing Health Module
- Classification: Impact-heavy / mixed
- Main Dashboard: Conversion risk, suppression risk, health score movement
- Activity Dashboard: ASINs scanned, warnings found, report created

## Import Engine
- Classification: Activity-heavy
- Main Dashboard: usually hidden
- Activity Dashboard: imports completed, stale data, errors, files created

## Campaign Optimizer
- Classification: Mixed
- Main Dashboard: profit effect, waste blocked, best/worst decisions
- Activity Dashboard: campaigns processed, actions generated, approvals pending

---

# 9. FINAL RULE

Future modules should never be added as dashboard clutter.

They must be classified first, then summarized correctly:

```text
Impact-heavy -> business outcome first
Activity-heavy -> execution visibility first
Mixed -> both, but separated clearly
```

---

*Future Module Classification and Naming v1.0 | 15 April 2026*  
*For NEW future modules only | Legacy modules remain unchanged until planned migration phase*
