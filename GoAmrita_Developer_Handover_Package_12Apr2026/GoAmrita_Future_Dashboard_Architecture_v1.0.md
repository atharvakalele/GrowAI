# Grow24 AI / GoAmrita - Future Dashboard Architecture v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Purpose:** Dashboard architecture for ALL NEW future modules/features only

---

# 1. PURPOSE

This document defines the **two-dashboard architecture** for all **new future modules/features**.

Shared dashboard/web production code should live under:

```text
Grow24_AI/core/dashboard/
```

Do not treat `ClaudeCode/Python` as the permanent dashboard code home.

It follows the decision finalized in discussion:
- Existing/legacy modules stay unchanged for now
- New future modules must publish outputs in a way that supports:
  - Main Dashboard
  - Activity Dashboard

---

# 2. TWO-DASHBOARD MODEL

## Dashboard 1: Main Dashboard
**Purpose:** Show business effect of our system

**Short definition:** `Main Dashboard = Outcome Dashboard`

This dashboard should answer:
- Did profit increase or decrease?
- Did we prevent loss?
- Did we reduce waste?
- Did rank improve or decline?
- Did Buy Box improve or worsen?
- What business impact did our actions create?

### Main Dashboard is for
- Owner
- Strategy review
- Business decisions
- Outcome-first understanding

### Main Dashboard must NOT become
- A log screen
- A scheduler screen
- A technical status dump
- A raw API/debug page

## Dashboard 2: Activity Dashboard
**Purpose:** Show system execution, runs, failures, reports, and pending review

**Short definition:** `Activity Dashboard = Execution Dashboard`

This dashboard should answer:
- Which modules ran?
- Which failed?
- Which reports were created?
- What is pending review?
- What warnings/errors happened?
- What is blocked?

### Activity Dashboard is for
- Operator
- Developer
- Staff / execution monitoring
- Process visibility

### Activity Dashboard must NOT become
- The main owner strategy screen
- A profit-storytelling screen
- A business-effect summary replacement

---

# 2A. WHY THIS SPLIT IS STRONG

This split is strongly aligned with the MASTER philosophy:

- **Sweet outside, nuclear reactor inside**
  - Main Dashboard = sweet, simple, outcome-first
  - Activity Dashboard = reactor-room visibility, controlled and detailed

- **User sees outcomes first, mechanics second**
  - Owner should first see: "Did the business improve?"
  - Operator/developer should first see: "What ran, failed, changed, or needs review?"

- **High-value signal stays clean**
  - Business impact is not buried under logs, retries, and file activity
  - Technical activity is not mixed with profit/rank/business interpretation

- **Future scaling becomes easier**
  - As more modules are added, dashboards stay understandable
  - New features can plug in without making one giant mixed dashboard

- **Matches the MASTER architecture direction**
  - Report Layer communicates effect
  - Infrastructure/Control belongs to operations/activity view
  - Strategy impact belongs to business/outcome view

## Final principle

**Main Dashboard tells whether our system improved the business.**  
**Activity Dashboard tells what the system actually did.**

---

# 3. MAIN DASHBOARD SECTIONS

Recommended section order:

## 1. Today's Net Impact
- Net profit effect
- Loss prevented
- Waste blocked
- Revenue protected

## 2. Critical Business Risks
- Buy Box loss
- Stockout risk
- Listing suppression risk
- Competitor threat
- Review/rating impact

## 3. Movement This Period
- Profit up/down
- TACoS up/down
- True profit up/down
- Rank up/down
- Conversion up/down
- Organic trend up/down

## 4. Top Winners
- Best-performing products/campaigns
- Biggest positive business effect

## 5. Top Risks / Losers
- Biggest negative movement
- Products/campaigns needing attention

## 6. Best and Worst Decisions
- Best action and effect
- Worst action and effect

## 7. AI Learning Impact
- New permanent rules
- Promoted rules
- Learning confidence

## 8. Feature Impact Summary
- Module-wise impact rollup

## Main Dashboard golden rule

If a card/section does not help answer:

```text
"Did our system improve the business?"
```

then it probably belongs in the Activity Dashboard, not here.

---

# 4. ACTIVITY DASHBOARD SECTIONS

Recommended section order:

## 1. System Status
- Scheduler health
- Modules running
- Success/fail count
- Fresh/stale state

## 2. Pending Review / Blocked Items
- Pending approvals
- Blocked modules
- Missing manual inputs
- Retry-needed items

## 3. Recent Activity Feed
- Latest runs
- Latest changes
- Latest warnings/errors

## 4. Latest Reports
- Latest report files
- Report age
- Open/download links

## 5. Module Run Table
- Module
- Last run
- Next run
- Status
- Duration
- Warning/error count

## 6. Errors / Warnings
- Grouped operational issues

## 7. Execution History
- Actions taken
- Rollback-ready items
- Execution summaries

## 8. Infra / Sync Health
- Auth health
- API health
- Import/sync state
- Queue/retry state

## Activity Dashboard golden rule

If a card/section mainly helps answer:

```text
"What happened in the system?"
```

then it belongs here, not in the Main Dashboard.

---

# 5. DASHBOARD TARGET RULE

Every new module must declare one of:
- `main`
- `activity`
- `both`

## Meaning
- `main` = publish business impact only
- `activity` = publish system activity only
- `both` = publish both summaries and appear in both dashboards

---

# 5A. REQUIRED OUTPUT QUESTIONS FOR EVERY FUTURE MODULE

Every new future module must answer these 2 questions:

## Question 1: Business Impact
```text
What business impact happened?
```

This answer becomes the **Impact Summary** for the Main Dashboard.

## Question 2: System Activity
```text
What system activity happened?
```

This answer becomes the **Activity Summary** for the Activity Dashboard.

## Mandatory output rule

For all new future modules, minimum output expectation is:
- Raw data output
- Main-dashboard impact summary
- Activity-dashboard run summary

This is not optional for future modules.

---

# 5B. CONCRETE EXAMPLES

These examples are the model for future developers and AI tools.

## Example: Competitor Tracker

### Main Dashboard view
- Buy Box threats
- Rank risk
- Revenue at risk
- Competitor pressure score

### Activity Dashboard view
- Tracked 30 ASINs
- 2 API retries
- 1 warning
- Report generated

## Example: Listing Health Module

### Main Dashboard view
- Conversion risk
- Listing suppression risk
- Listing health score movement

### Activity Dashboard view
- 280 ASINs scanned
- 17 warnings found
- 1 report created

## Example: FBA Module

### Main Dashboard view
- Stockout risk avoided
- Storage fee risk reduced
- Shipment value protected

### Activity Dashboard view
- Inventory scan complete
- Shipment draft created
- 3 SKUs flagged

## Example rule from these examples

The same module can appear in both dashboards, but it must speak in 2 different languages:
- business language
- execution language

That is the core of this architecture.

---

# 6. DISPLAY LOGIC

## Main Dashboard
- Show highest business value first
- Show risk before low-value informational items
- Hide low-priority noise by default
- Keep top area outcome-focused, not technical

## Activity Dashboard
- Show failures/warnings/pending review at top
- Show successful normal activity lower
- Group technical noise instead of flooding the screen

---

# 7. PRIORITY MODEL

Dashboard ordering should use:

```text
priority_score = business_impact + urgency + confidence + strategic_weight
```

## Recommended weights
- Business Impact = 40%
- Urgency = 30%
- Confidence = 20%
- Strategic Weight = 10%

## Suggested score bands
- `90-100` = Critical
- `70-89` = High
- `40-69` = Medium
- `0-39` = Low

---

# 8. FUTURE RULE

No future module should write directly for dashboard UI presentation.

Instead:
1. Module writes standardized summaries
2. Registry tells dashboard what exists and where to show it
3. Dashboard renders from standardized files only

This keeps UI clean and future-proof.

---

*Future Dashboard Architecture v1.0 | 15 April 2026*  
*For NEW future modules only | Legacy dashboard/report integrations remain unchanged for now*
